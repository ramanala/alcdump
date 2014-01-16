#!/usr/bin/python

import lmdb
import sys


inputdir = sys.argv[1]

print inputdir
env = lmdb.open(inputdir, max_dbs = 1)
print env.stat()

mydb = env.open_db('mydatabase')
print 'Opened Database'

txn = env.begin(db =  mydb, write = True)


print 'Getting value for a key'
val1 = txn.get('key1')
val2 = txn.get('key2')
val3 = txn.get('key3')
print 'This was the value retrieved: ' + str(val1) + ',' + str(val2) + ',' + str(val3)

print 'closing'

env.close()
print 'Done'
