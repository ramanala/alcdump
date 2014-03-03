replayed_snapshot="$1"
cd $replayed_snapshot

command="hg status 2>&1"
op1=`eval $command`

echo $op1

rm -f /tmp/hgstatus
echo $op1 > /tmp/hgstatus

command="hg log 2>&1"
op2=`eval $command`

echo $op2

rm -f /tmp/hglog
echo $op2 > /tmp/hglog

# we need to remove lock to verify
rm -f ./.hg/store/lock

command="hg verify 2>&1"
op3=`eval $command`

echo $op3

rm -f /tmp/hgverify
echo $op3 > /tmp/hgverify


rm -f /tmp/short_output

#status checker
python /home/ramnatthan/code/adsl-work/ALC/merc/compare.py

#verify checker
python /home/ramnatthan/code/adsl-work/ALC/merc/verifychecker.py

#log and recovery checker
python /home/ramnatthan/code/adsl-work/ALC/merc/compare2.py
python /home/ramnatthan/code/adsl-work/ALC/merc/recoverychecker.py

#rm add checker
python /home/ramnatthan/code/adsl-work/ALC/merc/rm_add_checker.py

#post checker
python /home/ramnatthan/code/adsl-work/ALC/merc/postchecker.py