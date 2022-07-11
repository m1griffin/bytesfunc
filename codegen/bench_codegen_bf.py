#!/usr/bin/python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the code for benchmark tests for 'bytesfunc' functions.
# Language: Python 3.5
# Date:     25-May-2021
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

# ==============================================================================

import glob
import os.path
import datetime

# ==============================================================================



# This goes at the top of the generated file.
headertemplate = '''#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   %(testfilename)s
# Purpose:  Benchmark tests for 'bytesfunc' functions.
# Language: Python 3.5
# Date:     01-Nov-2019.
# Ver:      %(verdate)s.
#
###############################################################################
#
#   Copyright 2014 - %(cpyear)s    Michael Griffin    <m12.griffin@gmail.com>
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
	xdata = %(test_op_x)s

	arraydata.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), arraysize)))
	assert len(arraydata.datax) == arraysize, 'datax is not expected length %%d' %% len(arraydata.datax)

	arraydata.arraylength = len(arraydata.datax)

	# Those functions which need a second parameter are given a single value for this benchmark.
	arraydata.yvalue = %(test_op_yval)s

	# Output data.
	arraydata.dataout = bytearray(list(itertools.repeat(0, arraysize)))
	assert len(arraydata.dataout) == arraysize, 'dataout is not expected length %%d' %% len(arraydata.dataout)


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
		%(pyequ)s

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
		%(bytesfuncequ)s
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
		%(bytesfuncequnosimd)s
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
		%(bytesfuncequsimd)s
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
		'x86_64' : %(x86_simd)s,
		'armv7l' : %(armv7_simd)s,
		'aarch64' : %(armv8_simd)s,
	}

	return signatures.get(platform.machine(), False)



HasSIMD = platformdetect()

##############################################################################

# Run the benchmarks.
funcname = '%(funcname)s'

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
SIMD vs non-SIMD:       %%s
====================== ===========
""" %% simdformat



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

'''




# ==============================================================================


# This defines the python code form of the benchmark equations.
pyequ = {
'bmax' : 'result = max(datax)',
'bmin' : 'result = min(datax)',
'bsum' : 'result = sum(datax)',
'ball' : 'result = all(([(x == yvalue) for x in datax]))',
'bany' : 'result = any([(x == yvalue) for x in datax])',
'findindex' : 'result = [x for x,y in enumerate(datax) if y >= yvalue]',
'eq' : 'result = all([x == yvalue for x in datax])',
'ge' : 'result = all([x >= yvalue for x in datax])',
'gt' : 'result = all([x > yvalue for x in datax])',
'le' : 'result = all([x <= yvalue for x in datax])',
'lt' : 'result = all([x < yvalue for x in datax])',
'ne' : 'result = all([x != yvalue for x in datax])',
'and_' : 'result = bytearray( (x & yvalue for x in datax) )',
'or_' : 'result = bytearray( (x | yvalue for x in datax) )',
'xor' : 'result = bytearray( (x ^ yvalue for x in datax) )',
'lshift' : 'result = bytearray( (255 & (x << yvalue) for x in datax) )',
'rshift' : 'result = bytearray( (x >> yvalue for x in datax) )',
'invert' : 'result = bytearray( (255 - x for x in datax) )',
}


# This defines the bytesfunc code form of the benchmark equations.
bytesfuncequ = {
'bsum' : 'result = bytesfunc.bsum(datax)',
'bmax' : 'result = bytesfunc.bmax(datax)',
'bmin' : 'result = bytesfunc.bmin(datax)',
'ball' : 'result = bytesfunc.ball("==", datax, yvalue)',
'bany' : 'result = bytesfunc.bany("==", datax, yvalue)',
'findindex' : 'result = bytesfunc.findindex(">=", datax, yvalue)',
'eq' : 'result = bytesfunc.eq(datax, yvalue)',
'ge' : 'result = bytesfunc.ge(datax, yvalue)',
'gt' : 'result = bytesfunc.gt(datax, yvalue)',
'le' : 'result = bytesfunc.le(datax, yvalue)',
'lt' : 'result = bytesfunc.lt(datax, yvalue)',
'ne' : 'result = bytesfunc.ne(datax, yvalue)',
'and_' : 'bytesfunc.and_(datax, yvalue, dataout)',
'or_' : 'bytesfunc.or_(datax, yvalue, dataout)',
'xor' : 'bytesfunc.xor(datax, yvalue, dataout)',
'lshift' : 'bytesfunc.lshift(datax, yvalue, dataout)',
'rshift' : 'bytesfunc.rshift(datax, yvalue, dataout)',
'invert' : 'bytesfunc.invert(datax, dataout)',
}

