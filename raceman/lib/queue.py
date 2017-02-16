from Queue import Queue
import heapq
import itertools
from raceman.lib.prio import *

class RMQItem(object):
    def __init__(self,value,priority=RM_PRIO_NORMAL,type=None,obsolete=False):
        self.priority=priority
        self.seq=None
        self.value=value
        self.deleted=False
        self.obsolete=obsolete

        if type:
            self.type=type
        else:
            self.type=value.__class__.__name__


    def __cmp__(self,other):
        if self.priority==other.priority:
            return self.seq.__cmp__(other.seq)
        else:
            return self.priority.__cmp__(other.priority)

    def __repr__(self):
        return "[prio:%s seq:%s value:%s type:%s deleted:%s obsoletes:%s]" % (self.priority, self.seq, self.value, self.type, self.deleted, self.obsolete)

class RMQueue(Queue):

    def _init(self, maxsize):
        self._counter=itertools.count()
        self.queue = []

    def _qsize(self, len=len):
        return len(filter(lambda f: not f.deleted,self.queue))

    def _put(self, item, heappush=heapq.heappush):
        if item.obsolete:
            for i in self.queue:
                if item.type==i.type:
                    i.deleted=True

        item.seq=next(self._counter)
        heappush(self.queue, item)

    def _get(self, heappop=heapq.heappop):
        while 1:
            item=heappop(self.queue)
            if item.deleted: 
                continue
            else:
                return item

