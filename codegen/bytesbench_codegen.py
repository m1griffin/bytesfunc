#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the code for benchmark tests for 'bytesfunc' functions.
# Language: Python 3.5
# Date:     02-Nov-2019
#
###############################################################################
#
#   Copyright 2014 - 2020    Michael Griffin    <m12.griffin@gmail.com>
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
# Module:   bytesbench.py
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

import bytesfunc

##############################################################################

# The size of test array to use.
ARRAYSIZE = 100000

# The width of the function name column in the output report.
FCOLWIDTH = 12

# The width of data columns for absolute (actual time) data.
ABSCOLWIDTH=10

# The width of data columns for relative time data.
RELCOLWIDTH=5

##############################################################################

SIMDFuncs_x86 = %(SIMD_data_x86)s

SIMDFuncs_armv7 = %(SIMD_data_armv7)s

SIMDFuncs_armv8 = %(SIMD_data_armv8)s

# Detect the hardware platform, and assign the correct platform data table to it.
if '-armv' in platform.platform():
	SIMDFuncs = SIMDFuncs_armv7
elif '-aarch64' in platform.platform():
	SIMDFuncs = SIMDFuncs_armv8
else:
	SIMDFuncs = SIMDFuncs_x86


##############################################################################

'''



# ==============================================================================

# The basic class template for benchmarking each array type for an operator.
benchmarkclass_template = '''

