# -*- coding:utf-8 -*-
# ИМ-ЕЧ, РД-ЕЧ, РД-МН, ИМ-МН
import pdb
words={
'TRILLION':	[0,	[u'ТРИЛЛИОН',	u'ТРИЛЛИОНА',	u'ТРИЛЛИОНОВ',	u'ТРИЛЛИОНЫ']],
'BILLION':	[0,	[u'МИЛЛИАРД',	u'МИЛЛИАРДА',	u'МИЛЛИАРДОВ',	u'МИЛЛИАРДЫ']],
'MILLION':	[0,	[u'МИЛЛИОН',	u'МИЛЛИОНА',	u'МИЛЛИОНОВ',	u'МИЛЛИОНЫ']],
'THOUSAND' :	[1,	[u'ТЫСЯЧА', 	u'ТЫСЯЧИ',	u'ТЫСЯЧ',    	u'ТЫСЯЧИ']],
'SECOND':	[1,	[u'СЕКУНДА',	u'СЕКУНДЫ',	u'СЕКУНД',   	u'СЕКУНДЫ']],
'MINUTE' :	[1,	[u'МИНУТА', 	u'МИНУТЫ',	u'МИНУТ',    	u'МИНУТЫ']],
'HOUR':   	[0,	[u'ЧАС',		u'ЧАСА',		u'ЧАСОВ',	u'ЧАСЫ']],
'TENTH':	[1,	[u'ДЕСЯТАЯ',	u'ДЕСЯТОЙ',	u'ДЕСЯТЫХ',	u'ДЕСЯТЫЕ']],
'HUNDREDTH':	[1,	[u'СОТАЯ',	u'СОТОЙ',	u'СОТЫХ',	u'СОТЫЕ']],
'THOUSANDTH':	[1,	[u'ТЫСЯЧНАЯ',	u'ТЫСЯЧНОЙ',	u'ТЫСЯЧНЫХ',	u'ТЫСЯЧНЫЕ']],
'LAP':		[0,	[u'КРУГ',	u'КРУГА',	u'КРУГОВ',	u'КРУГИ']]
}

wordforms  = [[2,0,1,1,1],[2,0,3,3,3]]

numbers = {
0:[u'НОЛЬ', u'НОЛЬ'],
1:[u'ОДИН', u'ОДНА'],
2:[u'ДВА', u'ДВЕ'],
3:[u'ТРИ', u'ТРИ'],
4:[u'ЧЕТЫРЕ', u'ЧЕТЫРЕ'],
5:[u'ПЯТЬ', u'ПЯТЬ'],
6:[u'ШЕСТЬ', u'ШЕСТЬ'],
7:[u'СЕМЬ', u'СЕМЬ'],
8:[u'ВОСЕМЬ', u'ВОСЕМЬ'],
9:[u'ДЕВЯТЬ', u'ДЕВЯТЬ'],
10:[u'ДЕСЯТЬ', u'ДЕСЯТЬ'],
11:[u'ОДИННАДЦАТЬ',u'ОДИННАДЦАТЬ'],
12:[u'ДВЕНАДЦАТЬ', u'ДВЕНАДЦАТЬ'],
13:[u'ТРИНАДЦАТЬ', u'ТРИНАДЦАТЬ'],
14:[u'ЧЕТЫРНАДЦАТЬ',u'ЧЕТЫРНАДЦАТЬ'],
15:[u'ПЯТНАДЦАТЬ', u'ПЯТНАДЦАТЬ'],
16:[u'ШЕСТНАДЦАТЬ', u'ШЕСТНАДЦАТЬ'],
17:[u'СЕМНАДЦАТЬ', u'СЕМНАДЦАТЬ'],
18:[u'ВОСЕМНАДЦАТЬ', u'ВОСЕМНАДЦАТЬ'],
19:[u'ДЕВЯТНАДЦАТЬ', u'ДЕВЯТНАДЦАТЬ'],
20:[u'ДВАДЦАТЬ', u'ДВАДЦАТЬ'],
30:[u'ТРИДЦАТЬ', u'ТРИДЦАТЬ'],
40:[u'СОРОК', u'СОРОК'],
50:[u'ПЯТЬДЕСЯТ', u'ПЯТЬДЕСЯТ'],
60:[u'ШЕСТЬДЕСЯТ',u'ШЕСТЬДЕСЯТ'],
70:[u'СЕМЬДЕСЯТ', u'СЕМЬДЕСЯТ'],
80:[u'ВОСЕМЬДЕСЯТ', u'ВОСЕМЬДЕСЯТ'],
90:[u'ДЕВЯНОСТО', u'ДЕВЯНОСТО'],
100:[u'СТО',u'СТО'],
200:[u'ДВЕСТИ', u'ДВЕСТИ'],
300:[u'ТРИСТА', u'ТРИСТА'],
400:[u'ЧЕТЫРЕСТА', u'ЧЕТЫРЕСТА'],
500:[u'ПЯТЬСОТ', u'ПЯТЬСОТ'],
600:[u'ШЕСТЬСОТ', u'ШЕСТЬСОТ'],
700:[u'СЕМЬСОТ', u'СЕМЬСОТ'],
800:[u'ВОСЕМЬСОТ', u'ВОСЕМЬСОТ'],
900:[u'ДЕВЯТЬСОТ', u'ДЕВЯТЬСОТ'],
}


def spell1000(number,gender):
    result=number
    resultlist=[]
    lastnumber=0
    for n in sorted(numbers.keys(),reverse=True):
	if n==result:
	    resultlist=resultlist+[numbers[n][gender]]
	    lastnumber=n
	    break
        if n<result:
	    (tmplist,lastnumber)= spell1000(n,gender)
	    resultlist=resultlist+tmplist
	    result=result - n
    return (resultlist,lastnumber)

def spellword1000(number,word=None):
	if word:
		gender=words[word][0]
	else:
		gender=0
	(spelled,form)=spell1000(number,gender)
	if form>4:
		wordform=2
	else:
		wordform=wordforms[gender][form]
	if word:
		return spelled+[words[word][1][wordform]]
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

