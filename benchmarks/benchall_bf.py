#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   benchall_bf.py
# Purpose:  Run benchmark tests for 'bytesfunc' functions.
# Language: Python 3.5
# Date:     20-Dec-2018.
# Ver:      28-May-2021.
#
###############################################################################
#
#   Copyright 2014 - 2021    Michael Griffin    <m12.griffin@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
##############################################################################

# ==============================================================================

import subprocess
import sys
import glob
import os
import platform
import argparse

import time
import json

# ==============================================================================



##############################################################################
def runbench(funcname, filename, arraysize, runtimetarget, timeout):
	"""This is used to run each individual benchmark.
	"""

	print('Testing %s ... ' % funcname, end = '', flush = True)
	starttime = time.perf_counter()

	try:
		# Older versions of Python (before 3.7) require a different syntax
		# in order to capture output. We use the new syntax, and if that
		# fails we fall back on the old one. The old version can be dropped
		# once we drop support for older versions of Python.
		try:
			result = subprocess.run(
				[sys.executable, filename, '--rawoutput', '--arraysize', '%d' % arraysize, 
						'--runtimetarget', '%.6f' % runtimetarget], 
				capture_output = True, text = True, timeout = timeout
				)
		except TypeError:
			result = subprocess.run(
				[sys.executable, filename, '--rawoutput', '--arraysize', '%d' % arraysize, 
						'--runtimetarget', '%.6f' % runtimetarget], 
				stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, 
				timeout = timeout
				)

		testresult = result.stdout
		testerror = result.stderr
	except subprocess.TimeoutExpired:
		print('Benchmark timed out ... ', end = '', flush = True)
		testresult = dict({})
		testerror = None
		return testresult, False, 'Benchmark timed out ... '

	print('%.2f seconds.' % (time.perf_counter() - starttime))


	# Check if the benchmark returned an error of its own.
	if len(testerror) > 0:
		print('Error in benchmark ...')
		return dict({}), False, testerror

	try:
		testdata = json.loads(testresult)
	except:
		return dict({}), False, 'Json error ...'


	# Check if benchmark ID field is present.
	if not 'benchname' in testdata:
		return dict({}), False, 'unknown benchmark type ...'

	# Check if the benchmark identifies itself correctly as belonging
	# to this project.
	if testdata['benchname'] != 'bytesfunc':
		return dict({}), False, 'invalid benchmark type: %s.' % testdata['benchname']


	return testdata, True, ''


##############################################################################


##############################################################################
def getbenchmarkfiles():
	'''Get a list of the benchmark files.
	'''
	filelist=glob.glob('benchmark_*.py')
	filelist.sort()
	return filelist

##############################################################################

##############################################################################
def fnamesplit(fname):
	''' Split a file name to extract the function name.
	'''
	# Split off file extension. E.g. ('benchmark_aall', '.py')
	rootname = os.path.splitext(fname)[0]
	# The part we want is the function name, which is the second part.
	return rootname.split('_', maxsplit=1)[1]


##############################################################################


def RunBenchmarks(arraysize, runtimetarget, timeout, errordata):
	''' Run all the benchmarks.
	'''

	# Find all the benchmarks in the current directory. The benchmarks are
	# recognised by the file pattern name.
	filelist = getbenchmarkfiles()

	# Convert the list of file names into a list of function and file names.
	funclist = [(fnamesplit(x), x) for x in filelist]

	totalresults = {}

	# Total any errors so we can report on how many there were.
	totalerrors = 0


	# Run the benchmarks, accumulating the data.
	for funcname, filename in funclist:
		testdata, testOK, errorcode = runbench(funcname, filename, arraysize, runtimetarget, timeout)
		if testOK:
			totalresults[funcname] = testdata
		else:
			print('\n\nBenchmark error in %s: \n%s\n\n' % (funcname, errorcode))
			totalresults[funcname] = errordata
			totalerrors += 1



	# Save just the names of the functions to use in the final report.
	funcnamelist = [x for x,y in funclist]

	return totalresults, funcnamelist, totalerrors


##############################################################################


##############################################################################

