import sys
import os

fo = open('/tmp/short_output','a')
expected_list = []

log_output = ''

with open('/tmp/hglog') as fp:
    for line in fp:
        line = line.rstrip('\n')
        log_output += line


fo.write(log_output)
with open('/tmp/logparams') as fi:
    for line in fi:
    	line = line.rstrip('\n')
    	expected_list.append(line)

        
isProblematic = False if (log_output in expected_list) else True 

if isProblematic:
	fo.write("\nLog::Problematic:-->" + log_output[:100])
else:
	fo.write("\nLog::No problem")
	
fo.close()