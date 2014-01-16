'''
Created on Jan 4, 2014

@author: ramnatthan
'''
#!/usr/bin/env python
import lmdb

env = lmdb.open('/home/ramnatthan/code/adsl-work/ALC/mdb/databases', max_dbs = 1)
print env.stat()

mydb = env.open_db('mydatabase')

env.close()
print 'Done'



