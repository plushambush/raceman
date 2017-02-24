# coding=windows-1251
# ��-��, ��-��, ��-��, ��-��
words={
'TRILLION':	[0,	[u'��������',	u'���������',	u'����������',	u'���������']],
'BILLION':	[0,	[u'��������',	u'���������',	u'����������',	u'���������']],
'MILLION':	[0,	[u'�������',	u'��������',	u'���������',	u'��������']],
'THOUSAND' :	[1,	[u'������', 	u'������',	u'�����',    	u'������']],
'SECOND':	[1,	[u'�������',	u'�������',	u'������',   	u'�������']],
'MINUTE' :	[1,	[u'������', 	u'������',	u'�����',    	u'������']],
'HOUR':   	[0,	[u'���',		u'����',		u'�����',	u'����']],
'TENTH':	[1,	[u'�������',	u'�������',	u'�������',	u'�������']],
'HUNDREDTH':	[1,	[u'�����',	u'�����',	u'�����',	u'�����']],
'THOUSANDTH':	[1,	[u'��������',	u'��������',	u'��������',	u'��������']],
'LAP':		[0,	[u'����',	u'�����',	u'������',	u'�����']]
}

wordforms  = [[2,0,1,1,1],[2,0,3,3,3]]

numbers = {
0:[u'����', u'����'],
1:[u'����', u'����'],
2:[u'���', u'���'],
3:[u'���', u'���'],
4:[u'������', u'������'],
5:[u'����', u'����'],
6:[u'�����', u'�����'],
7:[u'����', u'����'],
8:[u'������', u'������'],
9:[u'������', u'������'],
10:[u'������', u'������'],
11:[u'�����������',u'�����������'],
12:[u'����������', u'����������'],
13:[u'����������', u'����������'],
14:[u'������������',u'������������'],
15:[u'����������', u'����������'],
16:[u'�����������', u'�����������'],
17:[u'����������', u'����������'],
18:[u'������������', u'������������'],
19:[u'������������', u'������������'],
20:[u'��������', u'��������'],
30:[u'��������', u'��������'],
40:[u'�����', u'�����'],
50:[u'���������', u'���������'],
60:[u'����������',u'����������'],
70:[u'���������', u'���������'],
80:[u'�����������', u'�����������'],
90:[u'���������', u'���������'],
100:[u'���',u'���'],
200:[u'������', u'������'],
300:[u'������', u'������'],
400:[u'���������', u'���������'],
500:[u'�������', u'�������'],
600:[u'��������', u'��������'],
700:[u'�������', u'�������'],
800:[u'���������', u'���������'],
900:[u'���������', u'���������'],
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

def spellword1000(number,word):
    gender=words[word][0]
    (spelled,form)=spell1000(number,gender)
    if form>4:
	wordform=2
    else:
	wordform=wordforms[gender][form]
    return spelled+[words[word][1][wordform]]


def spell(number,word):
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

	    