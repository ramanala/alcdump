import sys
import subprocess
import os
import filecmp

fo = open('/tmp/short_output','a')

log_expected = []
with open('/tmp/logparams') as fp:
    for line in fp:
    	line = line.rstrip('\n')
    	log_expected.append(line)

log_output = ''
with open('/tmp/hglog') as fp:
    for line in fp:
        line = line.rstrip('\n')
        log_output += line

commit1 = False
commit2 = False
match = False

prob = False

#print 'log_output: ' + log_output
#print 'log_ex[0]: ' + log_expected[0]
#print 'log_ex[1]: ' + log_expected[1]

if log_output == log_expected[0]:
    commit1 = True
    bashcommand="command=\"hg checkout 0 2>&1\"; op=`eval $command`"
    os.system(bashcommand)

    if not filecmp.cmp('file1','/tmp/mercdata/file1'):
        prob = True
        fo.write("\nPostData::Problematic - File1 data not matching")

    if not filecmp.cmp('file2','/tmp/mercdata/file2'):   
        prob = True
        fo.write("\nPostData::Problematic - File2 data not matching")
	
elif log_output == log_expected[1]:
    commit2 = True
    bashcommand="command=\"hg checkout 1 2>&1\"; op=`eval $command`"
    os.system(bashcommand)
	
    if not filecmp.cmp('file1','/tmp/mercdata/file1'):
        prob = True
        fo.write("\nPostData::Problematic - File1 data not matching")

    if not filecmp.cmp('file2','/tmp/mercdata/file2'):   
        prob = True
        fo.write("\nPostData::Problematic - File2 data not matching")
	
    if not filecmp.cmp('file3','/tmp/mercdata/file3'):
        prob = True
        fo.write("\nPostData::Problematic - File3 data not matching")

    if not filecmp.cmp('file4','/tmp/mercdata/file4'):   
        prob = True
        fo.write("\nPostData::Problematic - File4 data not matching")
    
if not prob:
    fo.write("\nPostData:: No problem")

fo.close()
