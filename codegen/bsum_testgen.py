#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the unit tests for bsum.
# Language: Python 3.6
# Date:     19-Jan-2020
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

import itertools
import codegen_common

# ==============================================================================

# ==============================================================================

# The basic template for testing each array type for operator function.
op_template_general = '''

##############################################################################
class bsum_general_%(arrayevenodd)s_%(typecode)s(unittest.TestCase):
	"""Test bsum for basic general function operation.
	op_template_general
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		# The size of the test arrays. 
		arraylength = 256

		if '%(arrayevenodd)s' == 'odd':
			arraylength = arraylength + 3

		# This produces a list of values.
		testvalues = list(range(0, 256))
		testdata = testvalues[:arraylength]

		self.gentest =  %(typecode)s([x for x,y in zip(itertools.cycle(testdata), range(arraylength))])


	########################################################
	def test_bsum_general_function_A1(self):
		"""Test bsum  - Array code %(typecode)s. General test.
		"""
		result = bytesfunc.bsum(self.gentest)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_B1(self):
		"""Test bsum  - Array code %(typecode)s. Test optional maxlen parameter.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50)
		self.assertEqual(result, sum(self.gentest[:50]))


	########################################################
	def test_bsum_general_function_C1(self):
		"""Test bsum  - Array code %(typecode)s. Test optional matherrors parameter.
		"""
		result = bytesfunc.bsum(self.gentest, matherrors=True)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_D1(self):
		"""Test bsum  - Array code %(typecode)s. Test optional nosimd parameter.
		"""
		result = bytesfunc.bsum(self.gentest, nosimd=True)
		self.assertEqual(result, sum(self.gentest))


	########################################################
	def test_bsum_general_function_E1(self):
		"""Test bsum  - Array code %(typecode)s. Test optional maxlen, matherrors, nosimd parameters parameters together.
		"""
		result = bytesfunc.bsum(self.gentest, maxlen=50, nosimd=True, matherrors=True)
		self.assertEqual(result, sum(self.gentest[:50]))



##############################################################################

'''

# ==============================================================================


# The basic template for testing each array type for parameter errors.
op_template_params = '''

##############################################################################
class bsum_parameter_%(typecode)s(unittest.TestCase):
	"""Test bsum for basic parameter tests.
	op_template_params
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""

		arraylength = 96

		self.gentest =  %(typecode)s([100] * arraylength)


	########################################################
	def test_bsum_param_function_A1(self):
		"""Test bsum  - Array code %(typecode)s. Test invalid parameter type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(1)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_A2(self):
		"""Test bsum  - Array code %(typecode)s. Test invalid parameter type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum('xxxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum('xxxxx')


	########################################################
	def test_bsum_param_function_B1(self):
		"""Test bsum  - Array code %(typecode)s. Test missing parameter.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum()


	########################################################
	def test_bsum_param_function_B2(self):
		"""Test bsum  - Array code %(typecode)s. Test excess parameters.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, 5, 2, 2, 1)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(self.gentest, 2, 3)


	########################################################
	def test_bsum_param_function_C1(self):
		"""Test bsum  - Array code %(typecode)s. Test invalid keyword parameter name.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, xxxx=5)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(self.gentest, xxxx=5)


	########################################################
	def test_bsum_param_function_D1(self):
		"""Test bsum  - Array code %(typecode)s. Test invalid maxlen keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, maxlen='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_D2(self):
		"""Test bsum  - Array code %(typecode)s. Test invalid matherrors keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, matherrors='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


	########################################################
	def test_bsum_param_function_D3(self):
		"""Test bsum  - Array code %(typecode)s. Test invalid nosimd keyword type.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.bsum(self.gentest, nosimd='xxxx')

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = sum(1)


##############################################################################

'''

# ==============================================================================



# ==============================================================================

funcname = 'bsum'

filenamebase = 'test_' + funcname
filename = filenamebase + '.py'
headerdate = codegen_common.FormatHeaderData(filenamebase, '11-Jun-2014', funcname)


# This defines the module name.
modulename = 'bytesfunc'
# We don't import the array module for bytesfunc.
arrayimport = ''

# Add additional header data.
headerdate['modulename'] = modulename
headerdate['arrayimport'] = arrayimport


with open(filename, 'w') as f:
	# The copyright header.
	f.write(codegen_common.HeaderTemplate % headerdate)

	# Check each array type.
	for arraycode in ('bytes', 'bytearray'):

		f.write(op_template_general % {'typecode' : arraycode, 'arrayevenodd' : 'even'})
		f.write(op_template_general % {'typecode' : arraycode, 'arrayevenodd' : 'odd'})

	# Check parameters.
	for arraycode in ('bytes', 'bytearray'):
		f.write(op_template_params % {'typecode' : arraycode})


	#####
	# The code which initiates the unit test.

	f.write(codegen_common.testendtemplate % {'funcname' : funcname, 'testprefix' : 'bf'})

