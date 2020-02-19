#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   bytesbench.py
# Purpose:  Benchmark tests for 'bytesfunc' functions.
# Language: Python 3.5
# Date:     01-Nov-2019.
# Ver:      17-Feb-2020.
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

SIMDFuncs_x86 = ['and_', 'ball', 'bany', 'bmax', 'bmin', 'eq', 'findindex', 'ge', 'gt', 'invert', 'le', 'lt', 'ne', 'or_', 'xor']

SIMDFuncs_arm = ['and_', 'ball', 'bany', 'bmax', 'bmin', 'eq', 'findindex', 'ge', 'gt', 'invert', 'le', 'lshift', 'lt', 'ne', 'or_', 'rshift', 'xor']

# Detect the hardware platform, and assign the correct platform data table to it.
if '-armv' in platform.platform():
	SIMDFuncs = SIMDFuncs_arm
else:
	SIMDFuncs = SIMDFuncs_x86


##############################################################################



##############################################################################
class benchmark_bmax:
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
		self.funcname = 'bmax'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 0

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'bmax' in ('bany', 'findindex'):
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

		result = max(datax)
		pyresult = result

		result = bytesfunc.bmax(datax)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bmax(datax, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bmax(datax, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = max(datax)

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
			result = bytesfunc.bmax(datax)
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
			result = bytesfunc.bmax(datax, nosimd=True)
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
			result = bytesfunc.bmax(datax, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_bmin:
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
		self.funcname = 'bmin'
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
		xdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 0

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'bmin' in ('bany', 'findindex'):
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

		result = min(datax)
		pyresult = result

		result = bytesfunc.bmin(datax)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bmin(datax, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bmin(datax, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = min(datax)

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
			result = bytesfunc.bmin(datax)
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
			result = bytesfunc.bmin(datax, nosimd=True)
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
			result = bytesfunc.bmin(datax, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_bsum:
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
		self.funcname = 'bsum'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 0

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'bsum' in ('bany', 'findindex'):
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

		result = sum(datax)
		pyresult = result

		result = bytesfunc.bsum(datax)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bsum(datax)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bsum(datax)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = sum(datax)

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
			result = bytesfunc.bsum(datax)
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
			result = bytesfunc.bsum(datax)
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
			result = bytesfunc.bsum(datax)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_ball:
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
		self.funcname = 'ball'
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
		xdata = [125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 125

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'ball' in ('bany', 'findindex'):
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

		result = all(([(x == yvalue) for x in datax]))
		pyresult = result

		result = bytesfunc.ball("==", datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.ball("==", datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.ball("==", datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all(([(x == yvalue) for x in datax]))

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
			result = bytesfunc.ball("==", datax, yvalue)
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
			result = bytesfunc.ball("==", datax, yvalue, nosimd=True)
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
			result = bytesfunc.ball("==", datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_bany:
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
		self.funcname = 'bany'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 255

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'bany' in ('bany', 'findindex'):
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

		result = any([(x == yvalue) for x in datax])
		pyresult = result

		result = bytesfunc.bany("==", datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bany("==", datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.bany("==", datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = any([(x == yvalue) for x in datax])

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
			result = bytesfunc.bany("==", datax, yvalue)
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
			result = bytesfunc.bany("==", datax, yvalue, nosimd=True)
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
			result = bytesfunc.bany("==", datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_findindex:
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
		self.funcname = 'findindex'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 255

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'findindex' in ('bany', 'findindex'):
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

		result = [x for x,y in enumerate(datax) if y >= yvalue]
		pyresult = result

		result = bytesfunc.findindex(">=", datax, yvalue)
		assert pyresult[0] == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.findindex(">=", datax, yvalue, nosimd=True)
		assert pyresult[0] == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.findindex(">=", datax, yvalue, nosimd=False)
		assert pyresult[0] == result, "Benchmark results error %s" % self.funcname



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
			result = [x for x,y in enumerate(datax) if y >= yvalue]

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
			result = bytesfunc.findindex(">=", datax, yvalue)
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
			result = bytesfunc.findindex(">=", datax, yvalue, nosimd=True)
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
			result = bytesfunc.findindex(">=", datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_eq:
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
		self.funcname = 'eq'
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
		xdata = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 20

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'eq' in ('bany', 'findindex'):
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

		result = all([x == yvalue for x in datax])
		pyresult = result

		result = bytesfunc.eq(datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.eq(datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.eq(datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all([x == yvalue for x in datax])

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
			result = bytesfunc.eq(datax, yvalue)
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
			result = bytesfunc.eq(datax, yvalue, nosimd=True)
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
			result = bytesfunc.eq(datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_ge:
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
		self.funcname = 'ge'
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
		xdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 10

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'ge' in ('bany', 'findindex'):
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

		result = all([x >= yvalue for x in datax])
		pyresult = result

		result = bytesfunc.ge(datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.ge(datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.ge(datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all([x >= yvalue for x in datax])

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
			result = bytesfunc.ge(datax, yvalue)
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
			result = bytesfunc.ge(datax, yvalue, nosimd=True)
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
			result = bytesfunc.ge(datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_gt:
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
		self.funcname = 'gt'
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
		xdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 9

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'gt' in ('bany', 'findindex'):
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

		result = all([x > yvalue for x in datax])
		pyresult = result

		result = bytesfunc.gt(datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.gt(datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.gt(datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all([x > yvalue for x in datax])

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
			result = bytesfunc.gt(datax, yvalue)
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
			result = bytesfunc.gt(datax, yvalue, nosimd=True)
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
			result = bytesfunc.gt(datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_le:
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
		self.funcname = 'le'
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
		xdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 250

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'le' in ('bany', 'findindex'):
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

		result = all([x <= yvalue for x in datax])
		pyresult = result

		result = bytesfunc.le(datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.le(datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.le(datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all([x <= yvalue for x in datax])

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
			result = bytesfunc.le(datax, yvalue)
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
			result = bytesfunc.le(datax, yvalue, nosimd=True)
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
			result = bytesfunc.le(datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_lt:
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
		self.funcname = 'lt'
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
		xdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 251

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'lt' in ('bany', 'findindex'):
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

		result = all([x < yvalue for x in datax])
		pyresult = result

		result = bytesfunc.lt(datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.lt(datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.lt(datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all([x < yvalue for x in datax])

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
			result = bytesfunc.lt(datax, yvalue)
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
			result = bytesfunc.lt(datax, yvalue, nosimd=True)
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
			result = bytesfunc.lt(datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_ne:
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
		self.funcname = 'ne'
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
		xdata = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 5

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'ne' in ('bany', 'findindex'):
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

		result = all([x != yvalue for x in datax])
		pyresult = result

		result = bytesfunc.ne(datax, yvalue)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.ne(datax, yvalue, nosimd=True)
		assert pyresult == result, "Benchmark results error %s" % self.funcname

		result = bytesfunc.ne(datax, yvalue, nosimd=False)
		assert pyresult == result, "Benchmark results error %s" % self.funcname



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
			result = all([x != yvalue for x in datax])

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
			result = bytesfunc.ne(datax, yvalue)
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
			result = bytesfunc.ne(datax, yvalue, nosimd=True)
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
			result = bytesfunc.ne(datax, yvalue, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_and_:
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
		self.funcname = 'and_'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 15

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'and_' in ('bany', 'findindex'):
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

		result = bytearray( (x & yvalue for x in datax) )
		pyresult = result

		bytesfunc.and_(datax, yvalue, dataout)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.and_(datax, yvalue, dataout, nosimd=True)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.and_(datax, yvalue, dataout, nosimd=False)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname



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
			result = bytearray( (x & yvalue for x in datax) )

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
			bytesfunc.and_(datax, yvalue, dataout)
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
			bytesfunc.and_(datax, yvalue, dataout, nosimd=True)
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
			bytesfunc.and_(datax, yvalue, dataout, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_or_:
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
		self.funcname = 'or_'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 15

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'or_' in ('bany', 'findindex'):
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

		result = bytearray( (x | yvalue for x in datax) )
		pyresult = result

		bytesfunc.or_(datax, yvalue, dataout)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.or_(datax, yvalue, dataout, nosimd=True)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.or_(datax, yvalue, dataout, nosimd=False)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname



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
			result = bytearray( (x | yvalue for x in datax) )

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
			bytesfunc.or_(datax, yvalue, dataout)
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
			bytesfunc.or_(datax, yvalue, dataout, nosimd=True)
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
			bytesfunc.or_(datax, yvalue, dataout, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_xor:
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
		self.funcname = 'xor'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 15

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'xor' in ('bany', 'findindex'):
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

		result = bytearray( (x ^ yvalue for x in datax) )
		pyresult = result

		bytesfunc.xor(datax, yvalue, dataout)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.xor(datax, yvalue, dataout, nosimd=True)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.xor(datax, yvalue, dataout, nosimd=False)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname



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
			result = bytearray( (x ^ yvalue for x in datax) )

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
			bytesfunc.xor(datax, yvalue, dataout)
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
			bytesfunc.xor(datax, yvalue, dataout, nosimd=True)
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
			bytesfunc.xor(datax, yvalue, dataout, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_lshift:
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
		self.funcname = 'lshift'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 2

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'lshift' in ('bany', 'findindex'):
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

		result = bytearray( (255 & (x << yvalue) for x in datax) )
		pyresult = result

		bytesfunc.lshift(datax, yvalue, dataout)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.lshift(datax, yvalue, dataout, nosimd=True)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.lshift(datax, yvalue, dataout, nosimd=False)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname



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
			result = bytearray( (255 & (x << yvalue) for x in datax) )

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
			bytesfunc.lshift(datax, yvalue, dataout)
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
			bytesfunc.lshift(datax, yvalue, dataout, nosimd=True)
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
			bytesfunc.lshift(datax, yvalue, dataout, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_rshift:
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
		self.funcname = 'rshift'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 2

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'rshift' in ('bany', 'findindex'):
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

		result = bytearray( (x >> yvalue for x in datax) )
		pyresult = result

		bytesfunc.rshift(datax, yvalue, dataout)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.rshift(datax, yvalue, dataout, nosimd=True)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.rshift(datax, yvalue, dataout, nosimd=False)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname



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
			result = bytearray( (x >> yvalue for x in datax) )

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
			bytesfunc.rshift(datax, yvalue, dataout)
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
			bytesfunc.rshift(datax, yvalue, dataout, nosimd=True)
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
			bytesfunc.rshift(datax, yvalue, dataout, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################
class benchmark_invert:
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
		self.funcname = 'invert'
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
		xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]

		self.datax = bytearray(list(itertools.islice(itertools.cycle(xdata), self.arraysize)))
		assert len(self.datax) == self.arraysize, 'self.datax is not expected length %d' % len(self.datax)

		self.arraylength = len(self.datax)

		# Those functions which need a second parameter are given a single value for this benchmark.
		self.yvalue = 0

		# Output data.
		self.dataout = bytearray(list(itertools.repeat(0, self.arraysize)))
		assert len(self.dataout) == self.arraysize, 'self.dataout is not expected length %d' % len(self.dataout)


		# Some tests need a special adjustment to the test data.
		if 'invert' in ('bany', 'findindex'):
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

		result = bytearray( (255 - x for x in datax) )
		pyresult = result

		bytesfunc.invert(datax, dataout)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.invert(datax, dataout, nosimd=True)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname

		bytesfunc.invert(datax, dataout, nosimd=False)
		assert len([(x,y) for x,y in zip(pyresult, dataout) if x != y]) == 0, "Benchmark results error %s" % self.funcname



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
			result = bytearray( (255 - x for x in datax) )

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
			bytesfunc.invert(datax, dataout)
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
			bytesfunc.invert(datax, dataout, nosimd=True)
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
			bytesfunc.invert(datax, dataout, nosimd=False)
		endtime = time.perf_counter()

		aftime = (endtime - starttime) / self.bfitercounts

		return aftime


##############################################################################


##############################################################################


BenchClassesAll = [(benchmark_bmax, 'bmax'),
(benchmark_bmin, 'bmin'),
(benchmark_bsum, 'bsum'),
(benchmark_ball, 'ball'),
(benchmark_bany, 'bany'),
(benchmark_findindex, 'findindex'),
(benchmark_eq, 'eq'),
(benchmark_ge, 'ge'),
(benchmark_gt, 'gt'),
(benchmark_le, 'le'),
(benchmark_lt, 'lt'),
(benchmark_ne, 'ne'),
(benchmark_and_, 'and_'),
(benchmark_or_, 'or_'),
(benchmark_xor, 'xor'),
(benchmark_lshift, 'lshift'),
(benchmark_rshift, 'rshift'),
(benchmark_invert, 'invert')]


# Check if specific tests were requested. If so, then perform only those tests.
cmdline = sys.argv

if len(cmdline) > 1:
	BenchClasses = [x for x in BenchClassesAll if x[1] in cmdline]
else:
	BenchClasses = BenchClassesAll





##############################################################################

# Write out the platform data to keep track of what platform the test was run on.
def WritePlatformSignature(f):
	# test was run on.
	# 'Linux'
	f.write('Operating System: ' + platform.system() + '\n')

	# 'Linux-4.4.0-79-generic-x86_64-with-Ubuntu-16.04-xenial'
	f.write('Platform: ' + platform.platform() + '\n')

	# ('64bit', 'ELF')
	f.write('Word size: ' + platform.architecture()[0] + '\n')

	# 'GCC 5.4.0 20160609'
	f.write('Compiler: ' + platform.python_compiler() + '\n')

	# '4.4.0-79-generic'
	f.write('Python release: ' + platform.release() + '\n')
	f.write('\n\n\n')



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

with open('bytesbenchmarkdata.txt', 'w') as f:

	f.write(time.ctime() + '\n')

	WritePlatformSignature(f)

	f.write('Bytesfunc Benchmarks.\n\n\n')

	##########################################################################

	# The relative performance stats in default configuration.

	f.write('Relative Performance - Python Time / Bytesfunc Time.\n\n')
	f.write(RelTableSep + '\n')
	f.write(RelTableHead + '\n')
	f.write(RelTableSep + '\n')
	
	f.write('\n'.join(TestReport) + '\n')

	f.write(RelTableSep + '\n')

	avgval = sum(TestStats) / len(TestStats)
	maxval = max(TestStats)
	minval = min(TestStats)


	f.write('\n')
	f.write('=========== ========\n')
	f.write('Stat         Value\n')
	f.write('=========== ========\n')
	f.write('Average:    %0.1f\n' % avgval)
	f.write('Maximum:    %0.1f\n' % maxval)
	f.write('Minimum:    %0.1f\n' % minval)
	f.write('Array size: %d\n' % ARRAYSIZE)
	f.write('=========== ========\n')



	##########################################################################

	f.write('\n\n\n')

	f.write('Time per test iteration in microseconds.\n\n')
	f.write(AbsTableSep + '\n')
	f.write(AbsTableHead + '\n')
	f.write(AbsTableSep + '\n')

	f.write('\n'.join(RunTime) + '\n')

	f.write(AbsTableSep + '\n\n')


	##########################################################################

