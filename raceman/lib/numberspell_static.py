# coding=windows-1251
# ИМ-ЕЧ, РД-ЕЧ, РД-МН, ИМ-МН
words={
'TRILLION':		['m',	[u'ТРИЛЛИОН',	u'ТРИЛЛИОНА',	u'ТРИЛЛИОНОВ',	u'ТРИЛЛИОНЫ']],
'BILLION':		['m',	[u'МИЛЛИАРД',	u'МИЛЛИАРДА',	u'МИЛЛИАРДОВ',	u'МИЛЛИАРДЫ']],
'MILLION':		['m',	[u'МИЛЛИОН',	u'МИЛЛИОНА',	u'МИЛЛИОНОВ',	u'МИЛЛИОНЫ']],
'THOUSAND' :	['f',	[u'ТЫСЯЧА', 	u'ТЫСЯЧИ',	u'ТЫСЯЧ',    	u'ТЫСЯЧИ']],
'SECOND':		['f',	[u'СЕКУНДА',	u'СЕКУНДЫ',	u'СЕКУНД',   	u'СЕКУНДЫ']],
'MINUTE' :		['f',	[u'МИНУТА', 	u'МИНУТЫ',	u'МИНУТ',    	u'МИНУТЫ']],
'HOUR':   		['m',	[u'ЧАС',		u'ЧАСА',		u'ЧАСОВ',	u'ЧАСЫ']],
'TENTH':		['f',	[u'ДЕСЯТАЯ',	u'ДЕСЯТОЙ',	u'ДЕСЯТЫХ',	u'ДЕСЯТЫЕ']],
'HUNDREDTH':	['f',	[u'СОТАЯ',	u'СОТОЙ',	u'СОТЫХ',	u'СОТЫЕ']],
'THOUSANDTH':	['f',	[u'ТЫСЯЧНАЯ',	u'ТЫСЯЧНОЙ',	u'ТЫСЯЧНЫХ',	u'ТЫСЯЧНЫЕ']],
'LAP':			['m',	[u'КРУГ',	u'КРУГА',	u'КРУГОВ',	u'КРУГИ']]
}

wordforms  = {'m':[2,0,1,1,1],'f':[2,0,3,3,3]}


def spell1000(number,gender):
	    return ([("%d-%s-up" % (number,gender))],number%10)

def spellword1000(number,word=None):
	if word:
		gender=words[word][0]
	else:
		gender='m'
	(spelled,form)=spell1000(number,gender)
	if form>4:
		wordform=2
	else:
		wordform=wordforms[gender][form]
	if word:
		return spelled+["%s%s" % (word.lower(),wordform)]
	else:
		return spelled


def spell(number,word=None):
    tempn=number
    result=[]
    
    if (tempn / 1000000000000)>0:
	result=result+spellword1000(tempn/1000000000000,'TRILLION')
	tempn=tempn % 1000000000000
    
    if (tempn / 1000000000)>0:
	result=result+spellword1000(tempn/1000000000,'BILLION')
	tempn=tempn % 1000000000
    
    if (tempn / 1000000)>0:
	result=result+spellword1000(tempn/1000000,'MILLION')
	tempn=tempn % 1000000
    if (tempn / 1000) > 0:
	result=result+spellword1000(tempn/1000,'THOUSAND') 
	tempn=tempn % 1000
    result=result+spellword1000(tempn,word)
    return result

	    