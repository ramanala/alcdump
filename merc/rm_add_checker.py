import sys
import subprocess
import os

fo = open('/tmp/short_output','a')
lockwarningpath = '/home/ramnatthan/workload_snapshots/merc/replayed_snapshot/.hg/wlock'

if os.path.exists(lockwarningpath):
    os.remove(lockwarningpath)

fo = open('/tmp/short_output','a')

bashcommand="command=\"hg rm file1 file2 2>&1\"; op=`eval $command`;"
os.system(bashcommand)

bashcommand2="command=\"hg add file5 2>&1\"; echo hello > file5; op=`eval $command`; command2=\"hg commit -m 'File5' -u 'user1'\"; op=`eval $command2`"
os.system(bashcommand2)

bashcommand3="command=\"hg debugstate 2>&1\"; op=`eval $command`; rm -rf /tmp/hgdebugstate; echo $op > /tmp/hgdebugstate"
os.system(bashcommand3)

debug_output = ''
with open('/tmp/hgdebugstate') as fi:
        for line in fi:
            line = line.rstrip('\n')
            debug_output += line


if 'file5' not in debug_output:
    fo.write("RmAddCommit:: File5 add & commit failed")
elif 'file1' in debug_output or 'file2' in debug_output:
    fo.write("RmAddCommit:: File1 and File2 rm failed")
else:
    fo.write("RmAddCommit:: No problem")
    
fo.close()    