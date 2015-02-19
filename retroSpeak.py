#!/usr/bin/env python
#********************
# retroSpeak library
# retroSpeak is a Raspberry Pi controlled speech synthesizer using the vintage 
# SP0256-AL2
#
# Requires WiringPi2 and WiringPi2-Python
#
# The SP0256 is connected to pins on the MCP23S17
# The clock for the SP0256 is generated using a programmable oscillator LTC6903
# Both use SPI for control - allowing other GPIO pins to be used
# The clock can be adjusted from 1MHz to 5.1MHz. The suggested speed in the
# SP0256 datasheet is for 3.12MHz - which is the default.
#
# It is possible to stack up to 4 retroSpeak boards onto a Raspberry Pi
# To control more than one, create a new instance of the class, but with
# a different device number corresponding to jumpers set on the PCB
#
# The retroSpeak class only can speak allophones. It doesn't do text-to-speech.
# Look at vocabulary.py for a wordlist compiled from the list in the datasheet (with
# some additions) - or for a basic text to speech look at retroTTS.py that implements
# the Naval Research Laboratory (NRL) algorithm.
#
# retroSpeak plays the list of allophones in a separate thread - so your program 
# can do other things while it is speaking.
#
# Callbacks can be used to do something when an allophone is started, or when speech
# is started or finished. Look at the code at the end for an example. It should
# be possible to synchronise speech with flashing LEDs for example, or to shape 
# a robot mouth.
#
# (c) 2015 Jason Lane
#
# https://github.com/jas8mm/retroSpeak
#
# BSD Licence
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#******************** 

import array
import math
import time
import threading
import Queue
import atexit
from inspect import isfunction

import wiringpi2 as wiringpi
from wiringpi2 import GPIO

