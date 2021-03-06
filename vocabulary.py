#!/usr/bin/env python
#********************
# retroSpeak vocabulary
# retroSpeak is a Raspberry Pi controlled speech synthesizer using the vintage 
# SP0256-AL2 chip, and MCP23S17 SPI controlled port expander.
#
# Vocabulary based on example wordlists in the Archer/Radioshack SP0256 datasheet
# with typos corrected and a few additions - it's a slightly quirky list, 
# extended to allow creating a speaking calendar/clock
#
# The datasheet is available here: http://www.cpcwiki.eu/imgs/3/35/Sp0256al2_datasheet.pdf
#
# vocabulary is a simple Python dictionary
#
# To use it, simply import vocabulary into your Python script, and get the allophones for
# the words by using something like word=vocabulary['cognitive']
# 
# Also a dictionary of numbers is available so num=numbers[1] will return the allophones for 'one'
# daysOfMonth[1] will return allophones for 'first' and daysOfMonth[31] 'thirty first'
# daysOfWeek[0] will return allophones for 'monday' and daysOfWeek[6] 'sunday'
# 
# As this is based heavily on work in the public domain work, this code is relased as public domain.
#
#********************

vocabulary = {
    'a':'EY',
    'alarm':'AX LL AR MM',
    'am':'AE AE PA2 MM',
    'and':'AE AE NN1 PA2 DD1',
    'april':'EY PA3 PP RR2 IH IH LL',
    'ate':'EY PA3 TT2',
    'august':'AO AO PA2 GG2 AX SS PA3 TT1',
    'b':'BB2 IY',
    'bathe':'BB2 EY DH2',
    'bather':'BB2 EY DH2 ER1',
    'bathing':'BB2 EY DH2 IH NG',
    'beer':'BB2 YR',
    'bread':'BB1 RR2 EH EH PA1 DD1',
    'by':'BB2 AA AY',
    'c':'SS SS IY',
    'calendar':'KK1 AE AE LL EH NN1 PA2 DD2 ER1',
    'check':'CH EH EH PA3 KK2',
    'checked':'CH EH EH PA3 KK2 PA2 TT2',
    'checker':'CH EH EH PA3 KK1 ER1',
    'checkers':'CH EH EH PA3 KK1 ER1 ZZ',
    'checking':'CH EH EH PA3 KK1 IH NG',
    'checks':'CH EH EH PA3 KK1 SS',
    'clock':'KK1 LL AA AA PA3 KK2',
    'clown':'KK1 LL AW NN1',
    'cognitive':'KK3 AA AA GG3 NN1 IH PA3 TT2 IH VV',
    'collide':'KK3 AX LL AY DD1',
    'computer':'KK1 AX MM PP YY1 UW1 TT2 ER1',
    'cookie':'KK3 UH KK1 IY',
    'coop':'KK3 UW2 PA3 PP',
    'correct':'KK1 ER2 EH EH PA2 KK2 PA2 TT1',
    'corrected':'KK1 ER2 EH EH PA2 KK2 PA2 TT2 IH PA2 DD1',
    'correcting':'KK1 ER2 EH EH PA2 KK2 PA2 TT2 IH NG',
    'corrects':'KK1 ER2 EH EH PA2 KK2 PA2 TT1 SS',
    'crown':'KK1 RR2 AW NN1',
    'd':'DD2 IY',
    'date':'DD2 EY PA3 TT2',
    'daughter':'DD2 AO TT2 ER1',
    'day':'DD2 EH EY',
    'december':'DD2 IY SS SS EH EH MM PA1 BB2 ER1',
    'divided':'DD2 IH VV AY PA2 DD2 IH PA2 DD1',
    'e':'IY',
    'eight':'EY PA3 TT2',
    'eighteen':'EY PA2 PA3 TT2 IY NN1',
    'eighteenth':'EY PA2 PA3 TT2 IY NN1 PA2 TH',
    'eighth':'EY PA3 TT2 PA2 TH',
    'eighty':'EY PA3 TT2 IY',
    'eleven':'IH LL EH EH VV IH NN1',
    'eleventh':'IH LL EH EH VV IH NN1 PA2 TH',
    'emotional':'IY MM OW SH AX NN1 AX EL',
    'engage':'EH EH PA1 NN1 GG1 EY PA2 JH',
    'engagement':'EH EH PA1 NN1 GG1 EY PA2 JH MM EH EH NN1 PA2 PA3 TT2 ',
    'engages':'EH EH PA1 NN1 GG1 EY PA2 JH IH ZZ',
    'engaging':'EH EH PA1 NN1 GG1 EY PA2 JH IH NG',
    'enrage':'EH NN1 RR1 EY PA2 JH',
    'enraged':'EH NN1 RR1 EY PA2 JH PA2 DD1',
    'enrages':'EH NN1 RR1 EY PA2 JH IH ZZ',
    'enraging':'EH NN1 RR1 EY PA2 JH IH NG',
    'equal':'IY PA2 PA3 KK3 WH AX EL',
    'equals':'IY PA2 PA3 KK3 WH AX EL ZZ',
    'error':'EH XR OR',
    'escape':'EH SS SS PA3 KK1 EY PA3 PP',
    'escaped':'EH SS SS PA3 KK1 EY PA3 PP PA2 TT2',
    'escapes':'EH SS SS PA3 KK1 EY PA3 PP ZZ',
    'escaping':'EH SS SS PA3 KK1 EY PA3 PP IH NG',
    'extent':'EH KK1 SS TT2 EH EH NN1 TT2',
    'f':'EH EH FF FF',
    'february':'FF EH EH PA1 BB1 RR2 UW2 XR IY',
    'fifteen':'FF IH FF PA2 PA3 TT2 IY NN1',
    'fifteenth':'FF IH FF PA2 PA3 TT2 IY NN1 PA2 TH',
    'fifth':'FF IH FF FF PA3 TH',
    'fifty':'FF FF IH FF FF PA2 PA3 TT2 IY',
    'fir':'FF ER2',
    'first':'FF ER2 SS PA2 TT2',
    'five':'FF FF AY VV',
    'for':'FF FF OR',
    'fore':'FF FF OR',
    'forty':'FF OR PA3 TT2 IY',
    'four':'FF FF OR',
    'fourteen':'FF OR PA2 PA3 TT2 IY NN1',
    'fourteenth':'FF OR PA2 PA3 TT2 IY NN1 PA2 TH',
    'fourth':'FF FF OR PA2 TH',
    'freeze':'FF FF RR1 IY ZZ',
    'freezer':'FF FF RR1 IY ZZ ER1',
    'freezers':'FF FF RR1 IY ZZ ER1 ZZ',
    'freezing':'FF FF RR1 IY ZZ IH NG',
    'friday':'FF RR2 AY PA2 DD2 EY',
    'frozen':'FF FF RR1 OW ZZ EH NN1',
    'g':'JH IY',
    'gauge':'GG1 EY PA2 JH',
    'gauged':'GG1 EY PA2 JH PA2 DD1',
    'gauges':'GG1 EY PA2 JH IH ZZ',
    'gauging':'GG1 EY PA2 JH IH NG',
    'h':'EY PA2 PA3 CH',
    'hello':'HH1 EH LL AX OW',
    'hour':'AW ER1',
    'hundred':'HH2 AX AX NN1 PA2 DD2 RR2 IH IH PA1 DD1',
    'i':'AA AY',
    'infinitive':'IH NN1 FF FF IH IH NN1 IH PA2 PA3 TT2 IH VV',
    'intrigue':'IH NN1 PA3 TT2 RR2 IY PA1 GG3',
    'intrigued':'IH NN1 PA3 TT2 RR2 IY PA1 GG3 PA2 DD1',
    'intrigues':'IH NN1 PA3 TT2 RR2 IY PA1 GG3 ZZ',
    'intriguing':'IH NN1 PA3 TT2 RR2 IY PA1 GG3 IH NG',
    'investigate':'IH IH NN1 VV EH EH SS PA2 PA3 TT2 IH PA1 GG1 EY PA2 TT2',
    'investigated':'IH IH NN1 VV EH EH SS PA2 PA3 TT2 IH PA1 GG1 EY PA2 TT2 IH PA2 DD1',
    'investigates':'IH IH NN1 VV EH EH SS PA2 PA3 TT2 IH PA1 GG1 EY PA2 TT1 SS',
    'investigating':'IH IH NN1 VV EH EH SS PA2 PA3 TT2 IH PA1 GG1 EY PA2 TT2 IH NG',
    'investigator':'IH IH NN1 VV EH EH SS PA2 PA3 TT2 IH PA1 GG1 EY PA2 TT2 ER1',
    'investigators':'IH IH NN1 VV EH EH SS PA2 PA3 TT2 IH PA1 GG1 EY PA2 TT2 ER1 ZZ',
    'is':'IH IH ZZ',
    'j':'JH EH EY',
    'january':'JH AE AE NN1 YY2 XR IY',
    'july':'JH UW1 LL AY',
    'june':'JH UW2 NN1',
    'k':'KK1 EH EY',
    'key':'KK1 IY',
    'l':'EH EH EL',
    'legislate':'LL EH EH PA2 JH IH SS SS LL EY PA2 PA3 TT2',
    'legislated':'LL EH EH PA2 JH IH SS SS LL EY PA2 PA3 TT2 IH DD1',
    'legislates':'LL EH EH PA2 JH IH SS SS LL EY PA2 PA3 TT1 SS',
    'legislating':'LL EH EH PA2 JH IH SS SS LL EY PA2 PA3 TT2 IH NG',
    'legislature':'LL EH EH PA2 JH IH SS SS LL EY PA2 PA3 CH ER1',
    'letter':'LL EH EH PA3 TT2 ER1',
    'litter':'LL IH IH PA3 TT2 ER1',
    'little':'LL IH IH PA3 TT2 EL',
    'm':'EH EH MM',
    'march':'MM AR PA3 CH',
    'may':'MM EY',
    'memories':'MM EH EH MM ER2 IY ZZ',
    'memory':'MM EH EH MM ER2 IY',
    'million':'MM IH IH LL YY1 AX NN1',
    'minute':'MM IH NN1 IH PA3 TT2',
    'monday':'MM AX AX NN1 PA2 DD2 EY',
    'month':'MM AX NN1 TH',
    'n':'EH EH NN1',
    'nine':'NN1 AA AY NN1',
    'nineteen':'NN1 AY NN1 PA2 PA3 TT2 IY NN1',
    'nineteenth':'NN1 AY NN1 PA2 PA3 TT2 IY NN1 PA2 TH',
    'ninth':'NN1 AY NN1 PA2 TH',
    'ninety':'NN1 AY NN1 PA3 TT2 IY',
    'nip':'NN1 IH IH PA2 PA3 PP',
    'nipped':'NN1 IH IH PA2 PA3 PP PA3 TT2',
    'nipping':'NN1 IH IH PA2 PA3 PP IH NG',
    'nips':'NN1 IH IH PA2 PA3 PP SS',
    'no':'NN2 AX OW',
    'november':'NN2 OW VV EH EH MM PA1 BB2 BB2 ER1',
    'o':'OW',
    'of':'AA AA VV',
    'october':'AA PA2 KK2 PA3 TT2 OW PA1 BB2 ER1',
    'one':'WW AX AX NN1',
    'p':'PP IY',
    'physical':'FF FF IH ZZ IH PA3 KK1 AX EL',
    'pi':'PP AA AA AY',
    'pin':'PP IH IH NN1',
    'pinned':'PP IH IH NN1 PA2 DD1',
    'pinning':'PP IH IH NN1 IH NG',
    'pins':'PP IH IH NN1 ZZ',
    'pledge':'PP LL EH EH PA3 JH',
    'pledged':'PP LL EH EH PA3 JH PA2 DD1',
    'pledges':'PP LL EH EH PA3 JH IH ZZ',
    'pledging':'PP LL EH EH PA3 JH IH NG',
    'plus':'PP LL AX AX SS SS',
    'q':'KK1 YY1 UW2',
    'r':'AR',
    'raspberry':'RR1 AX SS SS PA3 BB1 ER2 RR2 IY',
    'ray':'RR1 EH EY',
    'rays':'RR1 EH EY ZZ',
    'ready':'RR1 EH EH PA1 DD2 IY',
    'red':'RR1 EH EH PA1 DD1',
    'robot':'RR1 OW PA2 BB2 AA PA3 TT2',
    'robots':'RR1 OW PA2 BB2 AA PA3 TT1 SS',
    's':'EH EH SS SS',
    'saturday':'SS SS AE PA3 TT2 ER1 PA2 DD2 EY',
    'score':'SS SS PA3 KK3 OR',
    'second':'SS SS EH PA3 KK1 IH NN1 PA2 DD1',
    'sensitive':'SS SS EH EH NN1 SS SS IH PA2 PA3 TT2 IH VV',
    'sensitivity':'SS SS EH EH NN1 SS SS IH PA2 PA3 TT2 IH VV IH PA2 PA3 TT2 IY',
    'september':'SS SS EH PA3 PP PA3 TT2 EH EH MM PA1 BB2 ER1',
    'seven':'SS SS EH EH VV IH NN1',
    'seventeen':'SS SS EH VV TH NN1 PA2 PA3 TT2 IY NN1',
    'seventeenth':'SS SS EH VV TH NN1 PA2 PA3 TT2 IY NN1 PA2 TH',
    'seventh':'SS SS EH VV TH NN1 PA2 TH',
    'seventy':'SS SS EH VV IH NN1 PA2 PA3 TT2 IY',
    'sincere':'SS SS IH IH NN1 SS SS YR',
    'sincerely':'SS SS IH IH NN1 SS SS YR LL IY',
    'sincerity':'SS SS IH IH NN1 SS SS EH EH RR1 IH PA2 PA3 TT2 IY',
    'sister':'SS SS IH IH SS PA3 TT2 ER1',
    'six':'SS SS IH IH PA3 KK2 SS',
    'sixteen':'SS SS IH PA3 KK2 SS PA2 PA3 TT2 IY NN1',
    'sixteenth':'SS SS IH PA3 KK2 SS PA2 PA3 TT2 IY NN1 PA2 TH',
    'sixth':'SS SS IH PA3 KK2 SS PA2 TH',
    'sixty':'SS SS IH PA3 KK2 SS PA2 PA3 TT2 IY',
    'speak':'SS SS PA3 PP IY PA3 KK2',
    'spell':'SS SS PA3 PP EH EH EL',
    'spelled':'SS SS PA3 PP EH EH EL PA3 DD1',
    'speller':'SS SS PA3 PP EH EH EL ER2',
    'spellers':'SS SS PA3 PP EH EH EL ER2 ZZ',
    'spelling':'SS SS PA3 PP EH EH EL IH NG',
    'spells':'SS SS PA3 PP EH EH EL ZZ',
    'start':'SS SS PA3 TT2 AR PA3 TT2',
    'started':'SS SS PA3 TT2 AR PA3 TT2 IH PA1 DD2',
    'starter':'SS SS PA3 TT2 AR PA3 TT2 ER1',
    'starting':'SS SS PA3 TT2 AR PA3 TT2 IH NG',
    'starts':'SS SS PA3 TT2 AR PA3 TT1 SS',
    'stop':'SS SS PA3 TT1 AA AA PA3 PP',
    'stopped':'SS SS PA3 TT1 AA AA PA3 PP PA3 TT2',
    'stopper':'SS SS PA3 TT1 AA AA PA3 PP ER1',
    'stopping':'SS SS PA3 TT1 AA AA PA3 PP IH NG',
    'stops':'SS SS PA3 TT1 AA AA PA3 PP SS',
    'subject (noun)':'SS SS AX AX PA2 BB1 PA2 JH EH PA3 KK2 PA3 TT2',
    'subject (verb)':'SS SS AX PA2 BB1 PA2 JH EH EH PA3 KK2 PA3 TT2',
    'sunday':'SS SS AX AX NN1 PA2 DD2 EY',
    'sweat':'SS SS WW EH EH PA3 TT2',
    'sweated':'SS SS WW EH EH PA3 TT2 IH PA3 DD1',
    'sweater':'SS SS WW EH EH PA3 TT2 ER1',
    'sweaters':'SS SS WW EH EH PA3 TT2 ER1 ZZ',
    'sweating':'SS SS WW EH EH PA3 TT2 IH NG',
    'sweats':'SS SS WW EH EH PA3 TT2 SS',
    'switch':'SS SS WH IH IH PA3 CH',
    'switched':'SS SS WH IH IH PA3 CH PA3 TT2',
    'switches':'SS SS WH IH IH PA3 CH IH ZZ',
    'switching':'SS SS WH IH IH PA3 CH IH NG',
    'system':'SS SS IH IH SS SS PA3 TT2 EH MM',
    'systems':'SS SS IH IH SS SS PA3 TT2 EH MM ZZ',
    't':'TT2 IY',
    'talk':'TT2 AO AO PA2 KK2',
    'talked':'TT2 AO AO PA3 KK2 PA3 TT2',
    'talker':'TT2 AO AO PA3 KK1 ER1',
    'talkers':'TT2 AO AO PA3 KK1 ER1 ZZ',
    'talking':'TT2 AO AO PA3 KK1 IH NG',
    'talks':'TT2 AO AO PA2 KK2 SS',
    'ten':'TT2 EH EH NN1',
    'tenth':'TT2 EH EH NN1 PA2 TH',
    'the':'DH1 PA3 IY',
    'then':'DH1 EH EH NN1',
    'third':'TH ER1 PA2 DD1',
    'thirteen':'TH ER1 PA2 PA3 TT2 IY NN1',
    'thirteenth':'TH ER1 PA2 PA3 TT2 IY NN1 PA2 TH',
    'thirty':'TH ER2 PA2 PA3 TT2 IY',
    'thirtieth':'TH ER2 PA2 PA3 TT2 IY PA2 EH TH',
    'thousand':'TH AA AW ZZ TH PA1 PA1 NN1 DD1',
    'thread':'TH RR1 EH EH PA2 DD1',
    'threaded':'TH RR1 EH EH PA2 DD2 IH PA2 DD1',
    'threader':'TH RR1 EH EH PA2 DD2 ER1',
    'threaders':'TH RR1 EH EH PA2 DD2 ER1 ZZ',
    'threading':'TH RR1 EH EH PA2 DD2 IH NG',
    'threads':'TH RR1 EH EH PA2 DD2 ZZ',
    'three':'TH RR1 IY',
    'thursday':'TH ER2 ZZ PA2 DD2 EY',
    'time':'TT2 AA AY MM',
    'times':'TT2 AA AY MM ZZ',
    'to':'TT2 UW2',
    'today':'TT2 UW2 PA3 DD2 EY',
    'too':'TT2 UW2',
    'tuesday':'TT2 UW2 ZZ PA2 DD2 EY',
    'twelve':'TT2 WH EH EH LL VV',
    'twelfth':'TT2 WH EH EH LL FF PA2 TH',
    'twenty':'TT2 WH EH EH NN1 PA2 PA3 TT2 IY',
    'twentieth':'TT2 WH EH EH NN1 PA2 PA3 TT2 IY PA2 EH TH',
    'two':'TT2 UW2',
    'u':'YY1 UW2',
    'uncle':'AX NG PA3 KK3 EL',
    'v':'VV IY',
    'w':'DD2 AX PA2 BB2 EL YY1 UW2',
    'wednesday':'WW EH EH NN1 ZZ PA2 DD2 EY',
    'whale':'WW EY EL',
    'whaler':'WW EY LL ER1',
    'whalers':'WW EY LL ER1 ZZ',
    'whales':'WW EY EL ZZ',
    'whaling':'WW EY LL IH NG',
    'won':'WW AX AX NN1',
    'x':'EH EH PA3 KK2 SS SS',
    'y':'WW AY',
    'year':'YY2 YR',
    'yes':'YY2 EH EH SS SS',
    # 'z':'ZZ IY',
    'z':'ZZ EH EH PA2 DD1',#  I'm in the UK! 
    'zero':'ZZ YR OW',
}