# This defines the bytesfunc code form without SIMD of the benchmark equations.
bytesfuncequnosimd = {
'bsum' : 'result = bytesfunc.bsum(datax, nosimd=True)',
'bmax' : 'result = bytesfunc.bmax(datax, nosimd=True)',
'bmin' : 'result = bytesfunc.bmin(datax, nosimd=True)',
'ball' : 'result = bytesfunc.ball("==", datax, yvalue, nosimd=True)',
'bany' : 'result = bytesfunc.bany("==", datax, yvalue, nosimd=True)',
'findindex' : 'result = bytesfunc.findindex(">=", datax, yvalue, nosimd=True)',
'eq' : 'result = bytesfunc.eq(datax, yvalue, nosimd=True)',
'ge' : 'result = bytesfunc.ge(datax, yvalue, nosimd=True)',
'gt' : 'result = bytesfunc.gt(datax, yvalue, nosimd=True)',
'le' : 'result = bytesfunc.le(datax, yvalue, nosimd=True)',
'lt' : 'result = bytesfunc.lt(datax, yvalue, nosimd=True)',
'ne' : 'result = bytesfunc.ne(datax, yvalue, nosimd=True)',
'and_' : 'bytesfunc.and_(datax, yvalue, dataout, nosimd=True)',
'or_' : 'bytesfunc.or_(datax, yvalue, dataout, nosimd=True)',
'xor' : 'bytesfunc.xor(datax, yvalue, dataout, nosimd=True)',
'lshift' : 'bytesfunc.lshift(datax, yvalue, dataout, nosimd=True)',
'rshift' : 'bytesfunc.rshift(datax, yvalue, dataout, nosimd=True)',
'invert' : 'bytesfunc.invert(datax, dataout, nosimd=True)',
}

# This defines the SIMD optimised bytesfunc code form of the benchmark equations.
bytesfuncequsimd = {
'bsum' : 'result = bytesfunc.bsum(datax, nosimd=False)',
'bmax' : 'result = bytesfunc.bmax(datax, nosimd=False)',
'bmin' : 'result = bytesfunc.bmin(datax, nosimd=False)',
'ball' : 'result = bytesfunc.ball("==", datax, yvalue, nosimd=False)',
'bany' : 'result = bytesfunc.bany("==", datax, yvalue, nosimd=False)',
'findindex' : 'result = bytesfunc.findindex(">=", datax, yvalue, nosimd=False)',
'eq' : 'result = bytesfunc.eq(datax, yvalue, nosimd=False)',
'ge' : 'result = bytesfunc.ge(datax, yvalue, nosimd=False)',
'gt' : 'result = bytesfunc.gt(datax, yvalue, nosimd=False)',
'le' : 'result = bytesfunc.le(datax, yvalue, nosimd=False)',
'lt' : 'result = bytesfunc.lt(datax, yvalue, nosimd=False)',
'ne' : 'result = bytesfunc.ne(datax, yvalue, nosimd=False)',
'and_' : 'bytesfunc.and_(datax, yvalue, dataout, nosimd=False)',
'or_' : 'bytesfunc.or_(datax, yvalue, dataout, nosimd=False)',
'xor' : 'bytesfunc.xor(datax, yvalue, dataout, nosimd=False)',
'lshift' : 'bytesfunc.lshift(datax, yvalue, dataout, nosimd=False)',
'rshift' : 'bytesfunc.rshift(datax, yvalue, dataout, nosimd=False)',
'invert' : 'bytesfunc.invert(datax, dataout, nosimd=False)',
}


# ==============================================================================

# This defines how to compare the results of the Python version and bytesfunc version.
# This is used to determine if the two methods are providing the same results.
equationverify = {
'bsum' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'bmax' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'bmin' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'ball' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'bany' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'findindex' : 'assert pyresult[0] == result, "Benchmark results error %s" % self.funcname',
'eq' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'ge' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'gt' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'le' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'lt' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'ne' : 'assert pyresult == result, "Benchmark results error %s" % self.funcname',
'and_' : 'assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname',
'or_' : 'assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname',
'xor' : 'assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname',
'lshift' : 'assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname',
'rshift' : 'assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname',
'invert' : 'assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname',
}


