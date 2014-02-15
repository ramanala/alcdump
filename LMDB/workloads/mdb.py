#!/usr/bin/env python
from __future__ import with_statement
import lmdb
import time

#writemap =  True, map_async = False, metasync = True)
#map_size = 7*4096
#metasync = False, writemap =  True, map_async = True
#, metasync = True, writemap =  True, map_async = True
env = lmdb.open('/home/ramnatthan/code/adsl-work/ALC/mdb/databases', max_dbs = 1)
print env.stat()

numTxn = 1
numInserts = 2
i = 1

class Timer(object):
    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        # Error handling here
        self.__finish = time.time()

    def duration_in_seconds(self):
        return self.__finish - self.__start

timer = Timer()


txn = env.begin(write=True)

for i in range(1, numInserts+1):
    #print "current value"+ str(i)
    key = 'k' + str(i+1)
    value = 'r' + str(i+1)
    txn.replace(key,value)

txn.commit()

print 'Env stat:'
print env.stat()

env.close()
print 'Done'



