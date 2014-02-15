#!/usr/bin/python

from bsddb3 import db
import shutil
import os
import sys

class BerkeleyDBWorkload:
    def __init__(self, dbLocation, accessMethod, fileName = 'default.db', useEnv = False, cleanupBeforeRun = True, sync = True,
                 useAutoCommit = False):
        self.useEnv = useEnv
        self.dbLocation = dbLocation
        self.fileName = fileName
        self.cleanupBeforeRun = cleanupBeforeRun
        self.sync = sync
        self.accessMethod = accessMethod
        self.useAutoCommit = useAutoCommit


    def GetDBInstance(self):
        self.dbInstance = None
        if(self.useEnv):
            self.env = db.DBEnv()
            self.env.set_lg_max(10*4096)
            self.env.set_tx_max(30)
            self.env.set_flags(db.DB_CREATE | db.DB_NOMMAP , 1)

            print 'opening env'
            #db.DB_THREAD - add this to next line OR to enable multiple threads
            # Should explore - DB_RECOVER and DB_RECOVER_FATAL?
            self.env.open(self.dbLocation, db.DB_CREATE | db.DB_INIT_MPOOL | db.DB_INIT_LOG | db.DB_INIT_TXN | db.DB_INIT_LOCK | db.DB_RECOVER | db.DB_THREAD | db.DB_PRIVATE)
            print 'env opened'

            self.dbInstance = db.DB(self.env)
        else:
            self.dbInstance = db.DB()


        return self.dbInstance


    def Run(self, op, numTuples = 4):

        txn = None
        if op == 'display':

            dbvar = self.GetDBInstance()

            #dbvar.set_flags(db.DB_CHKSUM)

            dbvar.open(self.dbLocation + '/' + self.fileName, None, self.accessMethod, db.DB_CREATE | db.DB_NOMMAP)


            txn = None

            print 'Getting values'
            self.GetAndPrintValues(numTuples, txn)
            print 'Get done'

        self.Close()

    def GetAndPrintValues(self, numPairs, txn):
        proper = True
        isNone = False
        isVal = False

        FAIL = '!!!!!!!!!!!'
        ENDC = '!!!!!!!!!'

        for x in range(1,numPairs+1):

            if self.accessMethod == db.DB_QUEUE:
                rec = self.dbInstance.consume(txn)
                val = rec[1]
            elif self.accessMethod == db.DB_RECNO:
                val = str(self.dbInstance.get(x, txn=txn))
            else:
                val =  str(self.dbInstance.get('k'+str(x), txn=txn))

            print val,

            #Below is dead check :) - Hack.
            if str(val) == 'None':
                isNone = True
                if isVal:
                    proper = False
            else:
                isVal = True
                if isNone:
                    proper = False

        print 'Done'
        if not proper:
            print FAIL + 'There was a problem in consistency gaurantees!!' + ENDC

        os.system("echo " + str(proper) + " > /tmp/short_output")

    def Close(self):

        self.dbInstance.sync()

        self.dbInstance.close()
        print 'Closed DB'

        if self.useEnv:
            self.env.close()
            print 'Close Env'


loc = '/home/ramnatthan/code/adsl-work/ALC/bdb/databases'
#loc = sys.argv[1]
print loc

prevsize = os.path.getsize(loc+'/'+'mydb.db')
workload1 = BerkeleyDBWorkload( dbLocation = loc, accessMethod = db.DB_BTREE,
                                fileName = 'mydb.db', useEnv = True,
                                cleanupBeforeRun = False, sync = False, useAutoCommit = False)

workload1.Run(op = 'display', numTuples = 1200)

currsize = os.path.getsize(loc+'/'+'mydb.db')


print 'Checking if actual recovery happened'

print 'Previous size:' + str(prevsize)
print 'Current size:' + str(currsize)

workload2 = BerkeleyDBWorkload( dbLocation = '/home/ramnatthan/code/adsl-work/ALC/bdb/databases', accessMethod = db.DB_BTREE,
                                fileName = 'mydb.db', useEnv = False,
                                cleanupBeforeRun = False, sync = False, useAutoCommit = True)

workload2.Run(op = 'display', numTuples = 1200)

print 'Done'