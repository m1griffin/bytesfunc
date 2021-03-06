#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   test_ne.py
# Purpose:  bytesfunc unit test.
# Language: Python 3.4
# Date:     01-Nov-2019.
# Ver:      25-Feb-2020.
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
"""This conducts unit tests for ne.
"""

##############################################################################
import sys


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
class ne_param_errors_bytes(unittest.TestCase):
	"""Test for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		self.data1 = bytes([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
		self.data2 = bytes([6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6])

		self.testval1 = self.data1[-1]
		self.testval2 = self.data2[-1]
		

		# Create some sequence equivalents which are different than the correct ones.
		self.badarray1str = ''.join([str(x) for x in self.data1])
		self.badarray1list = list(self.data1)

		self.badarray2str = ''.join([str(x) for x in self.data2])
		self.badarray2list = list(self.data2)


	########################################################
	def test_ne_array_num_a1(self):
		"""Test ne as *array-num* for string sequence - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1str, self.testval2)


	########################################################
	def test_ne_array_num_a2(self):
		"""Test ne as *array-num* for list sequence - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1list, self.testval2)



	########################################################
	def test_ne_array_num_b1(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, -1)


	########################################################
	def test_ne_array_num_b2(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, 256)


	########################################################
	def test_ne_array_num_b3(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, 5.0)


	########################################################
	def test_ne_array_num_b4(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, 'a')



	########################################################
	def test_ne_num_array_c1(self):
		"""Test ne as *num-array* for string sequence - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.testval1, self.badarray2str)


	########################################################
	def test_ne_num_array_c2(self):
		"""Test ne as *num-array* for list sequence - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.testval1, self.badarray2list)



	########################################################
	def test_ne_num_array_d1(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(-1, self.data2)


	########################################################
	def test_ne_num_array_d2(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(256, self.data2)


	########################################################
	def test_ne_num_array_d3(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(5.0, self.data2)


	########################################################
	def test_ne_num_array_d4(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne('a', self.data2)



	########################################################
	def test_ne_array_array_e1(self):
		"""Test ne as *array-array* for incompatible second array - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, self.badarray2str)


	########################################################
	def test_ne_array_array_e2(self):
		"""Test ne as *array-array* for incompatible second array - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, self.badarray2list)



	########################################################
	def test_ne_array_array_f1(self):
		"""Test ne as *array-array* for incompatible first array - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1str, self.data2)


	########################################################
	def test_ne_array_array_f2(self):
		"""Test ne as *array-array* for incompatible first array - Sequence type bytes.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1list, self.data2)



	########################################################
	def test_ne_no_params_g1(self):
		"""Test ne with no parameters - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.ne()


	########################################################
	def test_ne_too_many_params_g2(self):
		"""Test ne with no parameters - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, self.data2, self.data1)


	########################################################
	def test_ne_two_numeric_params_g3(self):
		"""Test ne with two numeric parameters - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.testval1, self.testval2)



##############################################################################



