#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   benchmark_eq.py
# Purpose:  Benchmark tests for 'bytesfunc' functions.
# Language: Python 3.5
# Date:     01-Nov-2019.
# Ver:      11-Jul-2022.
#
###############################################################################
#
#   Copyright 2014 - 2022    Michael Griffin    <m12.griffin@gmail.com>
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


##############################################################################

import time
import itertools
import math
import platform
import sys
import json
import collections
import argparse

import bytesfunc

##############################################################################



########################################################
def InitDataArrays(funcname, arraysize):
	"""Initialise the data arrays used to run the tests.
	"""
	adata = collections.namedtuple('arraydata', ['datax', 'dataout', 
										'yvalue', 'arraylength'])

	arraydata = adata


	# Ensure the data is in the right format for the array type.
	xdata = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

	arraydata.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), arraysize)))
	assert len(arraydata.datax) == arraysize, 'datax is not expected length %d' % len(arraydata.datax)

	arraydata.arraylength = len(arraydata.datax)

	# Those functions which need a second parameter are given a single value for this benchmark.
	arraydata.yvalue = 20

	# Output data.
	arraydata.dataout = bytearray(list(itertools.repeat(0, arraysize)))
	assert len(arraydata.dataout) == arraysize, 'dataout is not expected length %d' % len(arraydata.dataout)


	# Some tests need a special adjustment to the test data.
	if funcname in ('bany', 'findindex'):
		arraydata.datax[-1] = arraydata.yvalue


	return arraydata



########################################################
def calibrateruntime(arraysize, arraydata, runtimetarget, hassimd):
	"""Calibrate the run time for Python and default bytesfunc.
	"""
	pyitercounts = 1
	bfitercounts = 50
	bfiternosidmcounts = 50


	# First, do a timing calibration run.
	# Python native time.
	pytime = BenchmarkPython(pyitercounts, arraysize, arraydata)

	# bytesfunc time.
	bftime = BenchmarkBF(bfitercounts, arraydata)


	# Now calculate the average execution time and adjust the iterations
	# so that the tests will take approximately 0.1 seconds.
	# The time returned by the benchmark function is per iteration, so 
	# we don't need to adjust for this again.
	pyitercounts = int(runtimetarget / pytime)
	bfitercounts = int(runtimetarget / bftime)

	# Make sure the iteration count is at least 1.
	if pyitercounts < 1:
		pyitercounts = 1
	if bfitercounts < 1:
		bfitercounts = 1


	# bytesfunc time without SIMD for functions with SIMD.
	if hassimd:
		bftimenosimd = BenchmarkBFNoSIMD(bfiternosidmcounts, arraydata)
		bfiternosidmcounts = int(runtimetarget / bftimenosimd)
		if bfiternosidmcounts < 1:
			bfiternosidmcounts = 1
	else:
		bfiternosidmcounts = None


	return pyitercounts, bfitercounts, bfiternosidmcounts


########################################################
def BenchmarkPython(pyitercounts, arraysize, arraydata):
	"""Measure execution time of native Python code.
	"""
	# We provide a local reference to the arrays to make the representation simpler.
	datax = arraydata.datax
	dataout = arraydata.dataout
	yvalue = arraydata.yvalue

	# This is used for some tests only. 
	result = True

	# Time for python.
	starttime = time.perf_counter()

	for x in range(pyitercounts):
		result = all([x == yvalue for x in datax])

	endtime = time.perf_counter()

	pythontime = (endtime - starttime) / pyitercounts

	return pythontime


########################################################
def BenchmarkBF(bfitercounts, arraydata):
	"""Measure execution time for bytesfunc.
	"""
	# This is used for some tests only. 
	result = True

	# We provide a local reference to the arrays to make the representation simpler.
	datax = arraydata.datax
	dataout = arraydata.dataout
	yvalue = arraydata.yvalue


	# Time for bytesfunc version.
	starttime = time.perf_counter()
	for i in range(bfitercounts):
		result = bytesfunc.eq(datax, yvalue)
	endtime = time.perf_counter()

	bftime = (endtime - starttime) / bfitercounts

	return bftime



########################################################
def BenchmarkBFNoSIMD(bfiternosidmcounts, arraydata):
	"""Measure execution time for bytesfunc with SIMD turned off calls.
	"""
	# This is used for some tests only. 
	result = True

	# We provide a local reference to the arrays to make the representation simpler.
	datax = arraydata.datax
	dataout = arraydata.dataout
	yvalue = arraydata.yvalue


	# Time for bytesfunc version.
	starttime = time.perf_counter()
	for i in range(bfiternosidmcounts):
		result = bytesfunc.eq(datax, yvalue, nosimd=True)
	endtime = time.perf_counter()

	bftime = (endtime - starttime) / bfiternosidmcounts

	return bftime



