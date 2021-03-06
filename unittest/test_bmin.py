#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   test_bmin.py
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
"""This conducts unit tests for bmin.
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
class bmin_general_even_arraysize_with_simd_bytes(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytes([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytes([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytes([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytes([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytes([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytes. General test even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.gentest )
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytes. Test increasing values even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.inctest )
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytes. Test decreasing values even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.dectest )
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytes. Test finding max for data type even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest )
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytes. Test finding value from array that contains min for data type even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest )
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytes. Test optional maxlen parameter even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 )
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_even_arraysize_with_simd_bytes(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytes([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytes. Test invalid parameter type even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytes. Test missing parameter even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytes. Test excess parameters even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytes. Test invalid keyword parameter even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_odd_arraysize_with_simd_bytes(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytes([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytes([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytes([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytes([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytes([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytes. General test odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.gentest )
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytes. Test increasing values odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.inctest )
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytes. Test decreasing values odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.dectest )
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytes. Test finding max for data type odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest )
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytes. Test finding value from array that contains min for data type odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest )
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytes. Test optional maxlen parameter odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 )
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_odd_arraysize_with_simd_bytes(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytes([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytes. Test invalid parameter type odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytes. Test missing parameter odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytes. Test excess parameters odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytes. Test invalid keyword parameter odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_even_arraysize_without_simd_bytes(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytes([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytes([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytes([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytes([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytes([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytes. General test even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.gentest , nosimd=True)
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytes. Test increasing values even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.inctest , nosimd=True)
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytes. Test decreasing values even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.dectest , nosimd=True)
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytes. Test finding max for data type even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytes. Test finding value from array that contains min for data type even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest , nosimd=True)
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytes. Test optional maxlen parameter even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_even_arraysize_without_simd_bytes(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytes([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytes. Test invalid parameter type even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytes. Test missing parameter even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytes. Test excess parameters even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytes. Test invalid keyword parameter even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_odd_arraysize_without_simd_bytes(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytes([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytes([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytes([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytes([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytes([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytes. General test odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.gentest , nosimd=True)
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytes. Test increasing values odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.inctest , nosimd=True)
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytes. Test decreasing values odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.dectest , nosimd=True)
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytes. Test finding max for data type odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytes. Test finding value from array that contains min for data type odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest , nosimd=True)
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytes. Test optional maxlen parameter odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_odd_arraysize_without_simd_bytes(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytes([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytes. Test invalid parameter type odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytes. Test missing parameter odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytes. Test excess parameters odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytes. Test invalid keyword parameter odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_even_arraysize_with_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytearray([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytearray([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytearray([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytearray([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytearray([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytearray. General test even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.gentest )
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test increasing values even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.inctest )
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test decreasing values even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.dectest )
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test finding max for data type even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest )
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytearray. Test finding value from array that contains min for data type even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest )
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytearray. Test optional maxlen parameter even length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 )
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_even_arraysize_with_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytearray([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytearray. Test invalid parameter type even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test missing parameter even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test excess parameters even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test invalid keyword parameter even length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_odd_arraysize_with_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytearray([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytearray([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytearray([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytearray([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytearray([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytearray. General test odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.gentest )
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test increasing values odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.inctest )
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test decreasing values odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.dectest )
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test finding max for data type odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest )
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytearray. Test finding value from array that contains min for data type odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest )
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytearray. Test optional maxlen parameter odd length array with SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 )
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_odd_arraysize_with_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytearray([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytearray. Test invalid parameter type odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test missing parameter odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test excess parameters odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test invalid keyword parameter odd length array with SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 )

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_even_arraysize_without_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytearray([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytearray([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytearray([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytearray([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytearray([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytearray. General test even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.gentest , nosimd=True)
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test increasing values even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.inctest , nosimd=True)
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test decreasing values even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.dectest , nosimd=True)
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test finding max for data type even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytearray. Test finding value from array that contains min for data type even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest , nosimd=True)
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytearray. Test optional maxlen parameter even length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_even_arraysize_without_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytearray([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytearray. Test invalid parameter type even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test missing parameter even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test excess parameters even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test invalid keyword parameter even length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


##############################################################################



##############################################################################
class bmin_general_odd_arraysize_without_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic general function operation.
	op_template_general
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

		arraylength = 96 + arrayextension

		MaxVal = 255
		MinVal = 0

		# Generate lists of numbers covering most of the valid data range.
		halfrangeinc = list(range(5, 250))
		halfrangedec = list(range(250, 5, -1))

		gendata = list(itertools.chain.from_iterable(zip(halfrangeinc, halfrangedec)))
		incdata = halfrangeinc
		decdata = halfrangedec
		maxvaldata = list(itertools.chain(halfrangeinc, [MaxVal], halfrangedec))
		minvaldata = list((itertools.chain(halfrangeinc, [MinVal], halfrangedec)))


		# Test arrays.
		self.gentest = bytearray([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = bytearray([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = bytearray([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = bytearray([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = bytearray([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_bmin_general_function_01(self):
		"""Test bmin  - Sequence type bytearray. General test odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.gentest , nosimd=True)
		self.assertEqual(result, min(self.gentest))


	########################################################
	def test_bmin_general_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test increasing values odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.inctest , nosimd=True)
		self.assertEqual(result, min(self.inctest))


	########################################################
	def test_bmin_general_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test decreasing values odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.dectest , nosimd=True)
		self.assertEqual(result, min(self.dectest))


	########################################################
	def test_bmin_general_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test finding max for data type odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest))


	########################################################
	def test_bmin_general_function_05(self):
		"""Test bmin  - Sequence type bytearray. Test finding value from array that contains min for data type odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.minvaltest , nosimd=True)
		self.assertEqual(result, min(self.minvaltest))


	########################################################
	def test_bmin_general_function_06(self):
		"""Test bmin  - Sequence type bytearray. Test optional maxlen parameter odd length array without SIMD.
		"""
		result = bytesfunc.bmin(self.maxvaltest, maxlen=5 , nosimd=True)
		self.assertEqual(result, min(self.maxvaltest[:5]))



##############################################################################



##############################################################################
class bmin_parameter_odd_arraysize_without_simd_bytearray(unittest.TestCase):
	"""Test bmin for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = bytearray([MaxVal // 2] * arraylength)


	########################################################
	def test_bmin_param_function_01(self):
		"""Test bmin  - Sequence type bytearray. Test invalid parameter type odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(1 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(1)


	########################################################
	def test_bmin_param_function_02(self):
		"""Test bmin  - Sequence type bytearray. Test missing parameter odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min()


	########################################################
	def test_bmin_param_function_03(self):
		"""Test bmin  - Sequence type bytearray. Test excess parameters odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, 5, 2, 2 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, 2)


	########################################################
	def test_bmin_param_function_04(self):
		"""Test bmin  - Sequence type bytearray. Test invalid keyword parameter odd length array without SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bmin(self.gentest, xxxx=5 , nosimd=True)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = min(self.gentest, xxxx=5)


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
			f.write('bmin\n\n')
			trun = unittest.TextTestRunner(f)
			unittest.main(testRunner=trun)
	else:
		unittest.main()

##############################################################################