##############################################################################
class ne_param_errors_bytearray(unittest.TestCase):
	"""Test for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		self.data1 = bytearray([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
		self.data2 = bytearray([6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6])

		self.testval1 = self.data1[-1]
		self.testval2 = self.data2[-1]
		

		# Create some sequence equivalents which are different than the correct ones.
		self.badarray1str = ''.join([str(x) for x in self.data1])
		self.badarray1list = list(self.data1)

		self.badarray2str = ''.join([str(x) for x in self.data2])
		self.badarray2list = list(self.data2)


	########################################################
	def test_ne_array_num_a1(self):
		"""Test ne as *array-num* for string sequence - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1str, self.testval2)


	########################################################
	def test_ne_array_num_a2(self):
		"""Test ne as *array-num* for list sequence - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1list, self.testval2)



	########################################################
	def test_ne_array_num_b1(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, -1)


	########################################################
	def test_ne_array_num_b2(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, 256)


	########################################################
	def test_ne_array_num_b3(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, 5.0)


	########################################################
	def test_ne_array_num_b4(self):
		"""Test ne as *array-num* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, 'a')



	########################################################
	def test_ne_num_array_c1(self):
		"""Test ne as *num-array* for string sequence - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.testval1, self.badarray2str)


	########################################################
	def test_ne_num_array_c2(self):
		"""Test ne as *num-array* for list sequence - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.testval1, self.badarray2list)



	########################################################
	def test_ne_num_array_d1(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(-1, self.data2)


	########################################################
	def test_ne_num_array_d2(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(256, self.data2)


	########################################################
	def test_ne_num_array_d3(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(5.0, self.data2)


	########################################################
	def test_ne_num_array_d4(self):
		"""Test ne as *num-array* for incompatible number - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne('a', self.data2)



	########################################################
	def test_ne_array_array_e1(self):
		"""Test ne as *array-array* for incompatible second array - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, self.badarray2str)


	########################################################
	def test_ne_array_array_e2(self):
		"""Test ne as *array-array* for incompatible second array - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, self.badarray2list)



	########################################################
	def test_ne_array_array_f1(self):
		"""Test ne as *array-array* for incompatible first array - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1str, self.data2)


	########################################################
	def test_ne_array_array_f2(self):
		"""Test ne as *array-array* for incompatible first array - Sequence type bytearray.
		"""
		# This version is expected to pass.
		result = bytesfunc.ne(self.data1, self.data2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.badarray1list, self.data2)



	########################################################
	def test_ne_no_params_g1(self):
		"""Test ne with no parameters - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.ne()


	########################################################
	def test_ne_too_many_params_g2(self):
		"""Test ne with no parameters - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.data1, self.data2, self.data1)


	########################################################
	def test_ne_two_numeric_params_g3(self):
		"""Test ne with two numeric parameters - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.testval1, self.testval2)



##############################################################################



##############################################################################
class ne_param_errors_opt_bytes(unittest.TestCase):
	"""Test for invalid errors and maxlen parameters. The errors does not
	exist with these functions.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""

		self.inparray1a = bytes([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2a = bytes([6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6])
		self.inparray2b = copy.copy(self.inparray2a)

		self.testmaxlen = len(self.inparray1a) // 2


	########################################################
	def test_ne_array_num_a1(self):
		"""Test ne as *array-num* for matherrors=True - Sequence type bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, inpvalue)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, inpvalue, matherrors=True)


	########################################################
	def test_ne_array_num_a2(self):
		"""Test ne as *array-num* for maxlen='a' - Sequence type bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, inpvalue, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, inpvalue, maxlen='a')


	########################################################
	def test_ne_array_num_a3(self):
		"""Test ne as *array-num* for nosimd='a' - Sequence type bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, inpvalue, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, inpvalue, nosimd='a')


	########################################################
	def test_ne_num_array_c1(self):
		"""Test ne as *num-array* for matherrors=True - Sequence type bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(inpvalue, self.inparray1a)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(inpvalue, self.inparray1a, matherrors=True)


	########################################################
	def test_ne_num_array_c2(self):
		"""Test ne as *num-array* for maxlen='a' - Sequence type bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(inpvalue, self.inparray1a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(inpvalue, self.inparray1a, maxlen='a')


	########################################################
	def test_ne_num_array_c3(self):
		"""Test ne as *num-array* for nosimd='a' - Sequence type bytes.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(inpvalue, self.inparray1a, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(inpvalue, self.inparray1a, nosimd='a')


	########################################################
	def test_ne_array_array_e1(self):
		"""Test ne as *array-array* for matherrors=True - Sequence type bytes.
		"""

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, self.inparray2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, self.inparray2a, matherrors=True)


	########################################################
	def test_ne_array_array_e2(self):
		"""Test ne as *array-array* for maxlen='a' - Sequence type bytes.
		"""

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, self.inparray2a, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, self.inparray2a, maxlen='a')


	########################################################
	def test_ne_array_array_e3(self):
		"""Test ne as *array-array* for nosimd='a' - Sequence type bytes.
		"""

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, self.inparray2a, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, self.inparray2a, nosimd='a')


##############################################################################



