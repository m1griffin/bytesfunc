#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Module:   test_bsum.py
# Purpose:  bytesfunc unit test.
# Language: Python 3.4
# Date:     11-Jun-2014.
# Ver:      19-Jan-2020.
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
"""This conducts unit tests for bsum.
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
class bsum_general_even_bytes(unittest.TestCase):
	"""Test asum for basic general function operation.
	op_template_general
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# The size of the test arrays. 
		arraylength = 256

		if 'even' == 'odd':
			arraylength = arraylength + 3

		# This produces a list of values.
		testvalues = list(range(0, 256))
		testdata = testvalues[:arraylength]

		self.gentest =  bytes([x for x,y in zip(itertools.cycle(testdata), range(arraylength))])


	########################################################
	def test_bsum_general_function_A1(self):
		"""Test asum  - Array code bytes. General test.
		"""
		result = bytesfunc.bsum(self.gentest)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_B1(self):
		"""Test asum  - Array code bytes. Test optional maxlen parameter.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50)
		self.assertEqual(result, sum(self.gentest[:50]))


	########################################################
	def test_bsum_general_function_C1(self):
		"""Test asum  - Array code bytes. Test optional matherrors parameter.
		"""
		result = bytesfunc.bsum(self.gentest, matherrors=True)
		self.assertEqual(result, sum(self.gentest))



	########################################################
	def test_bsum_general_function_E1(self):
		"""Test asum  - Array code bytes. Test optional maxlen, matherrors parameters together.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50, matherrors=True)
		self.assertEqual(result, sum(self.gentest[:50]))



##############################################################################



##############################################################################
class bsum_general_odd_bytes(unittest.TestCase):
	"""Test asum for basic general function operation.
	op_template_general
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# The size of the test arrays. 
		arraylength = 256

		if 'odd' == 'odd':
			arraylength = arraylength + 3

		# This produces a list of values.
		testvalues = list(range(0, 256))
		testdata = testvalues[:arraylength]

		self.gentest =  bytes([x for x,y in zip(itertools.cycle(testdata), range(arraylength))])


	########################################################
	def test_bsum_general_function_A1(self):
		"""Test asum  - Array code bytes. General test.
		"""
		result = bytesfunc.bsum(self.gentest)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_B1(self):
		"""Test asum  - Array code bytes. Test optional maxlen parameter.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50)
		self.assertEqual(result, sum(self.gentest[:50]))


	########################################################
	def test_bsum_general_function_C1(self):
		"""Test asum  - Array code bytes. Test optional matherrors parameter.
		"""
		result = bytesfunc.bsum(self.gentest, matherrors=True)
		self.assertEqual(result, sum(self.gentest))



	########################################################
	def test_bsum_general_function_E1(self):
		"""Test asum  - Array code bytes. Test optional maxlen, matherrors parameters together.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50, matherrors=True)
		self.assertEqual(result, sum(self.gentest[:50]))



##############################################################################



##############################################################################
class bsum_general_even_bytearray(unittest.TestCase):
	"""Test asum for basic general function operation.
	op_template_general
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# The size of the test arrays. 
		arraylength = 256

		if 'even' == 'odd':
			arraylength = arraylength + 3

		# This produces a list of values.
		testvalues = list(range(0, 256))
		testdata = testvalues[:arraylength]

		self.gentest =  bytearray([x for x,y in zip(itertools.cycle(testdata), range(arraylength))])


	########################################################
	def test_bsum_general_function_A1(self):
		"""Test asum  - Array code bytearray. General test.
		"""
		result = bytesfunc.bsum(self.gentest)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_B1(self):
		"""Test asum  - Array code bytearray. Test optional maxlen parameter.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50)
		self.assertEqual(result, sum(self.gentest[:50]))


	########################################################
	def test_bsum_general_function_C1(self):
		"""Test asum  - Array code bytearray. Test optional matherrors parameter.
		"""
		result = bytesfunc.bsum(self.gentest, matherrors=True)
		self.assertEqual(result, sum(self.gentest))



	########################################################
	def test_bsum_general_function_E1(self):
		"""Test asum  - Array code bytearray. Test optional maxlen, matherrors parameters together.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50, matherrors=True)
		self.assertEqual(result, sum(self.gentest[:50]))



