#!/usr/bin/env python

import lmdb, sys
import traceback

try:
    print 'Opening env'

    env = lmdb.open(sys.argv[1], max_dbs = 1)
    print 'opened env'

    print env.stat()


    env.close()
    print 'Done'
except:
    #Any exception should show up in the results window. So just print it and raise.
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print ''.join('!! ' + line for line in lines)