##############################################################################
class ne_param_errors_opt_bytearray(unittest.TestCase):
	"""Test for invalid errors and maxlen parameters. The errors does not
	exist with these functions.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""

		self.inparray1a = bytearray([5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2a = bytearray([6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6])
		self.inparray2b = copy.copy(self.inparray2a)

		self.testmaxlen = len(self.inparray1a) // 2


	########################################################
	def test_ne_array_num_a1(self):
		"""Test ne as *array-num* for matherrors=True - Sequence type bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, inpvalue)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, inpvalue, matherrors=True)


	########################################################
	def test_ne_array_num_a2(self):
		"""Test ne as *array-num* for maxlen='a' - Sequence type bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, inpvalue, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, inpvalue, maxlen='a')


	########################################################
	def test_ne_array_num_a3(self):
		"""Test ne as *array-num* for nosimd='a' - Sequence type bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, inpvalue, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, inpvalue, nosimd='a')


	########################################################
	def test_ne_num_array_c1(self):
		"""Test ne as *num-array* for matherrors=True - Sequence type bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(inpvalue, self.inparray1a)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(inpvalue, self.inparray1a, matherrors=True)


	########################################################
	def test_ne_num_array_c2(self):
		"""Test ne as *num-array* for maxlen='a' - Sequence type bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(inpvalue, self.inparray1a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(inpvalue, self.inparray1a, maxlen='a')


	########################################################
	def test_ne_num_array_c3(self):
		"""Test ne as *num-array* for nosimd='a' - Sequence type bytearray.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.ne(inpvalue, self.inparray1a, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(inpvalue, self.inparray1a, nosimd='a')


	########################################################
	def test_ne_array_array_e1(self):
		"""Test ne as *array-array* for matherrors=True - Sequence type bytearray.
		"""

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, self.inparray2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, self.inparray2a, matherrors=True)


	########################################################
	def test_ne_array_array_e2(self):
		"""Test ne as *array-array* for maxlen='a' - Sequence type bytearray.
		"""

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, self.inparray2a, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, self.inparray2a, maxlen='a')


	########################################################
	def test_ne_array_array_e3(self):
		"""Test ne as *array-array* for nosimd='a' - Sequence type bytearray.
		"""

		# This version is expected to pass.
		result = bytesfunc.ne(self.inparray1a, self.inparray2a, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.ne(self.inparray1a, self.inparray2a, nosimd='a')


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_nosimd_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_nosimd_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_withsimd_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_withsimd_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_nosimd_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_nosimd_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_withsimd_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_withsimd_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytes(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytes(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytes.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytes.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytes.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytes.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytes.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_nosimd_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_nosimd_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_withsimd_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_even_arraysize_withsimd_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'even' == 'even':
			testdatasize = 512
		if 'even' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_nosimd_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_nosimd_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array , nosimd=True)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited , nosimd=True)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail , nosimd=True)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited , nosimd=True)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_withsimd_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_array_num_pass = [210, 11, 0, 255, 210]
		self.param_array_num_fail = [10, 10, 10, 10, 10]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.param_num_array_pass = [210, 11, 0, 255, 210]
		self.param_num_array_fail = [10, 10, 10, 10, 10]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([12, 9, 245]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([10, 10, 10]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 

##############################################################################
class ne_general_odd_arraysize_withsimd_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if 'odd' == 'even':
			testdatasize = 512
		if 'odd' == 'odd':
			testdatasize = 511


		self.data_array_num = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_array_num_pass = [10, 211, 0, 255, 10]
		self.param_array_num_fail = [210, 210, 210, 210, 210]

		self.data_num_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.param_num_array_pass = [10, 211, 0, 255, 10]
		self.param_num_array_fail = [210, 210, 210, 210, 210]

		self.data_array_array = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))
		self.data_array_array_pass = bytearray(list(itertools.islice(itertools.cycle([212, 9, 45]), testdatasize)))
		self.data_array_array_fail = bytearray(list(itertools.islice(itertools.cycle([210, 210, 210]), testdatasize)))


	########################################################
	def test_ne_basic_array_num_a1(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a2(self):
		"""Test ne as *array-num* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x != testval for x in self.data_array_num])

				result = bytesfunc.ne(self.data_array_num, testval )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_num_a3(self):
		"""Test ne as *array-num* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x != testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.ne(self.data_array_num, testval, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b1(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b2(self):
		"""Test ne as *num-array* for basic function - Sequence type bytearray.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval != x for x in self.data_num_array])

				result = bytesfunc.ne(testval, self.data_num_array )

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_num_array_b3(self):
		"""Test ne as *num-array* for basic function with array limit - Sequence type bytearray.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval != x for x in self.data_num_array[0:limited]])

				result = bytesfunc.ne(testval, self.data_num_array, maxlen=limited )

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c1(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c2(self):
		"""Test ne as *array-array* for basic function - Sequence type bytearray.
		"""
		expected = all([x != y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.ne(self.data_array_array, self.data_array_array_fail )

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_ne_basic_array_array_c3(self):
		"""Test ne as *array-array* for basic function with array limit - Sequence type bytearray.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x != y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.ne(self.data_array_array, self.data_array_array_pass, maxlen=limited )

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

 