##############################################################################
class benchmark_%(funcname)s:
	"""Benchmark a math function.
	"""

	########################################################
	def __init__(self):
		"""Initialise.
		"""
		self.pyitercounts = 1
		self.bfitercounts = 1
		self.bfiternosidmcounts = 1
		self.InitResults()
		self.funcname = '%(funcname)s'
		self.runtimetarget = 0.1

		# We need to escape any function names ending with an underscore to 
		# prevent it being interpreted as a formatting character in restructured
		# text input. 
		if self.funcname.endswith('_'):
			self.escfname = self.funcname.rstrip('_') + '\_'
		else:
			self.escfname = self.funcname


	########################################################
	def InitDataArrays(self):
		"""Initialise the data arrays used to run the tests.
		"""
		# Ensure the data is in the right format for the array type.
		xdata = %(test_op_x)s

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %%d' %% len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = %(test_op_yval)s

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %%d' %% len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if '%(funcname)s' in ('bany', 'findindex'):
			self.datax[-1] = self.yvalue



	########################################################
	def InitResults(self):
		"""Initialise the attributes which store the test results.
		"""
		# The actual numbers.
		self.PyDataTime = 0
		self.BfDataTime = 0
		self.BfDataNoSIMDTime = 0
		self.BfDataSIMDTime = 0

		# Relative times.
		self.RelativeTime = 0
		self.RelSIMDTime = 0



	########################################################
	def calibrateruntime(self):
		"""Calibrate the run time.
		"""
		self.pyitercounts = 1
		self.bfitercounts = 50
		self.bfiternosidmcounts = 50

		# First, do a timing calibration run.
		# Python native time.
		pytime = self.BenchmarkPython()

		# bytesfunc time.
		bftime = self.BenchmarkBF()


		# Now calculate the average execution time and adjust the iterations
		# so that the tests will take approximately 0.1 seconds.
		# The time returned by the benchmark function is per iteration, so 
		# we don't need to adjust for this again.
		self.pyitercounts = int(self.runtimetarget / pytime)
		self.bfitercounts = int(self.runtimetarget / bftime)

		# Make sure the iteration count is at least 1.
		if self.pyitercounts < 1:
			self.pyitercounts = 1
		if self.bfitercounts < 1:
			self.bfitercounts = 1


		# bytesfunc time without SIMD for functions with SIMD.
		if self.funcname in SIMDFuncs:
			bftimenosimd = self.BenchmarkBFNoSIMD()
			self.bfiternosidmcounts = int(self.runtimetarget / bftimenosimd)
			if self.bfiternosidmcounts < 1:
				self.bfiternosidmcounts = 1


	########################################################
	def verifytests(self):
		"""Compare the results of the benchmark equations to ensure the 
		results are comparable.
		"""
		# We provide a local reference to the arrays to make the representation simpler.
		datax = self.datax
		dataout = self.dataout
		yvalue = self.yvalue

		%(pyequ)s
		pyresult = result

		%(bytesfuncequ)s
		%(equationverify)s

		%(bytesfuncequnosimd)s
		%(equationverify)s

		%(bytesfuncequsimd)s
		%(equationverify)s



	########################################################
	def RunTests(self, arraysize):
		"""Run all the tests.
		"""
		self.arraysize = arraysize

		# Test.
		self.InitDataArrays()

		# Run a test to ensure the results from the different tests
		# are comparable. This is intended to discover programming bugs.
		self.verifytests()


		# Calibrate the run time to set the number of test iterations
		# to meet a target test run time.
		self.calibrateruntime()

		# Python native time.
		self.PyDataTime = self.BenchmarkPython()

		# bytesfunc time.
		self.BfDataTime = self.BenchmarkBF()

		# Python execution time relative to Bytesfunc time.
		self.RelativeTime = self.PyDataTime / self.BfDataTime


		# If the function supports SIMD operations, repeat the test
		# with SIMD turned off and on. 
		if self.funcname in SIMDFuncs:
			self.BfDataNoSIMDTime = self.BenchmarkBFNoSIMD()
			self.BfDataSIMDTime = self.BfDataTime

			self.RelSIMDTime = self.BfDataNoSIMDTime / self.BfDataSIMDTime




	########################################################
	def BenchmarkPython(self):
		"""Measure execution time of native Python code.
		"""
		# We provide a local reference to the arrays to make the representation simpler.
		datax = self.datax
		dataout = self.dataout
		yvalue = self.yvalue

		# This is used for some tests only. 
		result = True

		# Time for python.
		starttime = time.perf_counter()

		for x in range(self.pyitercounts):
			%(pyequ)s

		endtime = time.perf_counter()

		pythontime = (endtime - starttime) / self.pyitercounts

		return pythontime


	########################################################
	def BenchmarkBF(self):
		"""Measure execution time for bytesfunc.
		"""
		# This is used for some tests only. 
		result = True

		# We provide a local reference to the arrays to make the representation simpler.
		datax = self.datax
		dataout = self.dataout
		yvalue = self.yvalue


		# Time for bytesfunc version.
		starttime = time.perf_counter()
		for i in range(self.bfitercounts):
			%(bytesfuncequ)s
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime



	########################################################
	def BenchmarkBFNoSIMD(self):
		"""Measure execution time for bytesfunc with SIMD turned off calls.
		"""
		# This is used for some tests only. 
		result = True

		# We provide a local reference to the arrays to make the representation simpler.
		datax = self.datax
		dataout = self.dataout
		yvalue = self.yvalue


		# Time for bytesfunc version.
		starttime = time.perf_counter()
		for i in range(self.bfiternosidmcounts):
			%(bytesfuncequnosimd)s
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfiternosidmcounts

		return aftime



	########################################################
	def BenchmarkBFSIMD(self):
		"""Measure execution time for bytesfunc with SIMD.
		"""
		# This is used for some tests only. 
		result = True

		# We provide a local reference to the arrays to make the representation simpler.
		datax = self.datax
		dataout = self.dataout
		yvalue = self.yvalue


		# Time for bytesfunc version.
		starttime = time.perf_counter()
		for i in range(self.bfitercounts):
			%(bytesfuncequsimd)s
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################
'''


# ==============================================================================

# This accumulate the list of tests to run.
benchclasslisttemplate = """

##############################################################################


BenchClassesAll = [%s]


# Check if specific tests were requested. If so, then perform only those tests.
cmdline = sys.argv

if len(cmdline) > 1:
	BenchClasses = [x for x in BenchClassesAll if x[1] in cmdline]
else:
	BenchClasses = BenchClassesAll


"""

# ==============================================================================



# This is used to run all the tests.
benchruntemplate = '''


##############################################################################

# Write out the platform data to keep track of what platform the test was run on.
def WritePlatformSignature(f):
	f.write('BytesFunc Benchmarks.\\n')
	# test was run on.
	# 'Linux'
	f.write('Operating System: ' + platform.system() + '\\n')

	# 'Linux-4.4.0-79-generic-x86_64-with-Ubuntu-16.04-xenial'
	f.write('Platform: ' + platform.platform() + '\\n')

	# 'x86_64'
	f.write('Machine: ' + platform.machine() + '\\n')

	# ('64bit', 'ELF')
	f.write('Word size: ' + platform.architecture()[0] + '\\n')

	# 'GCC 5.4.0 20160609'
	f.write('Compiler: ' + platform.python_compiler() + '\\n')

	# '4.4.0-79-generic'
	f.write('Python release: ' + platform.release() + '\\n')
	f.write('\\n\\n\\n')



##############################################################################

# Convert seconds to microseconds for display.
def usec(t):
	return t * 1000000.0


##############################################################################

