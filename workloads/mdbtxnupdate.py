#!/usr/bin/env python

import lmdb

env = lmdb.open('/home/ramnatthan/code/adsl-work/ALC/mdb/databases', max_dbs = 1)
print env.stat()

mydb = env.open_db('mydatabase')

txn = env.begin(db =  mydb, write = True)
i = 1

key = 'key'+(str(i))
value = 'new' + str(i)
print 'Going to put' + str(i)
txn.replace(key, value)
print 'Done update ' + str(i)

i = 2

key = 'key'+(str(i))
value = 'new' + str(i)
print 'Going to put' + str(i)
txn.replace(key, value)
print 'Done update ' + str(i)

print 'going to commit'
txn.commit()
print 'commit done'


env.close()
print 'Done'



