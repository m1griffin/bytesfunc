#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   test_invert.py
# Purpose:  bytesfunc unit test.
# Language: Python 3.4
# Date:     30-Jan-2020.
# Ver:      30-Jan-2020.
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
"""This conducts unit tests for invert.
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
class invert_general_even_arraysize_nosimd_simd_bytes(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'even' == 'even':
			testdatasize = 320
		if 'even' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytes(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_even_arraysize_withsimd_simd_bytes(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'even' == 'even':
			testdatasize = 320
		if 'even' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytes(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_odd_arraysize_nosimd_simd_bytes(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'odd' == 'even':
			testdatasize = 320
		if 'odd' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytes(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_odd_arraysize_withsimd_simd_bytes(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'odd' == 'even':
			testdatasize = 320
		if 'odd' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytes(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytes.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_even_arraysize_nosimd_simd_bytearray(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'even' == 'even':
			testdatasize = 320
		if 'even' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytearray(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_even_arraysize_withsimd_simd_bytearray(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'even' == 'even':
			testdatasize = 320
		if 'even' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytearray(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_odd_arraysize_nosimd_simd_bytearray(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'odd' == 'even':
			testdatasize = 320
		if 'odd' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytearray(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited , nosimd=True)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_general_odd_arraysize_withsimd_simd_bytearray(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if 'odd' == 'even':
			testdatasize = 320
		if 'odd' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = bytearray(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_invert_inplace(self):
		"""Test invert in place - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_inplace_maxlen(self):
		"""Test invert in place with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.datam, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray(self):
		"""Test invert to output array - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_invert_outputarray_maxlen(self):
		"""Test invert to output array with array maxlen  - Sequence type bytearray.
		"""
		bytesfunc.invert(self.data, self.dataout, maxlen=self.limited )

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################



##############################################################################
class invert_param_errors_bytes(unittest.TestCase):
	"""Test invert for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.testarray1 = bytes(testdata)
		self.testarray2 = bytes(testdata)

		arraysize = len(self.testarray1)

		self.dataout = bytearray(itertools.repeat(0, arraysize))

		# Create some data array equivalents with an incompatible type.
		self.badarray1 = array.array('d', [float(x) for x in self.testarray1])

		self.baddataout = array.array('d', [float(x) for x in self.dataout])



	########################################################
	def test_invert_array_array_a1(self):
		"""Test invert as *array-array* for invalid type of input array - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.testarray1, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.badarray1, self.dataout)


	########################################################
	def test_invert_array_array_a2(self):
		"""Test invert as *array-array* for invalid type of output array - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.testarray1, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.testarray2, self.baddataout)


##############################################################################



##############################################################################
class invert_opt_param_errors_bytes(unittest.TestCase):
	"""Test invert for invalid maxlen parameters.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

		self.inparray1a = bytes(testdata)
		self.inparray1b = bytes(testdata)

		self.inparray2a = bytearray(testdata)
		self.inparray2b = bytearray(testdata)

		arraysize = len(self.inparray1a)

		self.dataout = bytearray(itertools.repeat(0, arraysize))

		self.testmaxlen = len(self.inparray1a) // 2


	########################################################
	def test_invert_array_none_a1(self):
		"""Test invert as *array-none* for maxlen='a' - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray2a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray2b, maxlen='a')


	########################################################
	def test_invert_array_none_a2(self):
		"""Test invert as *array-none* for nosimd='a' - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray2a, nosimd=False)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray2b, nosimd='a')


	########################################################
	def test_invert_array_array_b1(self):
		"""Test invert as *array-array* for maxlen='a' - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray1a, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray1b, self.dataout, maxlen='a')


	########################################################
	def test_invert_array_array_b2(self):
		"""Test invert as *array-array* for nosimd='a' - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray1a, self.dataout, nosimd=False)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray1b, self.dataout, nosimd='a')


	########################################################
	def test_invert_array_none_c1(self):
		"""Test invert as *array-none* for matherrors=True (unsupported option) - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray2a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray2b, matherrors=True)


	########################################################
	def test_invert_array_array_d1(self):
		"""Test invert as *array-array* for matherrors=True (unsupported option) - Sequence type bytes.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray1a, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray1b, self.dataout, matherrors=True)


	########################################################
	def test_invert_no_params_e1(self):
		"""Test invert with no parameters - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			bytesfunc.invert()


##############################################################################



##############################################################################
class invert_param_errors_bytearray(unittest.TestCase):
	"""Test invert for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.testarray1 = bytearray(testdata)
		self.testarray2 = bytearray(testdata)

		arraysize = len(self.testarray1)

		self.dataout = bytearray(itertools.repeat(0, arraysize))

		# Create some data array equivalents with an incompatible type.
		self.badarray1 = array.array('d', [float(x) for x in self.testarray1])

		self.baddataout = array.array('d', [float(x) for x in self.dataout])



	########################################################
	def test_invert_array_array_a1(self):
		"""Test invert as *array-array* for invalid type of input array - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.testarray1, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.badarray1, self.dataout)


	########################################################
	def test_invert_array_array_a2(self):
		"""Test invert as *array-array* for invalid type of output array - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.testarray1, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.testarray2, self.baddataout)