# Write out the platform data to keep track of what platform the test was run on.
def WritePlatformSignature(f):
	f.write('BytesFunc Benchmarks.\n')
	# test was run on.
	# 'Linux'
	f.write('Operating System: ' + platform.system() + '\n')

	# 'Linux-4.4.0-79-generic-x86_64-with-Ubuntu-16.04-xenial'
	f.write('Platform: ' + platform.platform() + '\n')

	# 'x86_64'
	f.write('Machine: ' + platform.machine() + '\n')

	# ('64bit', 'ELF')
	f.write('Word size: ' + platform.architecture()[0] + '\n')

	# 'GCC 5.4.0 20160609'
	f.write('Compiler: ' + platform.python_compiler() + '\n')

	# '4.4.0-79-generic'
	f.write('Python release: ' + platform.release() + '\n')


##############################################################################

########################################################
def escapename(funcname):
	''' We need to escape any function names ending with an underscore to 
	prevent it being interpreted as a formatting character in restructured
	text input. 
	''' 
	if funcname.endswith('_'):
		return funcname.rstrip('_') + '\\_'
	else:
		return funcname


########################################################
def tomicrosecond(val):
	''' If numeric, convert to microseconds by multiplying by 1,000,000. 
	If None, then return None.
	'''
	if val is None:
		return None
	else:
		return val * 1000000.0


########################################################
def writelinerelerror(f, label1):
	''' Write the error message instead of test results for relative results. 
	'''
	standformat = ' {0:<11}           error                 error\n'
	f.write(standformat.format(label1))


########################################################
def writelinedataerror(f, label1):
	''' Write the error message instead of test results for raw data results. 
	'''
	standformat = ' {0:<11}     error       error     error      error\n'
	f.write(standformat.format(label1))


##############################################################################


# The header for resuls comparing relative results.
RelResultsHeader = '''
Bytesfunc Benchmarks.


Relative Performance - Python Time / Bytesfunc Time.

============ ===================== ======================================
  function    Bytesfunc vs Python   SIMD vs non-SIMD
============ ===================== ======================================
'''

# The result templates. These are for cases without and with SIMD results.
RelResultTemplateNoSIMD = ' {0:<11}' + '{1:>16.1f}'
RelResultTemplate = RelResultTemplateNoSIMD + '      ' + '{2:>16.1f}'


# The end of the table for relative results.
RelResultsFooter = '============ ===================== ======================================'


########################################################
def WriteRelativeResults(f, totalresults, funcnamelist, arraysize):
	'''The relative performance stats in default configuration.
	'''
	f.write(RelResultsHeader)

	numstats = []

	# Go through the list of functions benchmarked. We iterate this way
	# so we can get the results in alphabetical order.
	for func in funcnamelist:
		# Get the results for just this function.
		funcvals = totalresults[func]

		# Escape names with trailing '_' for compatibility with ReST.
		funcesc = escapename(func)

		# Make sure that valid data is present.
		if 'error' not in funcvals:

			pyvals = funcvals['pydata']
			bfvals = funcvals['bfdata']
			simdvals = funcvals['bfdatasimd']
			nosimdvals = funcvals['bfdatanosimd']
			relcalc = pyvals / bfvals
			if simdvals is None:
				f.write(RelResultTemplateNoSIMD.format(funcesc, relcalc) + '\n')
			else:
				f.write(RelResultTemplate.format(funcesc, relcalc, nosimdvals / simdvals) + '\n')
			

			# Accumulate the values for the statistical summary. 
			numstats.append(relcalc)
		else:
			# Write the error string instead.
			writelinerelerror(f, funcesc)


	f.write(RelResultsFooter)

	# Avoid division by zero if all tests fail.
	try:
		avgval = sum(numstats) / len(numstats)
		maxval = max(numstats)
		minval = min(numstats)
	except:
		avgval = 0.0
		maxval = 0.0
		minval = 0.0


	f.write('\n\n\n')
	f.write('=========== ========\n')
	f.write('Stat         Value\n')
	f.write('=========== ========\n')
	f.write('Average:    %0.0f\n' % avgval)
	f.write('Maximum:    %0.0f\n' % maxval)
	f.write('Minimum:    %0.1f\n' % minval)
	f.write('Array size: %d\n' % arraysize)
	f.write('=========== ========\n')



##############################################################################


RawResultsHeader = '''
Time per test iteration in microseconds.

============ ========== =========== ========== ==========================
  function     Python    BytesFunc   Non-SIMD   With SIMD
============ ========== =========== ========== ==========================
'''