daysOfWeek = [
    vocabulary['monday'],vocabulary['tuesday'],vocabulary['wednesday'],
    vocabulary['thursday'],vocabulary['friday'],vocabulary['saturday'],vocabulary['sunday']
    ]

daysOfMonth = [ '',
    vocabulary['first'],vocabulary['second'],vocabulary['third'],
    vocabulary['fourth'],vocabulary['fifth'],vocabulary['sixth'],
    vocabulary['seventh'],vocabulary['eighth'],vocabulary['ninth'],
    vocabulary['tenth'],vocabulary['eleventh'],vocabulary['twelfth'],
    vocabulary['thirteenth'],vocabulary['fourteenth'],vocabulary['fifteenth'],
    vocabulary['sixteenth'],vocabulary['seventeenth'],vocabulary['eighteenth'],
    vocabulary['nineteenth'],vocabulary['twentieth'],
    vocabulary['twenty']+'PA2'+vocabulary['first'],
    vocabulary['twenty']+'PA2'+vocabulary['second'],
    vocabulary['twenty']+'PA2'+vocabulary['third'],
    vocabulary['twenty']+'PA2'+vocabulary['fourth'],
    vocabulary['twenty']+'PA2'+vocabulary['fifth'],
    vocabulary['twenty']+'PA2'+vocabulary['sixth'],
    vocabulary['twenty']+'PA2'+vocabulary['seventh'],
    vocabulary['twenty']+'PA2'+vocabulary['eighth'],
    vocabulary['twenty']+'PA2'+vocabulary['ninth'],
    vocabulary['thirtieth'],
    vocabulary['thirty']+'PA2'+vocabulary['first'] 
    ]

numbers = { 1:vocabulary['one'], 2:vocabulary['two'], 3:vocabulary['three'], 4:vocabulary['four'], 
            5:vocabulary['five'], 6:vocabulary['six'], 7:vocabulary['seven'], 8:vocabulary['eight'], 
            9:vocabulary['nine'], 10:vocabulary['ten'], 11:vocabulary['eleven'], 12:vocabulary['twelve'], 
            13:vocabulary['thirteen'], 14:vocabulary['fourteen'], 15:vocabulary['fifteen'], 16:vocabulary['sixteen'], 
            17:vocabulary['seventeen'], 18:vocabulary['eighteen'], 19:vocabulary['nineteen'], 20:vocabulary['twenty'],
            30:vocabulary['thirty'], 40:vocabulary['forty'], 50:vocabulary['fifty'], 60:vocabulary['sixty'], 
            70:vocabulary['seventy'], 80:vocabulary['eighty'], 90:vocabulary['ninety'], 100:vocabulary['hundred'], 
            1000:vocabulary['thousand'], 1000000:vocabulary['million'] }

