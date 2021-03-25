#!/bin/sh

# Run all the unit tests associated with Bytesfunc.

# Get the command line arguments.
testname=$1
packsource=$2
fileprefix=$3
# Test library version.
bf_version=$( pip3 show bytesfunc | grep Version | cut -d: -f2)

# This program resets the test log file and inserts a time stamp and
# information about the test platform in the top of the file.
./unit-test-timestamp.py $testname $packsource $fileprefix $bf_version


# Time at which the test sequence started.
starttime=$(date '+%s')

failcount=0
for utest in `ls test_*.py`

do
	# Construct the test to run.
	CMD="./"$utest
	echo "Testing: " $CMD
	# Run the test.
	$CMD -l
	result=$?
	# Speak a failure message, and count up how many failures.
	if [ "$result" -ne 0 ]
	then 
		failcount=$(($failcount + 1))
	fi

done

# Time at which the test sequence completed.
endtime=$(date '+%s')
elapsedtime=$(($endtime - $starttime))

# Indicate whether a test failed or not.
if [ $failcount -ne 0 ]
then 
	echo $failcount " tests failed."
else
	echo "All tests passed in" $elapsedtime "seconds."
fi