class retroSpeak():

    # Raspberry pi has two CS pins on SPI port 0
    _SP0256channel=0
    _LTC6903channel=1

    # Allophone lookup table from datasheet
    _allophones = { 'PA1':0, 'PA2':1, 'PA3':2, 'PA4':3, 'PA5':4, 'OY':5, 'AY':6, 'EH':7, 
             'KK3':8, 'PP':9, 'JH':10, 'NN1':11, 'IH':12, 'TT2':13, 'RR1':14, 'AX':15, 
             'MM':16, 'TT1':17, 'DH1':18, 'IY':19, 'EY':20, 'DD1':21, 'UW1':22, 'AO':23, 
             'AA':24, 'YY2':25, 'AE':26, 'HH1':27, 'BB1':28, 'TH':29, 'UH':30, 'UW2':31, 
             'AW':32, 'DD2':33, 'GG3':34, 'VV':35, 'GG1':36, 'SH':37, 'ZH':38, 'RR2':39, 
             'FF':40, 'KK2':41, 'KK1':42, 'ZZ':43, 'NG':44, 'LL':45, 'WW':46, 'XR':47, 
             'WH':48, 'YY1':49, 'CH':50, 'ER1':51, 'ER2':52, 'OW':53, 'DH2':54, 'SS':55, 
             'NN2':56, 'HH2':57, 'OR':58, 'AR':59, 'YR':60, 'GG2':61, 'EL':62, 'BB2':63 };

    # A queue of allophone numbers to speak in the background
    _speaking = Queue.Queue(500)
    _isSpeaking = False

    # Device number of the MCP23S17 - set with jumpers on the PCB
    _deviceNum = 0

    # pins on MCP23S17
    _ADDR = 0
    _ALD = 6
    _SBY = 7
    _RESET = 8
    _CLKCS = 9
    _GPIO1 = 10
    
    # Clock speed
    _clock = 3.12
    
    # callbacks
    _onStart = None
    _onAllophone = None
    _onStop = None

    def __init__(self, setupSys=True, base=100, device=0, clock=3.12):
        if setupSys:
            # give option of using a different wiringpi setup elsewhere
            wiringpi.wiringPiSetupSys()
        # Up to 4 retroSpeak boards can be stacked - use a different base and device number for each
        if device>3: 
            device=3 
        elif device<0: 
            device=0
        self._deviceNum = int(device)
        wiringpi.mcp23s17Setup(base,self._SP0256channel,self._deviceNum)
        wiringpi.wiringPiSPISetup(self._LTC6903channel,1000000)
        self._ADDR = base
        self._ALD = base+6
        self._SBY = base+7
        self._RESET = base+8
        self._CLKCS = base+9
        self._GPIO1 = base+10
        for n in range(base,base+16):
            # Set all pins as outputs
            wiringpi.pinMode(n,GPIO.OUTPUT)
        # Except standby pin
        wiringpi.pinMode(self._SBY,GPIO.INPUT)
        self.setClock(clock) 
        self.reset()
        # Disable speech chip when quitting program - otherwise 
        # chip may keep sounding if program crashes or Ctrl-C is used
        atexit.register(self.disable)
        # set up speaker thread
        thread = threading.Thread(target=self.speaker, args=())
        thread.daemon = True # Daemonize thread
        thread.start() # Start the execution

    def speaker(self):
        # Thread to speak allophones in the background
        while True:
            if not self._speaking.empty():
                if not(self._isSpeaking):
                    # Only just started speaking
                    self._isSpeaking = True
                    if self._onStart != None:
                        self._onStart()
                allophone = self._speaking.get()
                a = self._allophones[allophone]
                # Switch on voice chip
                wiringpi.digitalWrite(self._ALD,True)
                wiringpi.digitalWrite(self._RESET,True)
                # put the allophone number on the address lines
                for b in range(0,6):
                    # write each bit to A1-A6
                    wiringpi.digitalWrite(self._ADDR+b,a>>b & 1)
                # A low pulse on ALD (Address Load) starts the speech
                wiringpi.digitalWrite(self._ALD,False)
                wiringpi.digitalWrite(self._ALD,True)
                if self._onAllophone != None:
                    # Allophone callback
                    self._onAllophone(allophone)
                # And wait for SBY standby to go high - it is low when
                # chip is outputting speech - or 2 seconds in case things went wrong
                startTime = wiringpi.millis()
                while ((wiringpi.millis()-startTime) < 2000) and ( not wiringpi.digitalRead(self._SBY)):
                    # Let's delay to save polling constantly
                    time.sleep(0.01)
            else:
                if self._isSpeaking:
                    # Just finished speaking a sequence so check for stopped callback
                    if self._onStop != None:
                        self._onStop()
                self._isSpeaking = False

    def listAllophones(self):
        # returns the allophones as a list
        return sorted(keys(self._allophones))

    def isSpeaking(self):
        # True if chip is speaking
        # Need to check for both empty queue and _isSpeaking flag
        # as list might not be empty, but synthesizer hasn't started
        # speaking; and list might be empty, but last phoneme is still being spoken
        return not(self._speaking.empty()) or self._isSpeaking

    def stopSpeaking(self):
        # Clear queue and wait for current allophone to finish
        self._speaking.queue.clear()
        while self.isSpeaking():
            time.sleep(0.02)

    def speak( self, speech ):
        # Convert valid allophones to numbers and add to queue
        # Speech should be a string of allophones separated by spaces 
        for allophone in speech.upper().split():
            #print( allophone ),
            # Ignore strings not in allophone table
            if allophone in self._allophones:
                # put the speaking queue
                self._speaking.put(allophone)
            #else:
            #    print( "Invalid allophone: {}".format(allophone) )

    def speakList( self, allophones ):
        # Add list of allophones to speaking queue
        for allophone in allophones:
            if allophone.upper() in self._allophones:
                self._speaking.put(allophone.upper())

    def speakAndWait(self,speech):
        # Speak allophones, but wait until they're spoken
        self.speak(speech)
        while self.isSpeaking():
            time.sleep(0.05) 

    def wait(self):
        # Wait until speech is finished
        while self.isSpeaking():
            time.sleep(0.05) 

    def enable(self):
        # Enable speech chip - may click output amp
        wiringpi.digitalWrite(self._RESET,True)

    def disable(self):
        # Disable speech chip - may click output amp
        self.stopSpeaking()
        wiringpi.digitalWrite(self._RESET,False)

    def reset(self):
        # Toggle reset line - resets the speech chip
        wiringpi.digitalWrite(self._RESET,False)
        wiringpi.digitalWrite(self._ALD,True)
        wiringpi.digitalWrite(self._RESET,True)

    def _freqToCode( self, f, clk=1 ):
        # Calculate the octave and DAC settings for the LTC6903
        # f should be the frequency in MHz
        # clk is the clock mode - 0-3
        # calculate octave, frequency as per datasheet and 
        # returns a 16bit code to program the osc 
        # Details here: http://www.linear.com/product/LTC6903
        f = f*1000000 # convert to Hz
        octave = int( math.floor(3.322*math.log(f/1039.0,10)) )
        if octave<0: 
            octave=0
        elif octave>15:
            octave=15
        # calculate DAC code
        dac = int( round(2048-(2078*math.pow(2,10+octave))/f) )
        if dac<0: 
            dac=0
        elif dac>1023:
            dac=1023
        buf = ( (octave<<12) | (dac<<2) | (clk & 3) ) & 0xFFFF # 16 bit number
        # returns a 2 character string as wiringPiSPIDataRW requires a string type
        return chr(buf >> 8)+chr(buf & 0xFF)

    def setClock(self, clock):
        # Set clock speed using LTC6903
        # LTC6903 isn't individually addressable - so the CE pin is OR'd with
        # a GPIO pin on the MCP23S17. When both are low the oscillator
        # can be programmed. This allows retroSpeak boards to be stacked
        if clock < 1.0:
            # Limit frequency of clock. SP0256 has a limited range of speeds
            clock = 1.0
        elif clock > 5.1:
            clock = 5.1
        self._clock = clock
        code = self._freqToCode(clock)
        wiringpi.digitalWrite(self._CLKCS,False) # Enable clock programming
        # write clock to SPI port
        if wiringpi.wiringPiSPIDataRW(self._LTC6903channel, code):
            # if successful SPIDataRW returns a number > 0
            self._clock = clock
        else:
            print("Error setting clock.")
        wiringpi.digitalWrite(self._CLKCS,True)
        
    def clockSpeed(self):
        # return current clock speed
        return self._clock

    # Set up callbacks

    def setCallbackStart(self,callback):
        if isfunction(callback):
            self._onStart = callback
        else:
            self._onStart = None
    
    def setCallbackStop(self,callback):
        if isfunction(callback):
            self._onStop = callback
        else:
            self._onStop = None

    def setCallbackAllophone(self,callback):
        if isfunction(callback):
            self._onAllophone = callback
        else:
            self._onAllophone = None

    def GPIObase(self):
        # returns pin number of the first of the 6 spare GPIO pins on MCP23S17
        return self._GPIO1