##############################################################################



##############################################################################
class invert_opt_param_errors_bytearray(unittest.TestCase):
	"""Test invert for invalid maxlen parameters.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

		self.inparray1a = bytearray(testdata)
		self.inparray1b = bytearray(testdata)

		self.inparray2a = bytearray(testdata)
		self.inparray2b = bytearray(testdata)

		arraysize = len(self.inparray1a)

		self.dataout = bytearray(itertools.repeat(0, arraysize))

		self.testmaxlen = len(self.inparray1a) // 2


	########################################################
	def test_invert_array_none_a1(self):
		"""Test invert as *array-none* for maxlen='a' - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray2a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray2b, maxlen='a')


	########################################################
	def test_invert_array_none_a2(self):
		"""Test invert as *array-none* for nosimd='a' - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray2a, nosimd=False)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray2b, nosimd='a')


	########################################################
	def test_invert_array_array_b1(self):
		"""Test invert as *array-array* for maxlen='a' - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray1a, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray1b, self.dataout, maxlen='a')


	########################################################
	def test_invert_array_array_b2(self):
		"""Test invert as *array-array* for nosimd='a' - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray1a, self.dataout, nosimd=False)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray1b, self.dataout, nosimd='a')


	########################################################
	def test_invert_array_none_c1(self):
		"""Test invert as *array-none* for matherrors=True (unsupported option) - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray2a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray2b, matherrors=True)


	########################################################
	def test_invert_array_array_d1(self):
		"""Test invert as *array-array* for matherrors=True (unsupported option) - Sequence type bytearray.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray1a, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray1b, self.dataout, matherrors=True)


	########################################################
	def test_invert_no_params_e1(self):
		"""Test invert with no parameters - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			bytesfunc.invert()


##############################################################################



##############################################################################
class invert_seqlen_param_errors_bytes(unittest.TestCase):
	"""Test invert for invalid sequence lengths. Only parameter patterns
	which have more than one sequence can be tested.
	param_invalid_seqlen_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		testdatashort = [1, 2, 3, 4, 5]

		self.inparray = bytes(testdata)
		self.inparrayshort = bytes(testdatashort)

		self.dataout = bytearray([0] * len(testdata))
		self.dataoutshort = bytearray([0] * len(testdatashort))


	########################################################
	def test_invert_array_array_a1(self):
		"""Test invert as *array-array* for mismatched sequence length - Sequence type bytes
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparrayshort, self.dataout)


	########################################################
	def test_invert_array_array_a2(self):
		"""Test invert as *array-array* for mismatched sequence length - Sequence type bytes
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray, self.dataoutshort)


##############################################################################



##############################################################################
class invert_seqlen_param_errors_bytearray(unittest.TestCase):
	"""Test invert for invalid sequence lengths. Only parameter patterns
	which have more than one sequence can be tested.
	param_invalid_seqlen_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		testdatashort = [1, 2, 3, 4, 5]

		self.inparray = bytearray(testdata)
		self.inparrayshort = bytearray(testdatashort)

		self.dataout = bytearray([0] * len(testdata))
		self.dataoutshort = bytearray([0] * len(testdatashort))


	########################################################
	def test_invert_array_array_a1(self):
		"""Test invert as *array-array* for mismatched sequence length - Sequence type bytearray
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparrayshort, self.dataout)


	########################################################
	def test_invert_array_array_a2(self):
		"""Test invert as *array-array* for mismatched sequence length - Sequence type bytearray
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.inparray, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.inparray, self.dataoutshort)


##############################################################################



##############################################################################
class invert_seq_immutable_param_errors(unittest.TestCase):
	"""Test invert for immutable output sequence.
	param_seq_immutable_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

		self.bytesinp = bytes(testdata)
		self.bytearrayinp = bytearray(testdata)
		
		self.bytesout = bytes([0] * len(testdata))
		self.bytearrayout = bytearray([0] * len(testdata))



	########################################################
	def test_invert_array_none_a1(self):
		"""Test invert as *array-none* for output seq immutable.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.bytearrayinp)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.bytesinp)


	########################################################
	def test_invert_array_array_a2(self):
		"""Test invert as *array-array* for output seq immutable.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.bytesinp, self.bytearrayout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.bytesinp, self.bytesout)



	########################################################
	def test_invert_array_array_a3(self):
		"""Test invert as *array-array* for output seq immutable.
		"""
		# This version is expected to pass.
		bytesfunc.invert(self.bytearrayinp, self.bytearrayout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.invert(self.bytearrayinp, self.bytesout)


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
			f.write('invert\n\n')
			trun = unittest.TextTestRunner(f)
			unittest.main(testRunner=trun)
	else:
		unittest.main()

##############################################################################
