#!/usr/bin/env python

import lmdb

env = lmdb.open('/home/ramnatthan/code/adsl-work/ALC/mdb/databases', max_dbs = 1)
print env.stat()

mydb = env.open_db('mydatabase')


numInserts = 200

for i in range(1, numInserts+1):
    txn = env.begin(db =  mydb, write = True)
    key = 'key'+(str(i))
    value = 'value' + str(i)
    print 'Going to put' + str(i)
    txn.put(key, value)
    print 'Done update ' + str(i)
    print 'going to commit'
    txn.commit()
    print 'commit done'

env.close()
print 'Done'