##############################################################################



##############################################################################
class bsum_general_odd_bytearray(unittest.TestCase):
	"""Test asum for basic general function operation.
	op_template_general
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# The size of the test arrays. 
		arraylength = 256

		if 'odd' == 'odd':
			arraylength = arraylength + 3

		# This produces a list of values.
		testvalues = list(range(0, 256))
		testdata = testvalues[:arraylength]

		self.gentest =  bytearray([x for x,y in zip(itertools.cycle(testdata), range(arraylength))])


	########################################################
	def test_bsum_general_function_A1(self):
		"""Test asum  - Array code bytearray. General test.
		"""
		result = bytesfunc.bsum(self.gentest)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_B1(self):
		"""Test asum  - Array code bytearray. Test optional maxlen parameter.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50)
		self.assertEqual(result, sum(self.gentest[:50]))


	########################################################
	def test_bsum_general_function_C1(self):
		"""Test asum  - Array code bytearray. Test optional matherrors parameter.
		"""
		result = bytesfunc.bsum(self.gentest, matherrors=True)
		self.assertEqual(result, sum(self.gentest))



	########################################################
	def test_bsum_general_function_E1(self):
		"""Test asum  - Array code bytearray. Test optional maxlen, matherrors parameters together.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50, matherrors=True)
		self.assertEqual(result, sum(self.gentest[:50]))



##############################################################################



##############################################################################
class bsum_parameter_bytes(unittest.TestCase):
	"""Test asum for basic parameter tests.
	op_template_params
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""

		arraylength = 96

		self.gentest =  bytes([100] * arraylength)


	########################################################
	def test_bsum_param_function_A1(self):
		"""Test asum  - Array code bytes. Test invalid parameter type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(1)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_A2(self):
		"""Test asum  - Array code bytes. Test invalid parameter type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum('xxxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum('xxxxx')


	########################################################
	def test_bsum_param_function_B1(self):
		"""Test asum  - Array code bytes. Test missing parameter.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum()


	########################################################
	def test_bsum_param_function_B2(self):
		"""Test asum  - Array code bytes. Test excess parameters.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, 5, 2, 1)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(self.gentest, 2, 3)


	########################################################
	def test_bsum_param_function_C1(self):
		"""Test asum  - Array code bytes. Test invalid keyword parameter name.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, xxxx=5)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(self.gentest, xxxx=5)


	########################################################
	def test_bsum_param_function_D1(self):
		"""Test asum  - Array code bytes. Test invalid maxlen keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, maxlen='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_D2(self):
		"""Test asum  - Array code bytes. Test invalid matherrors keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, matherrors='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


##############################################################################



##############################################################################
class bsum_parameter_bytearray(unittest.TestCase):
	"""Test asum for basic parameter tests.
	op_template_params
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""

		arraylength = 96

		self.gentest =  bytearray([100] * arraylength)


	########################################################
	def test_bsum_param_function_A1(self):
		"""Test asum  - Array code bytearray. Test invalid parameter type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(1)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_A2(self):
		"""Test asum  - Array code bytearray. Test invalid parameter type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum('xxxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum('xxxxx')


	########################################################
	def test_bsum_param_function_B1(self):
		"""Test asum  - Array code bytearray. Test missing parameter.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum()


	########################################################
	def test_bsum_param_function_B2(self):
		"""Test asum  - Array code bytearray. Test excess parameters.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, 5, 2, 1)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(self.gentest, 2, 3)


	########################################################
	def test_bsum_param_function_C1(self):
		"""Test asum  - Array code bytearray. Test invalid keyword parameter name.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, xxxx=5)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(self.gentest, xxxx=5)


	########################################################
	def test_bsum_param_function_D1(self):
		"""Test asum  - Array code bytearray. Test invalid maxlen keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, maxlen='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_D2(self):
		"""Test asum  - Array code bytearray. Test invalid matherrors keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, matherrors='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


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
			f.write('bsum\n\n')
			trun = unittest.TextTestRunner(f)
			unittest.main(testRunner=trun)
	else:
		unittest.main()

##############################################################################
