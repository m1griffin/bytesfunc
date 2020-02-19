#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the unit tests for bmax and bmin.
# Language: Python 3.6
# Date:     31-Oct-2019
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

# ==============================================================================


# The basic template for testing each array type for operator function.
op_template_general = '''

##############################################################################
class %(funclabel)s_general_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typecode)s(unittest.TestCase):
	"""Test %(funclabel)s for basic general function operation.
	op_template_general
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
		self.gentest = %(typecode)s([x for x,y in zip(itertools.cycle(gendata), range(arraylength))])
		self.inctest = %(typecode)s([x for x,y in zip(itertools.cycle(incdata), range(arraylength))])
		self.dectest = %(typecode)s([x for x,y in zip(itertools.cycle(decdata), range(arraylength))])
		self.maxvaltest = %(typecode)s([x for x,y in zip(itertools.cycle(maxvaldata), range(arraylength))])
		self.minvaltest = %(typecode)s([x for x,y in zip(itertools.cycle(minvaldata), range(arraylength))])


	########################################################
	def test_%(funclabel)s_general_function_01(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. General test %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		result = bytesfunc.b%(funcname)s(self.gentest %(nosimd)s)
		self.assertEqual(result, %(funcname)s(self.gentest))


	########################################################
	def test_%(funclabel)s_general_function_02(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test increasing values %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		result = bytesfunc.b%(funcname)s(self.inctest %(nosimd)s)
		self.assertEqual(result, %(funcname)s(self.inctest))


	########################################################
	def test_%(funclabel)s_general_function_03(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test decreasing values %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		result = bytesfunc.b%(funcname)s(self.dectest %(nosimd)s)
		self.assertEqual(result, %(funcname)s(self.dectest))


	########################################################
	def test_%(funclabel)s_general_function_04(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test finding max for data type %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		result = bytesfunc.b%(funcname)s(self.maxvaltest %(nosimd)s)
		self.assertEqual(result, %(funcname)s(self.maxvaltest))


	########################################################
	def test_%(funclabel)s_general_function_05(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test finding value from array that contains min for data type %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		result = bytesfunc.b%(funcname)s(self.minvaltest %(nosimd)s)
		self.assertEqual(result, %(funcname)s(self.minvaltest))


	########################################################
	def test_%(funclabel)s_general_function_06(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test optional maxlen parameter %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		result = bytesfunc.b%(funcname)s(self.maxvaltest, maxlen=5 %(nosimd)s)
		self.assertEqual(result, %(funcname)s(self.maxvaltest[:5]))



##############################################################################

'''


# ==============================================================================


# The basic template for testing each array type for parameter errors.
op_template_params = '''

##############################################################################
class %(funclabel)s_parameter_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typecode)s(unittest.TestCase):
	"""Test %(funclabel)s for basic parameter tests.
	op_template_params
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

		arraylength = 96 + arrayextension


		MaxVal = 255
		MinVal = 0

		self.gentest = %(typecode)s([MaxVal // 2] * arraylength)


	########################################################
	def test_%(funclabel)s_param_function_01(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test invalid parameter type %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.b%(funcname)s(1 %(nosimd)s)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = %(funcname)s(1)


	########################################################
	def test_%(funclabel)s_param_function_02(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test missing parameter %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.b%(funcname)s()

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = %(funcname)s()


	########################################################
	def test_%(funclabel)s_param_function_03(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test excess parameters %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.b%(funcname)s(self.gentest, 5, 2, 2 %(nosimd)s)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = %(funcname)s(self.gentest, 2)


	########################################################
	def test_%(funclabel)s_param_function_04(self):
		"""Test %(funclabel)s  - Sequence type %(typecode)s. Test invalid keyword parameter %(arrayevenodd)s length array %(simdpresent)s SIMD.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.b%(funcname)s(self.gentest, xxxx=5 %(nosimd)s)

		# Check that the exception raised corresponds to the native Python behaviour.
		with self.assertRaises(TypeError):
			result = %(funcname)s(self.gentest, xxxx=5)


##############################################################################

'''

# ==============================================================================


# ==============================================================================

# The functions which are implemented by this program.
completefuncnames = ('bmax', 'bmin')


# The name of the function without the leading 'a'.
optype = {'bmax' : 'max', 
			'bmin' : 'min', 
}


# ==============================================================================

# This is used to generate test template data for tests.
def gentestdata(funcname):
	""" Generate test template data for tests.
	funcname (string): - The name of the function.
	Returns: (list) - A list of dictionaries containing the keys and
		values to generate individual test functions.
	"""

	# These are the different test values we will combine in various ways.
	arraycode = [('typecode', x) for x in ('bytes', 'bytearray')]
	hassimd = (('simdpresent', 'with'), ('simdpresent', 'without'))
	arraylen = (('arrayevenodd', 'even'), ('arrayevenodd', 'odd'))

	# The product function produces all possible combinations.
	combos = list(itertools.product(arraycode, hassimd, arraylen))


	# Convert the data into a list of dictionaries.
	testdata = [dict(x) for x in combos]

	nosimd = {'with' : '', 'without' : ', nosimd=True'}

	# Add in the data that doesn't change.
	for x in testdata:
		x['nosimd'] = nosimd[x['simdpresent']]
		x['funclabel'] = funcname
		x['funcname'] = optype[funcname]

	return testdata


# ==============================================================================

# This defines the module name.
modulename = 'bytesfunc'
# We don't import the array module for bytesfunc.
arrayimport = ''

for funcname in completefuncnames:


	# Data for the copyright header files.
	headerdate = codegen_common.FormatHeaderData('test_%s' % funcname, '01-Nov-2019', funcname)

	# Add additional header data.
	headerdate['modulename'] = modulename
	headerdate['arrayimport'] = arrayimport


	with open('test_%s.py' % funcname, 'w') as f:
		# The copyright header.
		f.write(codegen_common.HeaderTemplate % headerdate)

		# Output the generated code for basic operator tests.
		for datarec in gentestdata(funcname):
			f.write(op_template_general % datarec)
			f.write(op_template_params % datarec)



		# End of the tests.
		f.write(codegen_common.testendtemplate % {'funcname' : funcname, 'modulename' : modulename})


# ==============================================================================
