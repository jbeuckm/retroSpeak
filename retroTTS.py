#!/usr/bin/env python
#
# retroSpeak project
#
# A very primitive text to speech command. Only converts text at
# the command line. No attempt is made to convert numbers, much
# punctuation.
#
# As this is based heavily on Public Domain work, this code is relased as public domain.
#
# Ensure retroSpeak.py, en_US_rules.py and vocabulary.py are in the path or 
# same directory as this script
#
# Jason Lane 2015
#
# English to Phoneme text to speech
# Python version of Naval Research Laboratory algorithm
# described in NRL Report 7948 January 21st, 1976 Elovitz et al
# http://www.dtic.mil/cgi-bin/GetTRDoc?AD=ADA021929
# Adapted from the public domain C version by Wasser, 1985
# Retrieved from: ftp://svr-ftp.eng.cam.ac.uk/pub/comp.speech/synthesis/english2phoneme.tar.gz
#
# Outputs a form of International Pronounciation Alphabet (IPA) which is mapped
# to the allophone set used by the SP0256-AL2 in the retroSpeak project
#
#   The Phoneme codes (US English):
# 
#           IY      bEEt            IH      bIt
#           EY      gAte            EH      gEt
#           AE      fAt             AA      fAther
#           AO      lAWn            OW      lOne
#           UH      fUll            UW      fOOl
#           ER      mURdER          AX      About
#           AH      bUt             AY      hIde
#           AW      hOW             OY      tOY
#           p       Pack            b       Back
#           t       Time            d       Dime
#           k       Coat            g       Goat
#           f       Fault           v       Vault
#           TH      eTHer           DH      eiTHer
#           s       Sue             z       Zoo
#           SH      leaSH           ZH      leiSure
#           HH      How             m       suM
#           n       suN             NG      suNG
#           l       Laugh           w       Wear
#           y       Young           r       Rate
#           CH      CHar            j       Jar
#           WH      WHere
#
#
#   Rules are made up of four parts:
#   
#           The left context.
#           The text to match.
#           The right context.
#           The phonemes to substitute for the matched text.
#
#   Procedure:
# 
#           Seperate each block of letters (apostrophes included) 
#           and add a space on each side.  For each unmatched 
#           letter in the word, look through the rules where the 
#           text to match starts with the letter in the word.  If 
#           the text to match is found and the right and left 
#           context patterns also match, output the phonemes for 
#           that rule and skip to the next unmatched letter.
# 
# 
#   Special Context Symbols:
# 
#           #       One or more vowels
#           :       Zero or more consonants
#           ^       One consonant.
#           .       One of B, D, V, G, J, L, M, N, R, W or Z (voiced 
#                   consonants)
#           %       One of ER, E, ES, ED, ING, ELY (a suffix)
#                   (Found in right context only)
#           +       One of E, I or Y (a "front" vowel)
# 


import argparse

import retroSpeak
from en_US_rules import Rules
from vocabulary import *

# Parts of rules
leftPart  = 0
matchPart = 1
rightPart = 2
outPart   = 3

def isVowel(c):
    return c in ('A','E','I','O','U')

def isConsonant(c):
    return c.isupper() and not isVowel(c)

def translateWord(word):
    # Return a list of IPA phonemes that make up the word
    phonemes = ''
    word = ' ' + word + ' ' # Add padding spaces either side of word
    index=1 # start on first letter of word - after added space
    while index < len(word)-1:
        #print "Index: {} Letter:{}".format(index,word[index])
        if word[index].isupper():
            letterRules = Rules[word[index]]
        else:
            letterRules = Rules['punctuation']
        index,phoneme = findRule(word,index,letterRules)
        if phoneme != '':
            phonemes = phonemes + ' ' + phoneme
    return phonemes.split()
    
def findRule( word, index, rules ):
    # Find the matching rule for the character in the word
    # index is the position of the character to check
    # rules is a list of the rules corresponding to the character    
    # Find a matching centre pattern, then check the left and right patterns
    # Left hand pattern and text is reversed, as the test moves away from centre character
    # If all 3 tests match, return the index of the remainder of the word, and the
    # phoneme of the matched rule.
    for rule in rules:
        if rule[1]==word[index:index+len(rule[matchPart])]:
            # Found a matching centre pattern
            leftRule = rule[leftPart]
            rightRule = rule[rightPart]
            remainder = index+len(rule[matchPart])
            leftWord = word[:index] # All letters before centre pattern
            rightWord = word[remainder:] # All letters after centre pattern
            # Check for left match and right match
            if lrMatch(leftRule, leftWord) and lrMatch(rightRule, rightWord,right=True):
                return remainder,rule[outPart]
    # Rule not Found        
    print("Error: Can't find rule for '{}' in '{}'".format(word[index],word))
    return index+1,''
            
