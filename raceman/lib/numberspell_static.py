# coding=windows-1251
# ��-��, ��-��, ��-��, ��-��
words={
'TRILLION':		['m',	[u'��������',	u'���������',	u'����������',	u'���������']],
'BILLION':		['m',	[u'��������',	u'���������',	u'����������',	u'���������']],
'MILLION':		['m',	[u'�������',	u'��������',	u'���������',	u'��������']],
'THOUSAND' :	['f',	[u'������', 	u'������',	u'�����',    	u'������']],
'SECOND':		['f',	[u'�������',	u'�������',	u'������',   	u'�������']],
'MINUTE' :		['f',	[u'������', 	u'������',	u'�����',    	u'������']],
'HOUR':   		['m',	[u'���',		u'����',		u'�����',	u'����']],
'TENTH':		['f',	[u'�������',	u'�������',	u'�������',	u'�������']],
'HUNDREDTH':	['f',	[u'�����',	u'�����',	u'�����',	u'�����']],
'THOUSANDTH':	['f',	[u'��������',	u'��������',	u'��������',	u'��������']],
'LAP':			['m',	[u'����',	u'�����',	u'������',	u'�����']]
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

	    