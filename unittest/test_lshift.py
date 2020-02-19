#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   test_lshift.py
# Purpose:  bytesfunc unit test.
# Language: Python 3.4
# Date:     26-Jan-2020.
# Ver:      29-Jan-2020.
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
"""This conducts unit tests for lshift.
"""

##############################################################################
import sys

import array
import itertools
import math
import operator
import platform
import copy

import unittest

import bytesfunc

##############################################################################

##############################################################################

# The following code is all auto-generated.


 

##############################################################################
class lshift_general_even_arraysize_nosimd_simd_bytes(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 320

		if 'even' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytes(xdata)
		self.data2 = bytes(ydata)
		self.data3 = bytes(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytes.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_even_arraysize_withsimd_simd_bytes(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 320

		if 'even' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytes(xdata)
		self.data2 = bytes(ydata)
		self.data3 = bytes(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytes.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 )

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_odd_arraysize_nosimd_simd_bytes(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 320

		if 'odd' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytes(xdata)
		self.data2 = bytes(ydata)
		self.data3 = bytes(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytes.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_odd_arraysize_withsimd_simd_bytes(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 320

		if 'odd' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytes(xdata)
		self.data2 = bytes(ydata)
		self.data3 = bytes(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytes.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytes.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytes.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 )

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_even_arraysize_nosimd_simd_bytearray(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 320

		if 'even' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytearray(xdata)
		self.data2 = bytearray(ydata)
		self.data3 = bytearray(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytearray.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_even_arraysize_withsimd_simd_bytearray(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 320

		if 'even' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytearray(xdata)
		self.data2 = bytearray(ydata)
		self.data3 = bytearray(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytearray.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 )

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_odd_arraysize_nosimd_simd_bytearray(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 320

		if 'odd' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytearray(xdata)
		self.data2 = bytearray(ydata)
		self.data3 = bytearray(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited , nosimd=True)

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytearray.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 , nosimd=True)

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

 

##############################################################################
class lshift_general_odd_arraysize_withsimd_simd_bytearray(unittest.TestCase):
	"""Test lshift for basic general function operation.
	test_template_binop_shift
	"""


	########################################################
	def pyshift(self, lop, rop):
		"""Perform a shift operation in Python which produces the same 
		results as native shift operations.
		x86 CPUs do shifts rather peculiarly. For 32 bit arrays and
		smaller, only first 5 bits are used as the amount to shift for
		non-SIMD instructions. This means the shift "rolls over" after 32. 
		For 64 bit arrays, this is 64 bits or larger.
		However, x86 SIMD instructions do not follow this, and ARM is
		different as well.
		As a result of this, this shift function does not attempt to produce
		valid results outside of shift values (rop) beyond the bit length.
		(e.g. 0 - 7, 0 - 15, 0 - 31, 0 - 64)
		"""
		sresult = (lop << rop) & 255
		if sresult > 255:
			sresult = sresult - (255 + 1)
		return sresult


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 320

		if 'odd' == 'odd':
			testdatasize = 319

		paramitersize = 25


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		# All the amounts to shift the first parameter by, limited
		# the the number of bits in the word. We don't test for what
		# happens when we exceed this, as the results on x86 are irregular.
		ydata = list(range(8))
		# This provides the equivalent in the same length as the x array
		# to allow for tests with two input arrays.
		ydatax = list(itertools.islice(itertools.cycle(ydata), testdatasize))

		self.data1 = bytearray(xdata)
		self.data2 = bytearray(ydata)
		self.data3 = bytearray(ydatax)


		# When doing in place calculations, the output must be a bytearray.
		self.data1out = bytearray(xdata)
		self.data2out = bytearray(ydata)
		self.data3out = bytearray(ydatax)
		self.dataout1 = bytearray([0]*len(self.data1))
		self.dataout2 = bytearray([0]*len(self.data2))

		self.limited = len(self.data1) // 2

		# This is used for testing with single parameters. 
		self.data1param = xdata
		self.data2param = ydata



	########################################################
	def test_lshift_basic_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1out)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(datax)[self.limited:]

				bytesfunc.lshift(datax, testval, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datax, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)



	########################################################
	def test_lshift_basic_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for basic function - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				expected = [self.pyshift(x, testval) for x in datax]

				bytesfunc.lshift(datax, testval, self.dataout1 )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data2param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datax = copy.copy(self.data1)

				pydataout = [self.pyshift(x, testval) for x in datax]
				expected = pydataout[0:self.limited] + list(self.dataout1)[self.limited:]

				bytesfunc.lshift(datax, testval, self.dataout1, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout1, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2out)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(datay)[self.limited:]

				bytesfunc.lshift(testval, datay, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(datay, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for basic function - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				expected = [self.pyshift(testval, x) for x in datay]

				bytesfunc.lshift(testval, datay, self.dataout2 )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for basic function with array limit - Array code bytearray.
		"""
		for testval in self.data1param:
			with self.subTest(msg='Failed with parameter', testval = testval):

				# Copy the sequence so we don't change the original data.
				datay = copy.copy(self.data2)

				pydataout = [self.pyshift(testval, x) for x in datay]
				expected = pydataout[0:self.limited] + list(self.dataout2)[self.limited:]

				bytesfunc.lshift(testval, datay, self.dataout2, maxlen=self.limited )

				for dataoutitem, expecteditem in zip(self.dataout2, expected):
					# The behavour of assertEqual is modified by addTypeEqualityFunc.
					self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]

		bytesfunc.lshift(self.data1out, self.data3 )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for basic function with array limit - Array code bytearray.
		"""
		pydataout = [self.pyshift(x, y) for (x, y) in zip(self.data1out, self.data3)]
		expected = pydataout[0:self.limited] + list(self.data1out)[self.limited:]

		bytesfunc.lshift(self.data1out, self.data3, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(self.data1out, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_lshift_basic_array_array_array_e3(self):
		"""Test lshift as *array-array-array* for basic function - Array code bytearray.
		"""
		expected = [self.pyshift(x, y) for (x, y) in zip(self.data1, self.data3)]
		bytesfunc.lshift(self.data1, self.data3, self.dataout1 )

		for dataoutitem, expecteditem in zip(self.dataout1, expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class lshift_param_errors_bytes(unittest.TestCase):
	"""Test lshift for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata1 = [100,101,102,103,104,105,106,107,108,109]
		testdata2 = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), testdata1)]

		arraysize = len(testdata1)

		self.testarray1 = bytes(testdata1)
		self.testarray2 = bytes(testdata2)

		# When doing in place calculations, the output must be a bytearray.
		self.testarray1out = bytearray(testdata1)
		self.testarray2out = bytearray(testdata2)
		self.dataout = bytearray(itertools.repeat(0, arraysize))


		# Create some data array equivalents with an incompatible type.
		self.badarray1 = array.array('d', [float(x) for x in testdata1])
		self.badarray2 = array.array('d', [float(x) for x in testdata2])

		self.baddataout = array.array('d', [float(x) for x in self.dataout])


	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for invalid type of array - Array code bytes.
		"""
		for testvalue in self.testarray2:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1out)
				badarray1 = copy.copy(self.badarray1)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(badarray1, testvalue)


	########################################################
	def test_lshift_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for invalid type of number - Array code bytes.
		"""
		for testvalue, badvalue in zip(self.testarray2, self.badarray2):
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1out)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue)

				testarray1 = copy.copy(self.testarray1out)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testarray1, badvalue)



	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for invalid type of array - Array code bytes.
		"""
		for testvalue in self.testarray2:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1)
				badarray1 = copy.copy(self.badarray1)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(badarray1, testvalue, self.dataout)


	########################################################
	def test_lshift_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for invalid type of number - Array code bytes.
		"""
		for testvalue, badvalue in zip(self.testarray2, self.badarray2):
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):


				# This version is expected to pass.
				bytesfunc.lshift(self.testarray1, testvalue, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(self.testarray1, badvalue, self.dataout)


	########################################################
	def test_lshift_array_num_array_b3(self):
		"""Test lshift as *array-num-array* for invalid type of output array - Array code bytes.
		"""
		for testvalue in self.testarray2:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testarray1, testvalue, self.baddataout)



	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for invalid type of array - Array code bytes.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray2 = copy.copy(self.testarray2out)
				badarray2 = copy.copy(self.badarray2)

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, testarray2)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, badarray2)


	########################################################
	def test_lshift_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for invalid type of number - Array code bytes.
		"""
		for testvalue, badvalue in zip(self.testarray1, self.badarray1):
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray2 = copy.copy(self.testarray2out)

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, testarray2)

				testarray2 = copy.copy(self.testarray2out)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(badvalue, testarray2)



	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for invalid type of array - Array code bytes.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, self.testarray2, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, self.badarray2, self.dataout)


	########################################################
	def test_lshift_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for invalid type of number - Array code bytes.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, self.testarray2, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, self.badarray2, self.dataout)


	########################################################
	def test_lshift_num_array_array_d3(self):
		"""Test lshift as *num-array-array* for invalid type of output array - Array code bytes.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, self.testarray2, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, self.testarray2, self.baddataout)



	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for invalid type of array - Array code bytes.
		"""
		# Copy the sequence so we don't change the original data.
		testarray1 = copy.copy(self.testarray1out)

		# This version is expected to pass.
		bytesfunc.lshift(testarray1, self.testarray2)

		# Copy the sequence so we don't change the original data.
		testarray1out = copy.copy(self.testarray1out)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(testarray1out, self.badarray2)


	########################################################
	def test_lshift_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for invalid type of array - Array code bytes.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1out, self.testarray2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.badarray1, self.testarray2)



	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for invalid type of array - Array code bytes.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1, self.testarray2, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.testarray1, self.badarray2, self.dataout)


	########################################################
	def test_lshift_array_array_array_f2(self):
		"""Test lshift as *array-array-array* for invalid type of array - Array code bytes.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1, self.testarray2, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.badarray1, self.testarray2, self.dataout)


	########################################################
	def test_lshift_array_array_array_f3(self):
		"""Test lshift as *array-array-array* for invalid type of output array - Array code bytes.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1, self.testarray2, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.testarray1, self.testarray2, self.baddataout)


	########################################################
	def test_lshift_no_params_g1(self):
		"""Test lshift with no parameters - Array code bytes.
		"""
		with self.assertRaises(TypeError):
			bytesfunc.lshift()


##############################################################################



##############################################################################
class lshift_opt_param_errors_bytes(unittest.TestCase):
	"""Test lshift for invalid maxlen parameter.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.inpdata1a = [100,101,102,103,104,105,106,107,108,109	]
		self.inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), self.inpdata1a)]

		arraysize = len(self.inpdata1a)
		self.testmaxlen = len(self.inpdata1a) // 2
		self.outpdata = itertools.repeat(0, arraysize)


		self.inparray1a = bytes(self.inpdata1a)
		self.inparray2a = bytes(self.inpdata2a)

		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2b = copy.copy(self.inparray2a)


		# When doing in place calculations, the output must be a bytearray.
		self.inparray1aout = bytearray(self.inpdata1a)
		self.inparray2aout = bytearray(self.inpdata2a)
		self.dataout = bytearray(self.outpdata)

		self.inparray1bout = copy.copy(self.inparray1aout)
		self.inparray2bout = copy.copy(self.inparray2aout)

	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for maxlen='a' - Array code bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, inpvalue, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, inpvalue, maxlen='a')


	########################################################
	def test_lshift_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for matherrors=True (unsupported option) - Array code bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, inpvalue)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, inpvalue, matherrors=True)


	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for maxlen='a' - Array code bytes.
		"""
		# Copy the sequence so we don't change the original data.
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, inpvalue, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, inpvalue, self.dataout, maxlen='a')


	########################################################
	def test_lshift_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for matherrors=True (unsupported option) - Array code bytes.
		"""
		# Copy the sequence so we don't change the original data.
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, inpvalue, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, inpvalue, self.dataout, matherrors=True)


	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for maxlen='a' - Array code bytes.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2aout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2bout, maxlen='a')


	########################################################
	def test_lshift_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for matherrors=True (unsupported option) - Array code bytes.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2aout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2bout, matherrors=True)


	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for maxlen='a' - Array code bytes.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2a, self.dataout, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2b, self.dataout, maxlen='a')


	########################################################
	def test_lshift_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for matherrors=True (unsupported option) - Array code bytes.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2b, self.dataout, matherrors=True)


	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for maxlen='a' - Array code bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, self.inparray2a, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, self.inparray2b, maxlen='a')


	########################################################
	def test_lshift_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for matherrors=True (unsupported option) - Array code bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, self.inparray2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, self.inparray2b, matherrors=True)


	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for maxlen='a' - Array code bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, self.inparray2a, self.dataout, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, self.inparray2b, self.dataout, maxlen='a')


	########################################################
	def test_lshift_array_array_array_f2(self):
		"""Test lshift as *array-array-array* for matherrors=True (unsupported option) - Array code bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, self.inparray2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, self.inparray2b, self.dataout, matherrors=True)



##############################################################################



##############################################################################
class lshift_opt_nosimd_param_errors_bytes(unittest.TestCase):
	"""Test lshift for invalid nosimd parameter.
	param_invalid_opt_nosimd_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.inpdata1a = [100,101,102,103,104,105,106,107,108,109]
		self.inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), self.inpdata1a)]

		arraysize = len(self.inpdata1a)
		self.outpdata = itertools.repeat(0, arraysize)


		self.inparray1a = bytes(self.inpdata1a)
		self.inparray2a = bytes(self.inpdata2a)

		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2b = copy.copy(self.inparray2a)


		# When doing in place calculations, the output must be a bytearray.
		self.dataout = bytearray(self.outpdata)
		self.inparray1aout = bytearray(self.inpdata1a)
		self.inparray2aout = bytearray(self.inpdata2a)


		self.inparray1bout = copy.copy(self.inparray1a)
		self.inparray2bout = copy.copy(self.inparray2a)


	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for nosimd='a' - Array code bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, inpvalue, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, inpvalue, nosimd='a')


	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for nosimd='a' - Array code bytes.
		"""
		# Copy the sequence so we don't change the original data.
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, inpvalue, self.dataout, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, inpvalue, self.dataout, nosimd='a')


	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for nosimd='a' - Array code bytes.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2aout, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2bout, nosimd='a')


	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for nosimd='a' - Array code bytes.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2a, self.dataout, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2b, self.dataout, nosimd='a')


	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for nosimd='a' - Array code bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, self.inparray2a, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, self.inparray2b, nosimd='a')


	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for nosimd='a' - Array code bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, self.inparray2a, self.dataout, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, self.inparray2b, self.dataout, nosimd='a')



