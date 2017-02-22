# -*- coding: utf-8 -*-
import re
import raceman.lib.config as config

_SECONDSMS=1000
_MINUTESMS=60*_SECONDSMS
_HOURSMS=60*_MINUTESMS

DATEMATCH=re.compile("(?P<sign>\+|-)?((?P<hours>\d{1,2}?):)?((?P<minutes>\d{1,2}?)?:)?(?P<seconds>\d{1,22}?)\.(?P<ms>\d{3}?)\Z")



def partstoint(hours=0,minutes=0,seconds=0,ms=0,sign=1):
	return (int(hours)*_HOURSMS+int(minutes)*_MINUTESMS+int(seconds)*_SECONDSMS+int(ms))*int(sign)


def dictattr(dic,att,default=None):
	if (att in dic) and (dic[att]):
		return dic[att]
	else:
		if default is not None:
			return default
		else:
			raise AttributeError("%s is not in dictionary %s and no default (%s)" % (att,dic,default))
      


class RacingTime(object):
	def __init__(self):
		self._inttime=None
		self._sign=1

	@classmethod
	def fromstr(cls,str):
		match = DATEMATCH.match(str)
		if match:
			if dictattr(match.groupdict(),'sign',"+")=="-":
				sign=-1
			else:
				sign=1
			inttime=partstoint(hours=dictattr(match.groupdict(),'hours',0),
			minutes=dictattr(match.groupdict(),'minutes',0),
			seconds=dictattr(match.groupdict(),'seconds',0),
			ms=dictattr(match.groupdict(),'ms',0),sign=sign)
			c=cls()
			c._inttime=inttime
			return c
		else:
			raise ValueError("Cannot convert string %s to RacingTime" % str)
      
      
	@classmethod
	def fromint(cls,intval):
		i=int(intval)
		c=cls()
		c._inttime=i
		return c
    
    
    
	@classmethod
	def fromparts(cls,hours=0,minutes=0,seconds=0,ms=0,sign=1):
		i=partstoint(hours,minutes,seconds,ms,sign)
		c=cls()
		c._inttime=i
		return c


	def digits(self,a,digits):
		divs=float(pow(10,3-digits))
		return int(round(float(a)/divs))
    

    
	def __add__(self,other):
		return RacingTime.fromint(self._inttime+other._inttime)
    
	def __sub__(self,other):
		return RacingTime.fromint(self._inttime-other._inttime)
		
	def __div__(self,other):
		return RacingTime.fromint(self._inttime/other)
    
	def __cmp__(self,other):
		return self._inttime.__cmp__(other._inttime)      
    
	def hour(self):
		return abs(self._inttime)/_HOURSMS
      
	def minute(self):
		return abs(self._inttime) % _HOURSMS / _MINUTESMS
      
	def second(self):
		return abs(self._inttime) % _HOURSMS % _MINUTESMS / _SECONDSMS
      
	def ms(self):
		return abs(self._inttime) % _HOURSMS % _MINUTESMS % _SECONDSMS
    
	def sign(self, force=False):
		if self._inttime>0 and not  force:
			return ""
		else:
			if self._inttime<0:
				return "-"
			else:
				return "+"

	def tostr(self, compact=False,forcesign=False,tosay=False,digits=3):
		if not tosay:
			d1=":"
			d2="."
		else:
			d1="  "
			d2="  "
		if not compact:
			return ("%s%02d" + d1 + "%02d" + d1 + "%02d" + d2 + "%0"+str(digits)+"d") % (self.sign(forcesign),self.hour(),self.minute(),self.second(),self.ms())
		else:			
			ms=self.digits(self.ms(),digits)
			if tosay and ms<pow(10,digits-1):
				if ms<pow(10,digits-2):
					_ms=(("0" +d2)*(digits-1) + "%1d") %ms
				else:
					_ms=("0" +d2 + "%2d") % ms			
			else:
				_ms=("%0"+str(digits)+"d") % ms
			ret=("%d" + d2 + "%s") % (self.second(),_ms)
			if self.minute()<>0 or self.hour()<>0:
				ret=("%d" + d1 +"%s") % (self.minute(),ret)
			if self.hour()<>0:
				ret=("%d" + d1 + "%s") % (self.hour(),ret)
			ret=self.sign(forcesign)+ret
			return ret
      
    
	def __str__(self):
		return self.tostr()

	def __repr__(self):
		return super(RacingTime,self).__repr__()+ " ["+ self.__str__()+ "]"
    
	def todict(self,compact=False,forcesign=False):
		dic=dict()
		if compact:
			repr2="%02d"
			repr3="%03d"
		else:
			repr2="%d"
			repr3="%03d"
    
		dic['ms']=repr3 % self.ms()
		dic['second']=repr2  % self.second()

		if self.minute()<>0 or self.hour()<>0 or not compact:
			dic['minute']=repr2 % self.minute()
      
		if self.hour()<>0 or not compact:
			dic['hour']=repr2  % self.hour()
      
		sign=self.sign(forcesign)
		if sign:
			dic['sign']=sign
		return dic
          
	def round(self,precision, optimistic=True):
		if precision<3:
			if optimistic:
				return RacingTime.fromint(int(str(self._inttime)[:-(3-precision)]+"0"*(3-precision)))
			else:
				return RacingTime.fromint(int(round(float(self._inttime)/1000.0,precision)*1000.0))
			
		
	def say_list(self, complete=False):
	
		words={1:'TENTH',2:'HUNDREDTH',3:'THOUSANDTH'}
		result=[]
		metric=3
		ms=self.ms()
		
		while ms%10==0 and ms>0:
			ms=ms/10
			metric-=1
		
		if self.hour()<>0:
			result=spell(self.hour(),'HOUR')
			
		if self.minute()<>0 or self.hour()<>0:
			result+=spell(self.minute(),'MINUTE')
		
		result+=spell(self.second(),'SECOND')
		
		if ms==0:
			if complete:
				return result
			else:
				result=result[:-1]
				result+=[u"РОВНО"]
		else:	
			result=result[:-1]		

			if len(str(ms))==metric and not complete:
				if metric==1:
					result+=[u"И"]
				result+= spell(ms,words[metric])[:-1]
			else:
				result+=[u"И"]
				result+= spell(ms,words[metric])
			if complete:
				result+=[u"СЕКУНДЫ"]
		return result
		
	def say(self,complete=False):
		return " ".join(self.say_list(complete))
			
        

