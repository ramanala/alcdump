#!/usr/bin/python

import lmdb
import sys



# parser = OptionParser(usage="Usage: %prog [options] filename", description="...")
#------------------------------------------------------------------------------
# # example of a proper command line: -b 1 -f '/home/user1/workloads/seq' -w 40 -i 1 -s 1.0 -t 'sequential' -c False
# parser.add_option("-d", "--inputdir", dest="inputdir", type="string", default="",help="Database environment directory that the checker should worry about")
#------------------------------------------------------------------------------
#----------------------------------------- (options, args) = parser.parse_args()

#initialize local from command args
inputdir = sys.argv[1]

print inputdir
env = lmdb.open(inputdir, max_dbs = 1)
print env.stat()

#mydb = env.open_db('mydatabase')
#print 'Opened Database'

txn = env.begin(write = False)

numInserts = 4

for i in range(1, numInserts+1):
    key = 'k'+(str(i))
    print txn.get(key)

print 'closing'

env.close()
print 'Done'