##############################################################################



##############################################################################
class lshift_seqlen_param_errors_bytes(unittest.TestCase):
	"""Test lshift for invalid sequence lengths. Only parameter patterns
	which have more than one sequence can be tested.
	param_invalid_seqlen_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		inpdata1a = [100,101,102,103,104,105,106,107,108,109]
		inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), inpdata1a)]

		arraysize = len(inpdata1a)
		outpdata = itertools.repeat(0, arraysize)
		longoutpdata = itertools.repeat(0, arraysize * 2)


		# Regular sized sequences.
		self.goodseq1a = bytes(inpdata1a)
		self.goodseq1b = bytearray(inpdata1a)
		self.goodseq2a = bytes(inpdata2a)

		# When using a dedicated output sequence it must be a bytearray.
		self.dataout = bytearray(outpdata)


		# Longer sequences.
		self.longseq1a = bytes(inpdata1a * 2)
		self.longseq1b = bytearray(inpdata1a * 2)
		self.longseq2a = bytes(inpdata2a * 2)

		# When using a dedicated output sequence it must be a bytearray.
		self.longdataout = bytearray(longoutpdata)

		# This is an arbitrary numeric value which should work in call cases.
		self.inpvalue = 4


	########################################################
	def test_lshift_array_num_array_a1(self):
		"""Test lshift as *array-num-array* for mismatched sequence length - Seq type bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.inpvalue, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.longseq1a, self.inpvalue, self.dataout)



	########################################################
	def test_lshift_num_array_array_b1(self):
		"""Test lshift as *num-array-array* for mismatched sequence length - Seq type bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inpvalue, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inpvalue, self.longseq2a, self.dataout)


	########################################################
	def test_lshift_array_array_none_c1(self):
		"""Test lshift as *array-array-none* for mismatched sequence length - Seq type bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1b, self.goodseq2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.longseq1b, self.goodseq2a)


	########################################################
	def test_lshift_array_array_array_c2(self):
		"""Test lshift as *array-array-array* for mismatched sequence length - Seq type bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.longseq1a, self.goodseq2a, self.dataout)


	########################################################
	def test_lshift_array_array_array_c3(self):
		"""Test lshift as *array-array-array* for mismatched sequence length - Seq type bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.goodseq1a, self.longseq2a, self.dataout)


	########################################################
	def test_lshift_array_array_array_c4(self):
		"""Test lshift as *array-array-array* for mismatched sequence length - Seq type bytes.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.longdataout)


##############################################################################



##############################################################################
class lshift_param_errors_bytearray(unittest.TestCase):
	"""Test lshift for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata1 = [100,101,102,103,104,105,106,107,108,109]
		testdata2 = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), testdata1)]

		arraysize = len(testdata1)

		self.testarray1 = bytearray(testdata1)
		self.testarray2 = bytearray(testdata2)

		# When doing in place calculations, the output must be a bytearray.
		self.testarray1out = bytearray(testdata1)
		self.testarray2out = bytearray(testdata2)
		self.dataout = bytearray(itertools.repeat(0, arraysize))


		# Create some data array equivalents with an incompatible type.
		self.badarray1 = array.array('d', [float(x) for x in testdata1])
		self.badarray2 = array.array('d', [float(x) for x in testdata2])

		self.baddataout = array.array('d', [float(x) for x in self.dataout])


	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for invalid type of array - Array code bytearray.
		"""
		for testvalue in self.testarray2:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1out)
				badarray1 = copy.copy(self.badarray1)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(badarray1, testvalue)


	########################################################
	def test_lshift_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for invalid type of number - Array code bytearray.
		"""
		for testvalue, badvalue in zip(self.testarray2, self.badarray2):
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1out)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue)

				testarray1 = copy.copy(self.testarray1out)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testarray1, badvalue)



	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for invalid type of array - Array code bytearray.
		"""
		for testvalue in self.testarray2:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1)
				badarray1 = copy.copy(self.badarray1)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(badarray1, testvalue, self.dataout)


	########################################################
	def test_lshift_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for invalid type of number - Array code bytearray.
		"""
		for testvalue, badvalue in zip(self.testarray2, self.badarray2):
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):


				# This version is expected to pass.
				bytesfunc.lshift(self.testarray1, testvalue, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(self.testarray1, badvalue, self.dataout)


	########################################################
	def test_lshift_array_num_array_b3(self):
		"""Test lshift as *array-num-array* for invalid type of output array - Array code bytearray.
		"""
		for testvalue in self.testarray2:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray1 = copy.copy(self.testarray1)

				# This version is expected to pass.
				bytesfunc.lshift(testarray1, testvalue, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testarray1, testvalue, self.baddataout)



	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for invalid type of array - Array code bytearray.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray2 = copy.copy(self.testarray2out)
				badarray2 = copy.copy(self.badarray2)

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, testarray2)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, badarray2)


	########################################################
	def test_lshift_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for invalid type of number - Array code bytearray.
		"""
		for testvalue, badvalue in zip(self.testarray1, self.badarray1):
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# Copy the sequence so we don't change the original data.
				testarray2 = copy.copy(self.testarray2out)

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, testarray2)

				testarray2 = copy.copy(self.testarray2out)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(badvalue, testarray2)



	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for invalid type of array - Array code bytearray.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, self.testarray2, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, self.badarray2, self.dataout)


	########################################################
	def test_lshift_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for invalid type of number - Array code bytearray.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, self.testarray2, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, self.badarray2, self.dataout)


	########################################################
	def test_lshift_num_array_array_d3(self):
		"""Test lshift as *num-array-array* for invalid type of output array - Array code bytearray.
		"""
		for testvalue in self.testarray1:
			with self.subTest(msg='Failed with parameter', testvalue = testvalue):

				# This version is expected to pass.
				bytesfunc.lshift(testvalue, self.testarray2, self.dataout)

				# This is the actual test.
				with self.assertRaises(TypeError):
					bytesfunc.lshift(testvalue, self.testarray2, self.baddataout)



	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for invalid type of array - Array code bytearray.
		"""
		# Copy the sequence so we don't change the original data.
		testarray1 = copy.copy(self.testarray1out)

		# This version is expected to pass.
		bytesfunc.lshift(testarray1, self.testarray2)

		# Copy the sequence so we don't change the original data.
		testarray1out = copy.copy(self.testarray1out)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(testarray1out, self.badarray2)


	########################################################
	def test_lshift_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for invalid type of array - Array code bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1out, self.testarray2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.badarray1, self.testarray2)



	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for invalid type of array - Array code bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1, self.testarray2, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.testarray1, self.badarray2, self.dataout)


	########################################################
	def test_lshift_array_array_array_f2(self):
		"""Test lshift as *array-array-array* for invalid type of array - Array code bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1, self.testarray2, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.badarray1, self.testarray2, self.dataout)


	########################################################
	def test_lshift_array_array_array_f3(self):
		"""Test lshift as *array-array-array* for invalid type of output array - Array code bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.lshift(self.testarray1, self.testarray2, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.testarray1, self.testarray2, self.baddataout)


	########################################################
	def test_lshift_no_params_g1(self):
		"""Test lshift with no parameters - Array code bytearray.
		"""
		with self.assertRaises(TypeError):
			bytesfunc.lshift()


