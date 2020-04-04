#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the unit tests for ball, bany, findindex.
# Language: Python 3.4
# Date:     21-May-2014
#
###############################################################################
#
#   Copyright 2014 - 2019    Michael Griffin    <m12.griffin@gmail.com>
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

import itertools
import codegen_common

# ==============================================================================


# This template is for ball operations.
test_template_ball = ''' 

##############################################################################
class ball_general_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typelabel)s_%(testdataset)s(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_ball
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if '%(arrayevenodd)s' == 'odd':
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
	def test_ball_basic_eq_a1(self):
		"""Test ball for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are the same.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('==', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_eq_a2(self):
		"""Test ball for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are different.
		testval = %(tval1)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('==', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_eq_a3(self):
		"""Test ball for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is different.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('==', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)



	########################################################
	def test_ball_basic_gt_b1(self):
		"""Test ball for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('>', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_gt_b2(self):
		"""Test ball for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('>', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_gt_b3(self):
		"""Test ball for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('>', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)



	########################################################
	def test_ball_basic_ge_c1(self):
		"""Test ball for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('>=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_ge_c2(self):
		"""Test ball for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('>=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_ge_c3(self):
		"""Test ball for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('>=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_ge_c4(self):
		"""Test ball for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('>=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_ge_c5(self):
		"""Test ball for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('>=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)



	########################################################
	def test_ball_basic_lt_d1(self):
		"""Test ball for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('<', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_lt_d2(self):
		"""Test ball for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('<', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_lt_d3(self):
		"""Test ball for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('<', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)



	########################################################
	def test_ball_basic_le_e1(self):
		"""Test ball for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('<=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_le_e2(self):
		"""Test ball for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('<=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_le_e3(self):
		"""Test ball for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval4)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('<=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_le_e4(self):
		"""Test ball for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('<=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_le_e5(self):
		"""Test ball for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval4)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('<=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)



	########################################################
	def test_ball_basic_ne_f1(self):
		"""Test ball for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are not the same.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.ball('!=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_ne_f2(self):
		"""Test ball for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are the same.
		testval = %(tval1)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = all([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('!=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_ball_basic_ne_f3(self):
		"""Test ball for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = all([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.ball('!=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)



##############################################################################

'''


# ==============================================================================

# This template is for bany operations.
test_template_bany = ''' 

##############################################################################
class bany_general_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typelabel)s_%(testdataset)s(unittest.TestCase):
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
		if '%(arrayevenodd)s' == 'odd':
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
		"""Test bany for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are the same.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a2(self):
		"""Test bany for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are different.
		testval = %(tval1)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_eq_a3(self):
		"""Test bany for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x == testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('==', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_gt_b1(self):
		"""Test bany for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b2(self):
		"""Test bany for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_gt_b3(self):
		"""Test bany for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval3)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x > testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ge_c1(self):
		"""Test bany for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c2(self):
		"""Test bany for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c3(self):
		"""Test bany for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval3)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c4(self):
		"""Test bany for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ge_c5(self):
		"""Test bany for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x >= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('>=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_lt_d1(self):
		"""Test bany for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d2(self):
		"""Test bany for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_lt_d3(self):
		"""Test bany for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval3)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval2)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x < testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_le_e1(self):
		"""Test bany for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e2(self):
		"""Test bany for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e3(self):
		"""Test bany for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval3)s
		arrayval = %(tval4)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval2)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e4(self):
		"""Test bany for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_le_e5(self):
		"""Test bany for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x <= testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('<=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)



	########################################################
	def test_bany_basic_ne_f1(self):
		"""Test bany for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are not the same.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f2(self):
		"""Test bany for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are the same.
		testval = %(tval1)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertFalse(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval %(nosimd)s)
		self.assertFalse(result)
		self.assertEqual(result, expected)


	########################################################
	def test_bany_basic_ne_f3(self):
		"""Test bany for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		expected = any([(x != testval) for x in testdata])
		self.assertTrue(expected)

		# The actual test.
		result = bytesfunc.bany('!=', testdata, testval %(nosimd)s)
		self.assertTrue(result)
		self.assertEqual(result, expected)



##############################################################################

'''