# ==============================================================================


# First data set.
test_op_x = {
'bsum' : list(range(0, 250)),
'bmax' : list(range(0, 250)),
'bmin' : list(range(10, 250)),
'ball' : [125, 125] * 10,
'bany' : list(range(0, 250)),		# Need yvalue at end.
'findindex' : list(range(0, 250)),	# Need yvalue at end.
'eq' : [20, 20] * 10,
'ge' : list(range(10, 250)),
'gt' : list(range(10, 250)),
'le' : list(range(10, 250)),
'lt' : list(range(10, 250)),
'ne' : list(range(10, 250)),
'and_' : list(range(0, 256)),
'or_' : list(range(0, 256)),
'xor' : list(range(0, 256)),
'lshift' : list(range(0, 250)),
'rshift' : list(range(0, 250)),
'invert' : list(range(0, 250)),
}


# Second data value.
test_op_yval = {
'bsum' : 0,
'bmax' : 0,
'bmin' : 0,
'ball' : 125,
'bany' : 255,
'findindex' : 255,
'eq' : 20,
'ge' : 10,
'gt' : 9,
'le' : 250,
'lt' : 251,
'ne' : 5,
'and_' : 15,
'or_' : 15,
'xor' : 15,
'lshift' : 2,
'rshift' : 2,
'invert' : 0,
}



# ==============================================================================


# ==============================================================================

# Read the C function names from the source files.
def GetSourceFileSIMD(filepath, simdname):
	"""Get the names of functions which have SIMD acceleration. This
		works by reading the C source code file names and looking for
		the corresponding SIMD functions. This assumes that the 
		function name follows a specific convention.
		Since there is only one data type we don't have to worry about
		which data types are supported.
		It also searches to see which platforms (CPU types) are 
		supported, again by making assumptions about the function name.
		The C source code files must be in a specific position relative
		to this script.
	Parameters: filepath (string): Get the path defining the source files.
		simdname (string): The string pattern to match to find the
			functions with SIMD support.
		Returns: (list) a list of function names with SIMD support.
	"""
	# Get a list of the SIMD related header files.
	filelist = glob.glob(filepath)
	filelist.sort()

	filedata = []


	for fname in filelist:
		with open(fname, 'r') as f:
			# Search to see if the desired SIMD function is in the file.
			if simdname in f.read():
				# Split the file name from the rest of the path, and then
				# split the file prefix from the file extension ('.c') to
				# get the function name.
				funcname = os.path.split(os.path.basename(fname))[1].split('.')[0]
				filedata.append(funcname)

	return filedata


# ==============================================================================


# Find all the functions with x86 SIMD support.
SIMD_data_x86 = GetSourceFileSIMD('../src/*.c', '_x86_simd')
# Find all the functions with ARMv7 SIMD support.
SIMD_data_armv7 = GetSourceFileSIMD('../src/*.c', '_armv7_simd')
# Find all the functions with ARMv8 SIMD support.
SIMD_data_armv8 = GetSourceFileSIMD('../src/*.c', '_armv8_simd')


# ==============================================================================

# Timestamp to be used on all files created.
testdate = datetime.date.today()
testdatestamp = testdate.strftime('%d-%b-%Y')


# The number and name of each function is derived from the dictionaries above.
for funcname in pyequ.keys():

	filename = 'benchmark_%s.py' % funcname

	with open(filename, 'w') as f:

		op = {
		'testfilename' : filename,
		'verdate' : testdatestamp,
		'cpyear' : testdate.year,

		'funcname' : funcname,

		'test_op_x' : test_op_x[funcname],
		'test_op_yval' : test_op_yval[funcname],
		'pyequ' : pyequ[funcname],
		'bytesfuncequ' : bytesfuncequ[funcname],
		'bytesfuncequnosimd' : bytesfuncequnosimd[funcname],
		'bytesfuncequsimd' : bytesfuncequsimd[funcname],

		'x86_simd' : funcname in SIMD_data_x86,
		'armv7_simd' : funcname in SIMD_data_armv7,
		'armv8_simd' : funcname in SIMD_data_armv8,

		}


		f.write(headertemplate % op)


# ==============================================================================

