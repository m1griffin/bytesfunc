#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   test_bany.py
# Purpose:  bytesfunc unit test.
# Language: Python 3.4
# Date:     20-Jan-2020.
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
"""This conducts unit tests for bany.
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
class bany_general_even_arraysize_with_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_with_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_with_simd_bytes_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_with_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_with_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_with_simd_bytes_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_without_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_without_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_without_simd_bytes_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test even length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_without_simd_bytes_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_without_simd_bytes_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_without_simd_bytes_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytes([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytes. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytes(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_with_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_with_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_with_simd_bytearray_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_with_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_with_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_with_simd_bytearray_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval )
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_without_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_without_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_even_arraysize_without_simd_bytearray_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'even' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test even length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_without_simd_bytearray_0(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are different.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 101
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 99
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 101
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 101
		arrayval = 102
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 101
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_without_simd_bytearray_1(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are different.
		testval = 1
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 1
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 145
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 100
		arrayval = 1
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 145
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 145
		arrayval = 254
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 100
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 145
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 100
		arrayval = 145
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 1
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 1
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

 

##############################################################################
class bany_general_odd_arraysize_without_simd_bytearray_2(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_bany
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if 'odd' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_bany_basic_eq_a1(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are different.
		testval = 97
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 99
		arrayval = 97
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 100
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = 99
		arrayval = 97
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are less than the test value.
		testval = 100
		arrayval = 99
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are greater than the test value.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 100
		arrayval = 101
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 99
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data values are equal to the test value.
		testval = 99
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = 99
		arrayval = 100
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are not the same.
		testval = 99
		arrayval = 100
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# All data and test values are the same.
		testval = 97
		arrayval = testval
		testdata = bytearray([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = 99
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = 97
		testdata = bytearray(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval , nosimd=True)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################


##############################################################################
class bany_parameter_bytes(unittest.TestCase):
	"""Test for correct parameters for bany.
	param_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.data = bytes([100]*100)
		self.dataempty = bytes()
		self.testdata = 100
		self.baddata = 100.0


	########################################################
	def test_bany_param_a1(self):
		"""Test exception when no parameters passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_bany_param_a2(self):
		"""Test exception when one parameter passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_bany_param_a3(self):
		"""Test exception when two parameters passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_bany_param_a4(self):
		"""Test exception when six parameters passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, 99, 0, 99)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all([1, 2, 3, 4], 99)


	########################################################
	def test_bany_param_b1(self):
		"""Test exception with invalid keyword parameters passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, xx=2)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all([1,2,3], xx=2)


	########################################################
	def test_bany_param_b2(self):
		"""Test exception with invalid maxlen keyword parameter type passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, maxlen='x')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_c1(self):
		"""Test exception with invalid first parameter value  - Sequence type bytes.
		"""
		with self.assertRaises(ValueError):
			result = bytesfunc.bany('!', self.data, self.testdata)


	########################################################
	def test_bany_param_c3(self):
		"""Test exception with invalid first parameter type  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany(62, self.data, self.testdata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_c4(self):
		"""Test exception with invalid array parameter type  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', 99, self.testdata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_d1(self):
		"""Test exception with invalid array parameter type  - Sequence type bytes.
		"""
		with self.assertRaises(IndexError):
			result = bytesfunc.bany('==', self.dataempty, self.testdata)


	########################################################
	def test_bany_param_e1(self):
		"""Test exception with invalid compare parameter type  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, 'e')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_e2(self):
		"""Test exception with invalid compare parameter type  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.baddata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_f1(self):
		"""Test exception with invalid nosimd keyword parameter type passed  - Sequence type bytes.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, nosimd='x')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


##############################################################################


##############################################################################
class bany_parameter_bytearray(unittest.TestCase):
	"""Test for correct parameters for bany.
	param_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.data = bytearray([100]*100)
		self.dataempty = bytearray()
		self.testdata = 100
		self.baddata = 100.0


	########################################################
	def test_bany_param_a1(self):
		"""Test exception when no parameters passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_bany_param_a2(self):
		"""Test exception when one parameter passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_bany_param_a3(self):
		"""Test exception when two parameters passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_bany_param_a4(self):
		"""Test exception when six parameters passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, 99, 0, 99)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all([1, 2, 3, 4], 99)


	########################################################
	def test_bany_param_b1(self):
		"""Test exception with invalid keyword parameters passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, xx=2)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all([1,2,3], xx=2)


	########################################################
	def test_bany_param_b2(self):
		"""Test exception with invalid maxlen keyword parameter type passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, maxlen='x')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_c1(self):
		"""Test exception with invalid first parameter value  - Sequence type bytearray.
		"""
		with self.assertRaises(ValueError):
			result = bytesfunc.bany('!', self.data, self.testdata)


	########################################################
	def test_bany_param_c3(self):
		"""Test exception with invalid first parameter type  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany(62, self.data, self.testdata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_c4(self):
		"""Test exception with invalid array parameter type  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', 99, self.testdata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_d1(self):
		"""Test exception with invalid array parameter type  - Sequence type bytearray.
		"""
		with self.assertRaises(IndexError):
			result = bytesfunc.bany('==', self.dataempty, self.testdata)


	########################################################
	def test_bany_param_e1(self):
		"""Test exception with invalid compare parameter type  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, 'e')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_e2(self):
		"""Test exception with invalid compare parameter type  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.baddata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_bany_param_f1(self):
		"""Test exception with invalid nosimd keyword parameter type passed  - Sequence type bytearray.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bany('==', self.data, self.testdata, nosimd='x')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


##############################################################################


##############################################################################
class bany_overflow_bytes(unittest.TestCase):
	"""Test for parameter overflow.
	overflow_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.data = bytes([100]*100)
		self.MinVal = 0
		self.Maxval = 255


	########################################################
	def test_overflow_01_min(self):
		"""Test parameter overflow min  - Sequence type bytes.
		"""
		with self.assertRaises(OverflowError):
			result = bytesfunc.bany('==', self.data, self.MinVal - 1)

	########################################################
	def test_overflow_02_max(self):
		"""Test parameter overflow max  - Sequence type bytes.
		"""
		with self.assertRaises(OverflowError):
			result = bytesfunc.bany('==', self.data, self.Maxval + 1)

	########################################################
	def test_overflow_03_ok(self):
		"""Test no overflow. These should not overflow  - Sequence type bytes.
		"""
		result = bytesfunc.bany('==', self.data, self.MinVal)
		result = bytesfunc.bany('==', self.data, self.Maxval)

##############################################################################


##############################################################################
class bany_overflow_bytearray(unittest.TestCase):
	"""Test for parameter overflow.
	overflow_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.data = bytearray([100]*100)
		self.MinVal = 0
		self.Maxval = 255


	########################################################
	def test_overflow_01_min(self):
		"""Test parameter overflow min  - Sequence type bytearray.
		"""
		with self.assertRaises(OverflowError):
			result = bytesfunc.bany('==', self.data, self.MinVal - 1)

	########################################################
	def test_overflow_02_max(self):
		"""Test parameter overflow max  - Sequence type bytearray.
		"""
		with self.assertRaises(OverflowError):
			result = bytesfunc.bany('==', self.data, self.Maxval + 1)

	########################################################
	def test_overflow_03_ok(self):
		"""Test no overflow. These should not overflow  - Sequence type bytearray.
		"""
		result = bytesfunc.bany('==', self.data, self.MinVal)
		result = bytesfunc.bany('==', self.data, self.Maxval)

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
			f.write('bany\n\n')
			trun = unittest.TextTestRunner(f)
			unittest.main(testRunner=trun)
	else:
		unittest.main()

##############################################################################