# ==============================================================================


# This template is for findindex operations.
test_template_findindex = ''' 

##############################################################################
class findindex_general_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typelabel)s_%(testdataset)s(unittest.TestCase):
	"""Test for basic general function operation.
	test_template_findindex
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# We use a template to generate this code, so the following
		# compare is inserted into the template to generate code which
		# spills over past the SIMD handler.
		if '%(arrayevenodd)s' == 'odd':
			arrayextension = 5
		else:
			arrayextension = 0
		
		self.arraylength = 96 + arrayextension

		self.ARR_ERR_NOTFOUND = -1


		# Test values are filled in via a template. The relationship
		# between the numbers should be similar to the following example.
		# tval1 = 99
		# tval2 = 100
		# tval3 = 101
		# tval4 = 102


	########################################################
	def test_findindex_basic_eq_a1(self):
		"""Test findindex for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are the same.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y == testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('==', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_eq_a2(self):
		"""Test findindex for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are different.
		testval = %(tval1)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y == testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('==', testdata, testval %(nosimd)s)
		self.assertEqual(result, self.ARR_ERR_NOTFOUND)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_eq_a3(self):
		"""Test findindex for eq  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is the same.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y == testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('==', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)



	########################################################
	def test_findindex_basic_gt_b1(self):
		"""Test findindex for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y > testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_gt_b2(self):
		"""Test findindex for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y > testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>', testdata, testval %(nosimd)s)
		self.assertEqual(result, self.ARR_ERR_NOTFOUND)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_gt_b3(self):
		"""Test findindex for gt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is greater than to the test value.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval3)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y > testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)



	########################################################
	def test_findindex_basic_ge_c1(self):
		"""Test findindex for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y >= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>=', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_ge_c2(self):
		"""Test findindex for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y >= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>=', testdata, testval %(nosimd)s)
		self.assertEqual(result, self.ARR_ERR_NOTFOUND)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_ge_c3(self):
		"""Test findindex for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval3)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y >= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>=', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_ge_c4(self):
		"""Test findindex for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y >= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>=', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_ge_c5(self):
		"""Test findindex for ge  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is equal to the test value.
		testval = %(tval2)s
		arrayval = %(tval1)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = testval
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y >= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('>=', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)



	########################################################
	def test_findindex_basic_lt_d1(self):
		"""Test findindex for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y < testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_lt_d2(self):
		"""Test findindex for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y < testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<', testdata, testval %(nosimd)s)
		self.assertEqual(result, self.ARR_ERR_NOTFOUND)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_lt_d3(self):
		"""Test findindex for lt  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval3)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval2)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y < testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)



	########################################################
	def test_findindex_basic_le_e1(self):
		"""Test findindex for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are less than the test value.
		testval = %(tval3)s
		arrayval = %(tval2)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y <= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<=', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_le_e2(self):
		"""Test findindex for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are greater than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y <= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<=', testdata, testval %(nosimd)s)
		self.assertEqual(result, self.ARR_ERR_NOTFOUND)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_le_e3(self):
		"""Test findindex for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval3)s
		arrayval = %(tval4)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval2)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y <= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<=', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_le_e4(self):
		"""Test findindex for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data values are equal to the test value.
		testval = %(tval2)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y <= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<=', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_le_e5(self):
		"""Test findindex for le  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is less than the test value.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y <= testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('<=', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)



	########################################################
	def test_findindex_basic_ne_f1(self):
		"""Test findindex for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are not the same.
		testval = %(tval2)s
		arrayval = %(tval3)s
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y != testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('!=', testdata, testval %(nosimd)s)
		self.assertEqual(result, 0)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_ne_f2(self):
		"""Test findindex for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# All data and test values are the same.
		testval = %(tval1)s
		arrayval = testval
		testdata = %(typecode)s([arrayval] * self.arraylength)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y != testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('!=', testdata, testval %(nosimd)s)
		self.assertEqual(result, self.ARR_ERR_NOTFOUND)
		self.assertEqual(result, expected)


	########################################################
	def test_findindex_basic_ne_f3(self):
		"""Test findindex for ne  - Sequence type %(typelabel)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		# One test value near the end of the array is not the same.
		testval = %(tval2)s
		arrayval = testval
		testlist = [arrayval] * self.arraylength
		testlist[-2] = %(tval1)s
		testdata = %(typecode)s(testlist)

		# Verify test compatibility.
		pyfind = [x for x,y in enumerate(testdata) if y != testval]
		expected = pyfind[0] if len(pyfind) > 0 else self.ARR_ERR_NOTFOUND

		# The actual test.
		result = bytesfunc.findindex('!=', testdata, testval %(nosimd)s)
		self.assertEqual(result, len(testdata) - 2)
		self.assertEqual(result, expected)



##############################################################################

'''