########################################################
def BenchmarkBFSIMD(bfitercounts, arraydata):
	"""Measure execution time for bytesfunc with SIMD.
	"""
	afiternosidmcounts = 50
	# This is used for some tests only. 
	result = True

	# We provide a local reference to the arrays to make the representation simpler.
	datax = arraydata.datax
	dataout = arraydata.dataout
	yvalue = arraydata.yvalue


	# Time for bytesfunc version.
	starttime = time.perf_counter()
	for i in range(bfitercounts):
		result = bytesfunc.eq(datax, yvalue, nosimd=False)
	endtime = time.perf_counter()

	bftime = (endtime - starttime) / bfitercounts

	return bftime


##############################################################################

def GetCmdArguments():
	""" Get any command line arguments. These modify the operation of the program.
			rawoutput = If specified, will output raw data instead of a report.
			arraysize = Size of the array in elements.
			runtimetarget = The target length of time in seconds to run a benchmark for.
	"""
	arraysize = 100000
	runtimetarget = 0.1

	# Get any command line arguments.
	parser = argparse.ArgumentParser()

	# Output just the raw data.
	parser.add_argument('--rawoutput', action = 'store_true', help = 'Output raw data.')

	# Size of the test arrays.
	parser.add_argument('--arraysize', type = int, default = arraysize, 
		help='Size of test arrays in number of elements.')

	# The length of time to run each benchmark.
	parser.add_argument('--runtimetarget', type = float, default = runtimetarget, 
		help='Target length of time to run each benchmark for.')

	args = parser.parse_args()

	return args


##############################################################################


CmdArgs = GetCmdArguments()

ArraySize = CmdArgs.arraysize
RunTimeTarget = CmdArgs.runtimetarget


##############################################################################

# Detect the hardware platform, and assign the correct platform data table to it.
def platformdetect():
	""" Return True if the machine supports SIMD for this function.
	The results will vary depending upon which platform it is running on.
	"""
	# These are the supported options for SIMD. The values depend on
	# the particular function in question.
	# i686 = 32 bit x86, this never has SIMD.
	# x86_64 = 64 bit x86, supported on Linux with GCC only.
	# armv7l = 32 bit ARM, for Raspberry Pi 3 with 32 bit Linux.
	# aarch64 = 64 bit ARM, for Raspberry Pi 3 or 4 with 64 bit Linux.
	# These values were derived from the platform data reported by the benchmark.
	signatures = {
		'i686' : False,
		'x86_64' : True,
		'armv7l' : True,
		'aarch64' : True,
	}

	return signatures.get(platform.machine(), False)



HasSIMD = platformdetect()

##############################################################################

# Run the benchmarks.
funcname = 'eq'

##############################################################################


ArrayData = InitDataArrays(funcname, ArraySize)
pyitercounts, bfitercounts, bfiternosidmcounts = calibrateruntime(ArraySize, ArrayData, RunTimeTarget, HasSIMD)

PyData = BenchmarkPython(pyitercounts, ArraySize, ArrayData)
BfData = BenchmarkBF(bfitercounts, ArrayData)
if HasSIMD:
	BfDataNoSIMD = BenchmarkBFNoSIMD(bfiternosidmcounts, ArrayData)
	BfDataSIMD = BenchmarkBFSIMD(bfitercounts, ArrayData)
	simdratio = BfDataNoSIMD / BfDataSIMD
else:
	BfDataNoSIMD = None
	BfDataSIMD = None
	simdratio = None


##############################################################################

# If the function doesn't support SIMD, then just use a placeholder.
if HasSIMD:
	simdformat = '{2:>8.1f}'
else:
	simdformat = '    N/A'

standalonetemplate = """
Bytesfunc Benchmark.
====================== ===========
Function:               {0:>8}
Bytesfunc vs Python:    {1:>8.1f}
SIMD vs non-SIMD:       %s
====================== ===========
""" % simdformat



# If raw data is requested, output the raw numbers as JSON.
# This will normally be used by a parent process which called this
# benchmark as a child process.
# 'benchname' is used to help identify the benchmark to the "runner".
if CmdArgs.rawoutput:
	# Called by another process, return data as json.
	testresults = {'pydata' : PyData,
					'bfdata' : BfData,
					'bfdatanosimd' : BfDataNoSIMD,
					'bfdatasimd' : BfDataSIMD,
					'benchname' : 'bytesfunc',
					}

	print(json.dumps(testresults))

else:
	# The form of the template decides whether or not to use the third parameter. 
	print(standalonetemplate.format(funcname, (PyData / BfData), simdratio))


##############################################################################

