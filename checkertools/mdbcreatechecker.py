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

env = lmdb.open(inputdir, max_dbs = 1)
print env.stat()

print sys.argv[1]
print 'If you see this then there is no problem'

mydb = env.open_db('mydatabase')

print 'opened database'