def lrMatch( pattern, context, right=False ):
    # Pattern matching
    # pattern is the rule to check for, context is the text to left or right of the letter
    # the right flag signifies checking to the right or left of the current letter
    # If checking to the left, the pattern and context are reversed
    # print "{} Pattern:'{}' Context:'{}'".format('Right:' if right else 'Left:',pattern,context)
    if pattern=='':
        # Empty pattern matches any context
        return True
    if not right:
        # left hand rule - reverse pattern and context
        pattern = pattern[::-1]
        context = context[::-1]
    textPos = 0
    for p in pattern:
        # First check for simple text or space
        if p.isalpha() or p=="'" or p==" ":
            if p==context[textPos]:
                textPos = textPos+1
                continue
            else:
                return False
        if p=='#':
            # One or more vowels
            if not isVowel(context[textPos]):
                return False
            textPos = textPos+1
            while isVowel(context[textPos]):
                textPos = textPos+1
        elif p==':':
            # zero or more consonant
            while isConsonant(context[textPos]):
                textPos = textPos+1
        elif p=='^':
            # One consonant
            if not isConsonant(context[textPos]):
                return False
            textPos = textPos+1
        elif p=='.':
            #  B, D, V, G, J, L, M, N, R, W, Z
            if context[textPos] not in "BDVGJLMNRWZ":
                return False
            textPos = textPos+1
        elif p=='+':
            # E, I or Y (front vowel)
            if context[textPos] not in "EIY":
                return False
            textPos = textPos+1
        elif right and p=='%':
            # ER, E, ES, ED, ING, ELY (a suffix)
            # Only used in right hand rules
            if context[textPos:textPos+3] == 'ING' or context[textPos:textPos+3] == 'ERY':
                textPos = textPos+4
            elif context[textPos:textPos+2] == 'ER' or \
                context[textPos:textPos+2] == 'ES' or \
                context[textPos:textPos+2] == 'ED':
                textPos = textPos+3
            elif context[textPos] == 'E':
                textPos = textPos+2
            else:
                return False
        else:
            print("Bad char in {} pattern: '{}'".format('right' if right else 'left',p))
            return False
    return True
         
def translateText( text ):
    # Translate the text and return a list with the phonetic version of the words
    # Each word in the list is a list of phonemes.
    phonemes = []
    for word in text:
        phonemes.append(translateWord( word.upper() ))
    return phonemes

# The NRL phoneme set is a subset of the ones available on the SP0256
# This dictionary maps from IPA to SP0256
NRLIPAtoSPO256 = { 'AA':'AA', 'AE':'AE', 'AH':'AX AX', 'AO':'AO', 'AW':'AW',  'AX':'AX',
                   'AY':'AY', 'b':'BB1', 'CH':'CH',  'd':'DD1', 'DH':'DH1', 'EH':'EH',
                   'ER':'ER1','EY':'EY', 'f':'FF',   'g':'GG2', 'h':'HH1',  'IH':'IH',
                   'IY':'IY', 'j':'JH',  'k':'KK1',  'l':'LL',  'm':'MM',   'n':'NN1',
                   'NG':'NG', 'OW':'OW', 'OY':'OY',  'p':'PP',  'r':'RR1',  's':'SS',
                   'SH':'SH', 't':'TT1', 'TH':'TH',  'UH':'UH',  'UW':'UW2','v':'VV',
                   'w':'WW', 'WH':'WH', 'y':'YY1', 'z':'ZZ', 'ZH':'ZH', 'PAUSE':'PA4' };

def IPAtoSP0256( phonemes ):
    # convert a list of IPA phonemes into SP0256 phonemes
    sp0256 = []
    for phoneme in phonemes:
        if phoneme in NRLIPAtoSPO256:
            sp0256.append(NRLIPAtoSPO256[phoneme])
    return sp0256


def clockSpeed(freq):
    freq = float(freq)
    if freq < 1.0 or freq > 5.1:
        raise argparse.ArgumentTypeError("%r not in range [1.0, 5.1]"%(freq,))
    return freq

parser = argparse.ArgumentParser(description='Simple Text to Speech')
parser.add_argument('-c','--clock', action="store", default='3.12', dest='mhz', type=clockSpeed, help='Clock speed in MHz - range 1.0 to 5.1')
parser.add_argument('-b','--board', action="store", default=0, dest='board', type=int, choices=range(0,4), help='Select retroSpeak device 0-3 - default is 0')
parser.add_argument('-v','--verbose', action="store_const", const=True, default=False, dest='verbose', help='Print allophones')
parser.add_argument('-s','--silent', action="store_const", const=True, default=False, dest='silent', help='Do not speak. Print allophones.')

parser.add_argument('text', metavar='text', nargs=argparse.REMAINDER, help='Text to speak')

args = parser.parse_args()

phonemes = ''
for word in args.text:
    if word.lower() in vocabulary:
        phonemes = phonemes + ' ' + vocabulary[word.lower()]
    else:
        phonemes = phonemes + ' ' + ' '.join(IPAtoSP0256( translateWord(word.upper()) ) )
    phonemes = phonemes + ' PA4'

if args.verbose or args.silent:
    print phonemes

if not(args.silent):
    # Initialise retroSpeak board
    speech = retroSpeak.retroSpeak(clock=args.mhz,device=args.board)
    speech.speakAndWait(phonemes)



