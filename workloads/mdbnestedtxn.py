#!/usr/bin/env python

import lmdb

env = lmdb.open('/home/ramnatthan/code/adsl-work/ALC/mdb/databases', max_dbs = 1)
print env.stat()

mydb = env.open_db('mydatabase')

txn1 = env.begin(db =  mydb, write = True)

i = 1

key = 'key'+(str(i))
value = 'value' + str(i)
print 'Going to put' + str(i)
txn1.put(key, value)
print 'Done update ' + str(i)


i = 1

key = 'key'+(str(i))
value = 'new'+(str(i))
txn2 = env.begin(db =  mydb, parent= txn1, write = True)
print 'Going to put' + str(i)
txn2.replace(key, value)
print 'Done update ' + str(i)


print 'going to abort txn2'
txn2.abort()
print 'abortt done txn2'

valupdated = txn1.get('key1')
print str(valupdated)

print 'going to commit txn1'
txn1.commit()
print 'commit done txn1'




env.close()
print 'Done'