##############################################################################



##############################################################################
class lshift_opt_param_errors_bytearray(unittest.TestCase):
	"""Test lshift for invalid maxlen parameter.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.inpdata1a = [100,101,102,103,104,105,106,107,108,109	]
		self.inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), self.inpdata1a)]

		arraysize = len(self.inpdata1a)
		self.testmaxlen = len(self.inpdata1a) // 2
		self.outpdata = itertools.repeat(0, arraysize)


		self.inparray1a = bytearray(self.inpdata1a)
		self.inparray2a = bytearray(self.inpdata2a)

		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2b = copy.copy(self.inparray2a)


		# When doing in place calculations, the output must be a bytearray.
		self.inparray1aout = bytearray(self.inpdata1a)
		self.inparray2aout = bytearray(self.inpdata2a)
		self.dataout = bytearray(self.outpdata)

		self.inparray1bout = copy.copy(self.inparray1aout)
		self.inparray2bout = copy.copy(self.inparray2aout)

	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for maxlen='a' - Array code bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, inpvalue, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, inpvalue, maxlen='a')


	########################################################
	def test_lshift_array_num_none_a2(self):
		"""Test lshift as *array-num-none* for matherrors=True (unsupported option) - Array code bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, inpvalue)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, inpvalue, matherrors=True)


	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for maxlen='a' - Array code bytearray.
		"""
		# Copy the sequence so we don't change the original data.
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, inpvalue, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, inpvalue, self.dataout, maxlen='a')


	########################################################
	def test_lshift_array_num_array_b2(self):
		"""Test lshift as *array-num-array* for matherrors=True (unsupported option) - Array code bytearray.
		"""
		# Copy the sequence so we don't change the original data.
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, inpvalue, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, inpvalue, self.dataout, matherrors=True)


	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for maxlen='a' - Array code bytearray.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2aout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2bout, maxlen='a')


	########################################################
	def test_lshift_num_array_none_c2(self):
		"""Test lshift as *num-array-none* for matherrors=True (unsupported option) - Array code bytearray.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2aout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2bout, matherrors=True)


	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for maxlen='a' - Array code bytearray.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2a, self.dataout, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2b, self.dataout, maxlen='a')


	########################################################
	def test_lshift_num_array_array_d2(self):
		"""Test lshift as *num-array-array* for matherrors=True (unsupported option) - Array code bytearray.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2b, self.dataout, matherrors=True)


	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for maxlen='a' - Array code bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, self.inparray2a, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, self.inparray2b, maxlen='a')


	########################################################
	def test_lshift_array_array_none_e2(self):
		"""Test lshift as *array-array-none* for matherrors=True (unsupported option) - Array code bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, self.inparray2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, self.inparray2b, matherrors=True)


	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for maxlen='a' - Array code bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, self.inparray2a, self.dataout, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, self.inparray2b, self.dataout, maxlen='a')


	########################################################
	def test_lshift_array_array_array_f2(self):
		"""Test lshift as *array-array-array* for matherrors=True (unsupported option) - Array code bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, self.inparray2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, self.inparray2b, self.dataout, matherrors=True)



##############################################################################



##############################################################################
class lshift_opt_nosimd_param_errors_bytearray(unittest.TestCase):
	"""Test lshift for invalid nosimd parameter.
	param_invalid_opt_nosimd_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.inpdata1a = [100,101,102,103,104,105,106,107,108,109]
		self.inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), self.inpdata1a)]

		arraysize = len(self.inpdata1a)
		self.outpdata = itertools.repeat(0, arraysize)


		self.inparray1a = bytearray(self.inpdata1a)
		self.inparray2a = bytearray(self.inpdata2a)

		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2b = copy.copy(self.inparray2a)


		# When doing in place calculations, the output must be a bytearray.
		self.dataout = bytearray(self.outpdata)
		self.inparray1aout = bytearray(self.inpdata1a)
		self.inparray2aout = bytearray(self.inpdata2a)


		self.inparray1bout = copy.copy(self.inparray1a)
		self.inparray2bout = copy.copy(self.inparray2a)


	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for nosimd='a' - Array code bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, inpvalue, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, inpvalue, nosimd='a')


	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for nosimd='a' - Array code bytearray.
		"""
		# Copy the sequence so we don't change the original data.
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, inpvalue, self.dataout, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, inpvalue, self.dataout, nosimd='a')


	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for nosimd='a' - Array code bytearray.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2aout, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2bout, nosimd='a')


	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for nosimd='a' - Array code bytearray.
		"""
		inpvalue = self.inparray1a[0]

		# This version is expected to pass.
		bytesfunc.lshift(inpvalue, self.inparray2a, self.dataout, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(inpvalue, self.inparray2b, self.dataout, nosimd='a')


	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for nosimd='a' - Array code bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1aout, self.inparray2a, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1bout, self.inparray2b, nosimd='a')


	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for nosimd='a' - Array code bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inparray1a, self.inparray2a, self.dataout, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inparray1b, self.inparray2b, self.dataout, nosimd='a')



