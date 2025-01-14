echo off

REM Run all the tests associated with bytesfunc.

SET testname=%1
SET packsource=%2
SET fileprefix=%3

REM Set some default values if none were passed as arguments.
if [%testname%]==[]  SET testname=bytesfunc
if [%packsource%]==[]  SET packsource=unspecified
if [%fileprefix%]==[]  SET fileprefix=unspecified

REM Delete any previous report to avoid appending to it.
del bf_unittest.txt

REM ==============================================================

SET failcount=0

FOR /R %%A IN (test_*.py) DO CALL :pytest %%A

ECHO Testing completed with %failcount% errors.
GOTO :DONE

REM Subroutine pytest =============================================
:pytest
echo "Testing: " %1
python %1 -l
IF ERRORLEVEL 1 SET /A failcount += 1

EXIT /B

REM ==============================================================

:DONE

REM This will collect information about the test environment and then
REM summarize the pass / fail criteria.
python reportunittest.py %testname% %packsource% %fileprefix% bf_unittest.txt > reportunittestresult.txt

type bf_unittest.txt >> reportunittestresult.txt
del bf_unittest.txt
rename reportunittestresult.txt bf_unittest.txt