# ==============================================================================

# ==============================================================================

# The basic template for testing parameters.
param_template = '''
##############################################################################
class %(funclabel)s_parameter_%(typelabel)s(unittest.TestCase):
	"""Test for correct parameters for %(funclabel)s.
	param_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.data = %(typecode)s([100]*100)
		self.dataempty = %(typecode)s()
		self.testdata = 100
		self.baddata = 100.0


	########################################################
	def test_%(funclabel)s_param_a1(self):
		"""Test exception when no parameters passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_%(funclabel)s_param_a2(self):
		"""Test exception when one parameter passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_%(funclabel)s_param_a3(self):
		"""Test exception when two parameters passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all()


	########################################################
	def test_%(funclabel)s_param_a4(self):
		"""Test exception when six parameters passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data, self.testdata, 99, 0, 99)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all([1, 2, 3, 4], 99)


	########################################################
	def test_%(funclabel)s_param_b1(self):
		"""Test exception with invalid keyword parameters passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data, self.testdata, xx=2)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all([1,2,3], xx=2)


	########################################################
	def test_%(funclabel)s_param_b2(self):
		"""Test exception with invalid maxlen keyword parameter type passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data, self.testdata, maxlen='x')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_%(funclabel)s_param_c1(self):
		"""Test exception with invalid first parameter value  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(ValueError):
			result = bytesfunc.%(funcname)s('!', self.data, self.testdata)


	########################################################
	def test_%(funclabel)s_param_c3(self):
		"""Test exception with invalid first parameter type  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(62, self.data, self.testdata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_%(funclabel)s_param_c4(self):
		"""Test exception with invalid array parameter type  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', 99, self.testdata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_%(funclabel)s_param_d1(self):
		"""Test exception with invalid array parameter type  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(IndexError):
			result = bytesfunc.%(funcname)s('==', self.dataempty, self.testdata)


	########################################################
	def test_%(funclabel)s_param_e1(self):
		"""Test exception with invalid compare parameter type  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data, 'e')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_%(funclabel)s_param_e2(self):
		"""Test exception with invalid compare parameter type  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data, self.baddata)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


	########################################################
	def test_%(funclabel)s_param_f1(self):
		"""Test exception with invalid nosimd keyword parameter type passed  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('==', self.data, self.testdata, nosimd='x')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = all(1)


##############################################################################

'''
# ==============================================================================

# ==============================================================================


# The basic template for testing parameter overflow.
overflow_template = '''
##############################################################################
class %(funclabel)s_overflow_%(typelabel)s(unittest.TestCase):
	"""Test for parameter overflow.
	overflow_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		self.data = %(typecode)s([100]*100)
		self.MinVal = 0
		self.Maxval = 255


	########################################################
	def test_overflow_01_min(self):
		"""Test parameter overflow min  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(OverflowError):
			result = bytesfunc.%(funcname)s('==', self.data, self.MinVal - 1)

	########################################################
	def test_overflow_02_max(self):
		"""Test parameter overflow max  - Sequence type %(typelabel)s.
		"""
		with self.assertRaises(OverflowError):
			result = bytesfunc.%(funcname)s('==', self.data, self.Maxval + 1)

	########################################################
	def test_overflow_03_ok(self):
		"""Test no overflow. These should not overflow  - Sequence type %(typelabel)s.
		"""
		result = bytesfunc.%(funcname)s('==', self.data, self.MinVal)
		result = bytesfunc.%(funcname)s('==', self.data, self.Maxval)

##############################################################################

'''