##############################################################################



##############################################################################
class lshift_seqlen_param_errors_bytearray(unittest.TestCase):
	"""Test lshift for invalid sequence lengths. Only parameter patterns
	which have more than one sequence can be tested.
	param_invalid_seqlen_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		inpdata1a = [100,101,102,103,104,105,106,107,108,109]
		inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), inpdata1a)]

		arraysize = len(inpdata1a)
		outpdata = itertools.repeat(0, arraysize)
		longoutpdata = itertools.repeat(0, arraysize * 2)


		# Regular sized sequences.
		self.goodseq1a = bytearray(inpdata1a)
		self.goodseq1b = bytearray(inpdata1a)
		self.goodseq2a = bytearray(inpdata2a)

		# When using a dedicated output sequence it must be a bytearray.
		self.dataout = bytearray(outpdata)


		# Longer sequences.
		self.longseq1a = bytearray(inpdata1a * 2)
		self.longseq1b = bytearray(inpdata1a * 2)
		self.longseq2a = bytearray(inpdata2a * 2)

		# When using a dedicated output sequence it must be a bytearray.
		self.longdataout = bytearray(longoutpdata)

		# This is an arbitrary numeric value which should work in call cases.
		self.inpvalue = 4


	########################################################
	def test_lshift_array_num_array_a1(self):
		"""Test lshift as *array-num-array* for mismatched sequence length - Seq type bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.inpvalue, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.longseq1a, self.inpvalue, self.dataout)



	########################################################
	def test_lshift_num_array_array_b1(self):
		"""Test lshift as *num-array-array* for mismatched sequence length - Seq type bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inpvalue, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inpvalue, self.longseq2a, self.dataout)


	########################################################
	def test_lshift_array_array_none_c1(self):
		"""Test lshift as *array-array-none* for mismatched sequence length - Seq type bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1b, self.goodseq2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.longseq1b, self.goodseq2a)


	########################################################
	def test_lshift_array_array_array_c2(self):
		"""Test lshift as *array-array-array* for mismatched sequence length - Seq type bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.longseq1a, self.goodseq2a, self.dataout)


	########################################################
	def test_lshift_array_array_array_c3(self):
		"""Test lshift as *array-array-array* for mismatched sequence length - Seq type bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.goodseq1a, self.longseq2a, self.dataout)


	########################################################
	def test_lshift_array_array_array_c4(self):
		"""Test lshift as *array-array-array* for mismatched sequence length - Seq type bytearray.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.goodseq1a, self.goodseq2a, self.longdataout)


##############################################################################



##############################################################################
class lshift_seq_immutable_param_errors(unittest.TestCase):
	"""Test lshift for immutable output sequence.
	param_seq_immutable_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		inpdata1a = [100,101,102,103,104,105,106,107,108,109]
		inpdata2a = [x for (x,y) in zip(itertools.cycle([0,1,2,3,4,5]), inpdata1a)]

		outpdata = list(itertools.repeat(0, len(inpdata1a)))


		self.bytesinput1 = bytes(inpdata1a)
		self.bytesinput2 = bytes(inpdata2a)
		self.bytesoutput = bytes(outpdata)

		self.bytesarrayin1 = bytearray(inpdata1a)
		self.bytesarrayin2 = bytearray(inpdata2a)
		self.bytesarrayoutput = bytearray(outpdata)


		# This is an arbitrary numeric value which should work in call cases.
		self.inpvalue = 4

	########################################################
	def test_lshift_array_num_none_a1(self):
		"""Test lshift as *array-num-none* for output seq immutable.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.bytesarrayin1, self.inpvalue)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.bytesinput1, self.inpvalue)


	########################################################
	def test_lshift_array_num_array_b1(self):
		"""Test lshift as *array-num-array* for output seq immutable.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.bytesinput1, self.inpvalue, self.bytesarrayoutput)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.bytesinput1, self.inpvalue, self.bytesoutput)


	########################################################
	def test_lshift_num_array_none_c1(self):
		"""Test lshift as *num-array-none* for output seq immutable.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inpvalue, self.bytesarrayin2)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inpvalue, self.bytesinput2)


	########################################################
	def test_lshift_num_array_array_d1(self):
		"""Test lshift as *num-array-array* for output seq immutable.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.inpvalue, self.bytesinput2, self.bytesarrayoutput)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.inpvalue, self.bytesinput2, self.bytesoutput)


	########################################################
	def test_lshift_array_array_none_e1(self):
		"""Test lshift as *array-array-none* for output seq immutable.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.bytesarrayin1, self.bytesinput2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.bytesinput1, self.bytesinput2)


	########################################################
	def test_lshift_array_array_array_f1(self):
		"""Test lshift as *array-array-array* for output seq immutable.
		"""

		# This version is expected to pass.
		bytesfunc.lshift(self.bytesinput1, self.bytesinput2, self.bytesarrayoutput)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.lshift(self.bytesinput1, self.bytesinput2, self.bytesoutput)



##############################################################################


##############################################################################
if __name__ == '__main__':

	# Check to see if the log file option has been selected. This is an option
	# which we have added in order to decide where to output the results.
	if '-l' in sys.argv:
		# Remove the option from the argument list so that "unittest" does 
		# not complain about unknown options.
		sys.argv.remove('-l')

		with open('bytesfunc_unittest.txt', 'a') as f:
			f.write('\n\n')
			f.write('lshift\n\n')
			trun = unittest.TextTestRunner(f)
			unittest.main(testRunner=trun)
	else:
		unittest.main()

##############################################################################