# The result templates. These are for cases without and with SIMD results.
RawResultTemplateNoSIMD = ' {0:<11}' + '{1:>10.1f}' + '{2:>11.1f}'
RawResultTemplate = RawResultTemplateNoSIMD + '{3:>11.1f}' + '{4:>11.1f}'

RawResultsFooter = '============ ========== =========== ========== =========================='



########################################################
def WriteAbsResults(f, totalresults, funcnamelist):
	''' Write the absolute raw data results. 
	'''
	f.write(RawResultsHeader)

	# Go through the list of functions benchmarked. We iterate this way
	# so we can get the results in alphabetical order.
	for func in funcnamelist:
		# Get the results for just this function.
		funcvals = totalresults[func]

		# Escape names with trailing '_' for compatibility with ReST.
		funcesc = escapename(func)

		# Make sure that valid data is present.
		if 'error' not in funcvals:

			pyvals = tomicrosecond(funcvals['pydata'])
			bfvals = tomicrosecond(funcvals['bfdata'])
			simdvals = tomicrosecond(funcvals['bfdatasimd'])
			nosimdvals = tomicrosecond(funcvals['bfdatanosimd'])
			if simdvals is None:
				f.write(RawResultTemplateNoSIMD.format(funcesc, pyvals, bfvals) + '\n')
			else:
				f.write(RawResultTemplate.format(funcesc, pyvals, bfvals, nosimdvals, simdvals) + '\n')

		else:
			# Write the string instead.
			writelinedataerror(f, funcesc)


	f.write(RawResultsFooter + '\n')



##############################################################################

def WriteResults(totalresults, funcnamelist, totalerrors, arraysize):
	''' Write the results to a file as a report. 
	'''
	with open('bf_benchmarkdata.txt', 'w') as f:

		f.write(time.ctime() + '\n')

		WritePlatformSignature(f)

		# The total number of tests conducted, and how many errors there were.
		f.write('Total Tests: %d\n' % len(funcnamelist))
		f.write('Total Errors: %d\n' % totalerrors)
		f.write('\n\n')

		# The relative performance stats in default configuration.
		WriteRelativeResults(f, totalresults, funcnamelist, arraysize)

		f.write('\n\n\n')

		WriteAbsResults(f, totalresults, funcnamelist)

		f.write('\n')


##############################################################################

##############################################################################

def GetCmdArguments():
	""" Get any command line arguments. These modify the operation of the program.
			arraysize = Size of the array in elements.
			runtimetarget = The target length of time in seconds to run a benchmark for.
	"""
	arraysize = 100000
	runtimetarget = 0.1
	timeout = 60

	# Get any command line arguments.
	parser = argparse.ArgumentParser()

	# Size of the test arrays.
	parser.add_argument('--arraysize', type = int, default = arraysize, 
		help='Size of test arrays in number of elements.')

	# The length of time to run each benchmark.
	parser.add_argument('--runtimetarget', type = float, default = runtimetarget, 
		help='Target length of time to run each benchmark for.')

	# Individual benchmark timeout in seconds.
	parser.add_argument('--timeout', type = int, default = timeout, 
		help='Timeout in seconds for each benchmark.')


	args = parser.parse_args()

	return args


##############################################################################


CmdArgs = GetCmdArguments()

ArraySize = CmdArgs.arraysize
RunTimeTarget = CmdArgs.runtimetarget
TimeOut = CmdArgs.timeout

##############################################################################


# This is used in place of actual data when there is an error.
ErrorData = {'error' : None}


##############################################################################

print('\n\nStarting BytesFunc benchmarks.\n')

starttime = time.perf_counter()

# Run the benchmarks.
TotalResults, FuncNameList, TotalErrors = RunBenchmarks(ArraySize, RunTimeTarget, TimeOut, ErrorData)

# Write out the results.
WriteResults(TotalResults, FuncNameList, TotalErrors, ArraySize)


print('\nTime to run all benchmarks: %.2f seconds.' % (time.perf_counter() - starttime))
# The total number of tests conducted, and how many errors there were.
print('Total benchmark tests: %d' % len(FuncNameList))
print('Total benchmark errors: %d\n\n' % TotalErrors)


##############################################################################
