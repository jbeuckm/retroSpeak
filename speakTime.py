#!/usr/bin/env python
#********************
# retroSpeak example - speak date and time
# Ensure retroSpeak.py and vocabulary.py are in the path or same directory 
# as this script
#
#   usage: speakTime.py [-h] [-c MHZ] [-t] [-d]
#
#   Speaks the time and date using retroSpeak
#
#   optional arguments:
#   -h, --help           show this help message and exit
#   -c MHZ, --clock MHZ  Clock speed in MHz - range 1.0 to 5.1
#   -t, --time           Speak time only
#   -d, --date           Speak time only
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

import datetime
import argparse

import retroSpeak
from vocabulary import *

def timeToSpeak(now):
    # return allophones for the time
    hour = now.hour
    minute = now.minute
    # am/pm
    if hour>12:
        ampm=vocabulary['p']
        hour = hour - 12
    else:
        ampm=vocabulary['a']
    ampm += ' PA4 ' + vocabulary['m'] + ' PA5 '
    # Hours
    if hour > 0:
        hours = numbers[hour]
    else:
        hours = numbers[12]
    hours += ' PA4 '
    # Minutes
    if minute == 0:
        minutes = ''
    elif minute < 21:
        minutes = numbers[minute]
        if minute < 10:
            minutes = vocabulary['o'] + ' PA4 ' + minutes
    else:
        minutes = numbers[(minute/10)*10]
        if minute % 10 > 0:
            minutes = minutes + ' PA4 ' + numbers[minute % 10]
    minutes += ' PA4 '
    return 'PA5 ' + vocabulary['the'] + ' PA4 ' + vocabulary['time'] + ' PA4 ' + vocabulary['is'] +\
                    ' PA4 ' + hours + minutes + ampm

def dateToSpeak(now):
    # return allophones for the date
    weekday = daysOfWeek[now.weekday()]
    month = vocabulary[now.strftime('%B').lower()]
    day = daysOfMonth[now.day]
    return 'PA5 ' + vocabulary['today'] + ' PA4 ' + vocabulary['is'] + ' PA4 ' +\
        weekday + ' PA4 ' + vocabulary['the'] + ' PA4 ' + day + ' PA4 ' + \
        vocabulary['of'] + ' PA4 ' + month + ' PA4 '

def clockSpeed(freq):
    freq = float(freq)
    if freq < 1.0 or freq > 5.1:
        raise argparse.ArgumentTypeError("%r not in range [1.0, 5.1]"%(freq,))
    return freq

parser = argparse.ArgumentParser(description='Speaks the time and date using retroSpeak')
parser.add_argument('-c','--clock', action="store", default='3.12', dest='mhz', type=clockSpeed, help='Clock speed in MHz - range 1.0 to 5.1')
parser.add_argument('-t','--time', action="store_const", const=True, default=False, dest='timeOnly', help='Speak time only')
parser.add_argument('-d','--date', action="store_const", const=True, default=False, dest='dateOnly', help='Speak time only')
parser.add_argument('-b','--board', action="store", default=0, dest='board', type=int, choices=range(0,4), help='Select retroSpeak device 0-3 - default is 0')


args = parser.parse_args()

# Initialise retroSpeak board
speech = retroSpeak.retroSpeak(clock=args.mhz,device=args.board)

now = datetime.datetime.now()

if args.dateOnly and args.timeOnly:
    args.dateOnly = False
    args.timeOnly = False
# Speak the time and date
if not(args.dateOnly):
    speech.speakAndWait( timeToSpeak(now) )
if not(args.timeOnly):
    speech.speakAndWait( dateToSpeak(now) )