# Relative table.
RelTableSep =  '============ ===================== ======================================'
RelTableHead = '  function    Bytesfunc vs Python   SIMD vs non-SIMD'
RelTableFmt =  ' {0:11}      {1:10.1f}            {2:10.1f}'

# Absolute time table.
AbsTableSep =  '============ ========== =========== ========== =========================='
AbsTableHead = '  function     Python    BytesFunc   Non-SIMD   With SIMD'
AbsTableFmt =  ' {0:11} {1:9.1f} {2:10.1f} {3:10.1f} {4:10.1f}'


##############################################################################

TestReport = []
TestStats = []
RunTime = []

# Run the tests.
for benchcode, funcname in BenchClasses:
	print('Testing %s ... ' % funcname, end = '', flush = True)
	bc = benchcode()
	starttime = time.perf_counter()
	bc.RunTests(ARRAYSIZE)
	print('%.2f seconds.' % (time.perf_counter() - starttime))
	TestReport.append(RelTableFmt.format(bc.escfname, bc.RelativeTime, bc.RelSIMDTime))
	TestStats.append(bc.RelativeTime)
	RunTime.append(AbsTableFmt.format(bc.escfname, usec(bc.PyDataTime), usec(bc.BfDataTime), usec(bc.BfDataNoSIMDTime), usec(bc.BfDataSIMDTime)))



##############################################################################


# Print the results

with open('bf_benchmarkdata.txt', 'w') as f:

	f.write(time.ctime() + '\\n')

	WritePlatformSignature(f)

	f.write('Bytesfunc Benchmarks.\\n\\n\\n')

	##########################################################################

	# The relative performance stats in default configuration.

	f.write('Relative Performance - Python Time / Bytesfunc Time.\\n\\n')
	f.write(RelTableSep + '\\n')
	f.write(RelTableHead + '\\n')
	f.write(RelTableSep + '\\n')
	
	f.write('\\n'.join(TestReport) + '\\n')

	f.write(RelTableSep + '\\n')

	avgval = sum(TestStats) / len(TestStats)
	maxval = max(TestStats)
	minval = min(TestStats)


	f.write('\\n')
	f.write('=========== ========\\n')
	f.write('Stat         Value\\n')
	f.write('=========== ========\\n')
	f.write('Average:    %0.1f\\n' % avgval)
	f.write('Maximum:    %0.1f\\n' % maxval)
	f.write('Minimum:    %0.1f\\n' % minval)
	f.write('Array size: %d\\n' % ARRAYSIZE)
	f.write('=========== ========\\n')



	##########################################################################

	f.write('\\n\\n\\n')

	f.write('Time per test iteration in microseconds.\\n\\n')
	f.write(AbsTableSep + '\\n')
	f.write(AbsTableHead + '\\n')
	f.write(AbsTableSep + '\\n')

	f.write('\\n'.join(RunTime) + '\\n')

	f.write(AbsTableSep + '\\n\\n')


	##########################################################################

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

# This defines the arrayfunc code form without SIMD of the benchmark equations.
bytesfuncequnosimd = {
'bsum' : 'result = bytesfunc.bsum(datax)',
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
'bsum' : 'result = bytesfunc.bsum(datax)',
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

testdate = datetime.date.today()
headerdata = {
'verdate' : testdate.strftime('%d-%b-%Y'),
'cpyear' : testdate.year,
'SIMD_data_x86' : str(SIMD_data_x86),
'SIMD_data_armv7' : str(SIMD_data_armv7),
'SIMD_data_armv8' : str(SIMD_data_armv8),
}

# Output the benchmark.
with open('bytesbench.py', 'w') as f:

	# Header including copyright and imports.
	f.write(headertemplate % headerdata)

	# The individual test classes.
	for funcname in pyequ.keys():
		opvals = {
			'funcname' : funcname,
			'test_op_x' : test_op_x[funcname],
			'test_op_yval' : test_op_yval[funcname],
			'pyequ' : pyequ[funcname],
			'bytesfuncequ' : bytesfuncequ[funcname],
			'bytesfuncequnosimd' : bytesfuncequnosimd[funcname],
			'bytesfuncequsimd' : bytesfuncequsimd[funcname],
			'equationverify' : equationverify[funcname],
		}

		f.write(benchmarkclass_template % opvals)

	# List of function names to run.
	benchclasses = ["(benchmark_%s, '%s')" % (x,x) for x in pyequ.keys()]
	f.write(benchclasslisttemplate % ',\n'.join(benchclasses))


	# Code to run the tests and output the results.
	f.write(benchruntemplate)


# ==============================================================================