# ==============================================================================



# ==============================================================================


# Test data for ball. 
testdatasets = ((99, 100, 101, 102), (1, 100, 145, 254),  (97, 99, 100, 101))


# ==============================================================================

# This is used to generate test template data for general tests.
def genbasictestdata():
	""" Generate test template data for general tests.
	Returns: (list) - A list of dictionaries containing the keys and
		values to generate individual test functions.
	"""
	# These are the different test values we will combine in various ways.
	arraycode = [('typecode', x) for x in ('bytes', 'bytearray')]
	hassimd = (('simdpresent', 'with'), ('simdpresent', 'without'))
	arraylen = (('arrayevenodd', 'even'), ('arrayevenodd', 'odd'))
	testdata = (('testdataset', 0), ('testdataset', 1), ('testdataset', 2))

	# The product function produces all possible combinations.
	combos = list(itertools.product(arraycode, hassimd, arraylen, testdata))


	# Convert the data into a list of dictionaries.
	testdata = [dict(x) for x in combos]

	nosimd = {'with' : '', 'without' : ', nosimd=True'}

	# Now go through the list and add data which goes with the ones we have already defined.
	for x in testdata:
		x['typelabel'] = x['typecode']
		x['nosimd'] = nosimd[x['simdpresent']]

		x['tval1'] = testdatasets[x['testdataset']][0]
		x['tval2'] = testdatasets[x['testdataset']][1]
		x['tval3'] = testdatasets[x['testdataset']][2]
		x['tval4'] = testdatasets[x['testdataset']][3]

	return testdata


# ==============================================================================

# ==============================================================================


# Select the basic templates.
basictemplates = {'ball' : test_template_ball, 
				'bany' : test_template_bany, 
				'findindex' : test_template_findindex
				}

# ==============================================================================


# The functions which are implemented by this program.
completefuncnames = ('ball', 'bany', 'findindex')


# ==============================================================================

# This defines the module name.
modulename = 'bytesfunc'
# We don't import the array module for bytesfunc.
arrayimport = ''

# Output the functions which implement the individual implementation functions.
for funcname in completefuncnames:

	filenamebase = 'test_' + funcname
	filename = filenamebase + '.py'
	headerdate = codegen_common.FormatHeaderData(filenamebase, '20-Jan-2020', funcname)

	# Add additional header data.
	headerdate['modulename'] = modulename
	headerdate['arrayimport'] = arrayimport


	# Select the implementation template for the current function.
	testtemplate = basictemplates[funcname]

	with open(filename, 'w') as f:
		# The copyright header.
		f.write(codegen_common.HeaderTemplate % headerdate)

		# Basic tests.
		for gentestdata in genbasictestdata():
			# Basic tests.
			f.write(testtemplate % gentestdata)


		#####
		# Parameter tests.

		# Check each array type.
		for arraycode in ('bytes', 'bytearray'):

			f.write(param_template % {'funclabel' : funcname,
									'funcname' : funcname,
									'typelabel' : arraycode,
									'typecode' : arraycode,
									})

		#####
		# Parameter overflow tests.

		# Check each array type.
		for arraycode in ('bytes', 'bytearray'):

			f.write(overflow_template % {'funclabel' : funcname,
									'funcname' : funcname,
									'typelabel' : arraycode,
									'typecode' : arraycode,
									})

		#####
		# The code which initiates the unit test.
		f.write(codegen_common.testendtemplate % {'funcname' : funcname, 'testprefix' : 'bf'})


# ==============================================================================