##############################################################################
class ne_numpos_bytes(unittest.TestCase):
	"""Test with a single fail value in different array positions.
	test_template_numpos
	"""


	########################################################
	def setUp(self):
		"""Initialise. The test data is generated from the script itself.
		"""
		self.testarraylen = 159

		test_data1 = [5] * self.testarraylen
		self.data1 = bytes(test_data1)

		self.testval1 = self.data1[0]

		self.data1_fail = [5] * self.testarraylen
		self.data1_fail[-1] = 6
		self.data1fail = bytes(self.data1_fail)

		test_data2 = [6] * self.testarraylen
		self.data2 = bytes(test_data2)

		self.testval2 = self.data2[0]

		self.data2_fail = [6] * self.testarraylen
		self.data2_fail[-1] = 5
		self.data2fail = bytes(self.data2_fail)



	########################################################
	def test_ne_numpos_array_num_a1(self):
		"""Test ne as *array-num* for failing with different data positions in array - Sequence type bytes.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x != self.testval2 for x in self.data1fail])

				result = bytesfunc.ne(self.data1fail, self.testval2)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			# Shift the data one position.
			self.data1_fail.append(self.data1_fail.pop(0))
			self.data1fail = bytes(self.data1_fail)


	########################################################
	def test_ne_numpos_num_array_b1(self):
		"""Test ne as *num-array* for failing with different data positions in array - Sequence type bytes.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([self.testval1 != x for x in self.data2fail])

				result = bytesfunc.ne(self.testval1, self.data2fail)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data2_fail.append(self.data2_fail.pop(0))
			self.data2fail = bytes(self.data2_fail)


	########################################################
	def test_ne_numpos_array_array_c1(self):
		"""Test ne as *array-array* for failing with different data positions in array 1 - Sequence type bytes.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x != y for x,y in zip(self.data1fail, self.data2)])

				result = bytesfunc.ne(self.data1fail, self.data2)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data1_fail.append(self.data1_fail.pop(0))
			self.data1fail = bytes(self.data1_fail)


	########################################################
	def test_ne_numpos_array_array_c2(self):
		"""Test ne as *array-array* for failing with different data positions in array 2 - Sequence type bytes.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x != y for x,y in zip(self.data1, self.data2fail)])

				result = bytesfunc.ne(self.data1, self.data2fail)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data2_fail.append(self.data2_fail.pop(0))
			self.data2fail = bytes(self.data2_fail)


##############################################################################

 


##############################################################################
class ne_numpos_bytearray(unittest.TestCase):
	"""Test with a single fail value in different array positions.
	test_template_numpos
	"""


	########################################################
	def setUp(self):
		"""Initialise. The test data is generated from the script itself.
		"""
		self.testarraylen = 159

		test_data1 = [5] * self.testarraylen
		self.data1 = bytearray(test_data1)

		self.testval1 = self.data1[0]

		self.data1_fail = [5] * self.testarraylen
		self.data1_fail[-1] = 6
		self.data1fail = bytearray(self.data1_fail)

		test_data2 = [6] * self.testarraylen
		self.data2 = bytearray(test_data2)

		self.testval2 = self.data2[0]

		self.data2_fail = [6] * self.testarraylen
		self.data2_fail[-1] = 5
		self.data2fail = bytearray(self.data2_fail)



	########################################################
	def test_ne_numpos_array_num_a1(self):
		"""Test ne as *array-num* for failing with different data positions in array - Sequence type bytearray.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x != self.testval2 for x in self.data1fail])

				result = bytesfunc.ne(self.data1fail, self.testval2)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			# Shift the data one position.
			self.data1_fail.append(self.data1_fail.pop(0))
			self.data1fail = bytearray(self.data1_fail)


	########################################################
	def test_ne_numpos_num_array_b1(self):
		"""Test ne as *num-array* for failing with different data positions in array - Sequence type bytearray.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([self.testval1 != x for x in self.data2fail])

				result = bytesfunc.ne(self.testval1, self.data2fail)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data2_fail.append(self.data2_fail.pop(0))
			self.data2fail = bytearray(self.data2_fail)


	########################################################
	def test_ne_numpos_array_array_c1(self):
		"""Test ne as *array-array* for failing with different data positions in array 1 - Sequence type bytearray.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x != y for x,y in zip(self.data1fail, self.data2)])

				result = bytesfunc.ne(self.data1fail, self.data2)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data1_fail.append(self.data1_fail.pop(0))
			self.data1fail = bytearray(self.data1_fail)


	########################################################
	def test_ne_numpos_array_array_c2(self):
		"""Test ne as *array-array* for failing with different data positions in array 2 - Sequence type bytearray.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x != y for x,y in zip(self.data1, self.data2fail)])

				result = bytesfunc.ne(self.data1, self.data2fail)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data2_fail.append(self.data2_fail.pop(0))
			self.data2fail = bytearray(self.data2_fail)


##############################################################################


##############################################################################
if __name__ == '__main__':

	# Check to see if the log file option has been selected. This is an option
	# which we have added in order to decide where to output the results.
	if '-l' in sys.argv:
		# Remove the option from the argument list so that "unittest" does 
		# not complain about unknown options.
		sys.argv.remove('-l')

		with open('bf_unittest.txt', 'a') as f:
			f.write('\n\n')
			f.write('ne\n\n')
			trun = unittest.TextTestRunner(f)
			unittest.main(testRunner=trun)
	else:
		unittest.main()

##############################################################################