if __name__ == '__main__':
    # Example to demonstrate speech, and ability to do work while speaking.
    import sys

    # Callback functions called while speaking
    def onStart():
        print "Starting..."

    def onAllophone(a):
        print a,
        sys.stdout.flush()

    def onFinish():
        print "Finished..."

    def alternateSpeed(a):
        try:
            alternateSpeed.spd = not(alternateSpeed.spd)
        except AttributeError:
            alternateSpeed.spd = True
        if alternateSpeed.spd:
            speech.setClock(3.12)
        else:
            speech.setClock(4)

    print("retroSpeak test")
    speech = retroSpeak(clock=3.12,device=0)
    speech.setCallbackAllophone(onAllophone)
    speech.setCallbackStart(onStart)
    speech.setCallbackStop(onFinish)
    # Hello World
    utterances = [("Hello World", "HH1 EH ll LL AX OW PA4 WW ER1 LL DD2 PA5 "),
                  ("I am a computer",
                  "aa ay pa3 aa mm pa3 ey pa3 kk1 ax mm pp yy1 uw1 tt2 er1 pa5 "),
                  ("My name is Raspberry Pi",
                  "mm ay pa3 nn2 ey mm pa3 ih ih zz pa3 rr2 ax ss ss bb1 er2 rr2 ey pa3 pp aa ay pa5 ") ]
    # Different speeds
    for speed in [3.12,1.5,2,4,5]:
        speech.setClock(speed)
        print("Clock: {}MHz".format(speed))
        for (words,allophones) in utterances:
            print(words)
            speech.speakAndWait(allophones)
    # Different speed for each allophone - set with callback
    speech.setCallbackAllophone(alternateSpeed)
    speech.setCallbackStart(None)
    speech.setCallbackStop(None)
    print("Wobbly...")
    for (words,allophones) in utterances:
        print(words)
        speech.speakAndWait( allophones )
    print("Done")

