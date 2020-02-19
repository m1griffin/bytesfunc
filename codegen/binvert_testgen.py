#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the unit tests for math operators with one variable.
# Language: Python 3.5
# Date:     08-Dec-2017
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


# ==============================================================================

import itertools
import codegen_common


# ==============================================================================

# This template is for invert. 
test_template_invert = '''

##############################################################################
class %(funclabel)s_general_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typecode)s(unittest.TestCase):
	"""Test for basic general tests.
	test_template_invert
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		if '%(arrayevenodd)s' == 'even':
			testdatasize = 320
		if '%(arrayevenodd)s' == 'odd':
			testdatasize = 319


		# Generate test data over the full data type range.
		xdata = list(itertools.islice(itertools.cycle(range(256)), testdatasize))


		self.data = %(typecode)s(xdata)
		self.datam = bytearray(xdata)
		self.dataout = bytearray([0]*len(self.data))

		# This inverts the unsignec char.
		self.expected = [255 - x for x in self.data]

		self.limited = len(self.data) // 2

		self.expectedlimit1 = self.expected[0:self.limited] + list(self.data)[self.limited:]
		self.expectedlimit2 = self.expected[0:self.limited] + list(self.dataout)[self.limited:]


	########################################################
	def test_%(funclabel)s_inplace(self):
		"""Test %(funclabel)s in place - Sequence type %(typecode)s.
		"""
		bytesfunc.%(funcname)s(self.datam %(nosimd)s)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_%(funclabel)s_inplace_maxlen(self):
		"""Test %(funclabel)s in place with array maxlen  - Sequence type %(typecode)s.
		"""
		bytesfunc.%(funcname)s(self.datam, maxlen=self.limited %(nosimd)s)

		for dataoutitem, expecteditem in zip(list(self.datam), self.expectedlimit1):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_%(funclabel)s_outputarray(self):
		"""Test %(funclabel)s to output array - Sequence type %(typecode)s.
		"""
		bytesfunc.%(funcname)s(self.data, self.dataout %(nosimd)s)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expected):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)


	########################################################
	def test_%(funclabel)s_outputarray_maxlen(self):
		"""Test %(funclabel)s to output array with array maxlen  - Sequence type %(typecode)s.
		"""
		bytesfunc.%(funcname)s(self.data, self.dataout, maxlen=self.limited %(nosimd)s)

		for dataoutitem, expecteditem in zip(list(self.dataout), self.expectedlimit2):
			# The behavour of assertEqual is modified by addTypeEqualityFunc.
			self.assertEqual(dataoutitem, expecteditem)



##############################################################################

'''


# ==============================================================================


# The template used to generate the tests for testing invalid parameter types.
param_invalid_template = '''

##############################################################################
class %(funclabel)s_param_errors_%(typecode)s(unittest.TestCase):
	"""Test %(funclabel)s for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		self.testarray1 = %(typecode)s(testdata)
		self.testarray2 = %(typecode)s(testdata)

		arraysize = len(self.testarray1)

		self.dataout = bytearray(itertools.repeat(0, arraysize))

		# Create some data array equivalents with an incompatible type.
		self.badarray1 = array.array('d', [float(x) for x in self.testarray1])

		self.baddataout = array.array('d', [float(x) for x in self.dataout])



	########################################################
	def test_%(funclabel)s_array_array_a1(self):
		"""Test %(funclabel)s as *array-array* for invalid type of input array - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.testarray1, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.badarray1, self.dataout)


	########################################################
	def test_%(funclabel)s_array_array_a2(self):
		"""Test %(funclabel)s as *array-array* for invalid type of output array - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.testarray1, self.dataout)

		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.testarray2, self.baddataout)


##############################################################################

'''

# ==============================================================================

# The template used to generate the tests for testing invalid parameter types
# for maxlen.
param_invalid_opt_template = '''

##############################################################################
class %(funclabel)s_opt_param_errors_%(typecode)s(unittest.TestCase):
	"""Test %(funclabel)s for invalid maxlen parameters.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

		self.inparray1a = %(typecode)s(testdata)
		self.inparray1b = %(typecode)s(testdata)

		self.inparray2a = bytearray(testdata)
		self.inparray2b = bytearray(testdata)

		arraysize = len(self.inparray1a)

		self.dataout = bytearray(itertools.repeat(0, arraysize))

		self.testmaxlen = len(self.inparray1a) // 2


	########################################################
	def test_%(funclabel)s_array_none_a1(self):
		"""Test %(funclabel)s as *array-none* for maxlen='a' - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray2a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray2b, maxlen='a')


	########################################################
	def test_%(funclabel)s_array_none_a2(self):
		"""Test %(funclabel)s as *array-none* for nosimd='a' - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray2a, nosimd=False)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray2b, nosimd='a')


	########################################################
	def test_%(funclabel)s_array_array_b1(self):
		"""Test %(funclabel)s as *array-array* for maxlen='a' - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray1a, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray1b, self.dataout, maxlen='a')


	########################################################
	def test_%(funclabel)s_array_array_b2(self):
		"""Test %(funclabel)s as *array-array* for nosimd='a' - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray1a, self.dataout, nosimd=False)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray1b, self.dataout, nosimd='a')


	########################################################
	def test_%(funclabel)s_array_none_c1(self):
		"""Test %(funclabel)s as *array-none* for matherrors=True (unsupported option) - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray2a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray2b, matherrors=True)


	########################################################
	def test_%(funclabel)s_array_array_d1(self):
		"""Test %(funclabel)s as *array-array* for matherrors=True (unsupported option) - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray1a, self.dataout, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray1b, self.dataout, matherrors=True)


	########################################################
	def test_%(funclabel)s_no_params_e1(self):
		"""Test %(funclabel)s with no parameters - Sequence type %(typecode)s.
		"""
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s()


##############################################################################

'''

# ==============================================================================


# ==============================================================================

# The template used to generate the tests for testing invalid sequence length
# errors.
param_invalid_seqlen_template = '''

##############################################################################
class %(funcname)s_seqlen_param_errors_%(typecode)s(unittest.TestCase):
	"""Test %(funcname)s for invalid sequence lengths. Only parameter patterns
	which have more than one sequence can be tested.
	param_invalid_seqlen_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""
		testdata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		testdatashort = [1, 2, 3, 4, 5]

		self.inparray = %(typecode)s(testdata)
		self.inparrayshort = %(typecode)s(testdatashort)

		self.dataout = bytearray([0] * len(testdata))
		self.dataoutshort = bytearray([0] * len(testdatashort))


	########################################################
	def test_%(funclabel)s_array_array_a1(self):
		"""Test %(funclabel)s as *array-array* for mismatched sequence length - Sequence type %(typecode)s
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparrayshort, self.dataout)


	########################################################
	def test_%(funclabel)s_array_array_a2(self):
		"""Test %(funclabel)s as *array-array* for mismatched sequence length - Sequence type %(typecode)s
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.inparray, self.dataout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.inparray, self.dataoutshort)


##############################################################################

'''

# ==============================================================================


# ==============================================================================

# The template used to generate the tests for testing invalid parameter types
# for when the output is immutable.
param_seq_immutable_template = '''

##############################################################################
class %(funcname)s_seq_immutable_param_errors(unittest.TestCase):
	"""Test %(funcname)s for immutable output sequence.
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
	def test_%(funclabel)s_array_none_a1(self):
		"""Test %(funclabel)s as *array-none* for output seq immutable.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.bytearrayinp)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.bytesinp)


	########################################################
	def test_%(funclabel)s_array_array_a2(self):
		"""Test %(funclabel)s as *array-array* for output seq immutable.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.bytesinp, self.bytearrayout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.bytesinp, self.bytesout)



	########################################################
	def test_%(funclabel)s_array_array_a3(self):
		"""Test %(funclabel)s as *array-array* for output seq immutable.
		"""
		# This version is expected to pass.
		bytesfunc.%(funcname)s(self.bytearrayinp, self.bytearrayout)


		# This is the actual test.
		with self.assertRaises(TypeError):
			bytesfunc.%(funcname)s(self.bytearrayinp, self.bytesout)


##############################################################################

'''

# ==============================================================================

# ==============================================================================


def makedata():
	'''Make the combinations of data options for tests.
	'''
	typecode = [('typecode', x) for x in ('bytes', 'bytearray')]
	arrayevenodd = (('arrayevenodd', 'even'), ('arrayevenodd', 'odd'))
	simdpresent = (('simdpresent', 'nosimd'), ('simdpresent', 'withsimd'))

	# This creates all the combinations of test data.
	combos = [dict(x) for x in itertools.product(typecode, arrayevenodd, simdpresent)]

	nosimd = {'nosimd' : {'nosimd' : ', nosimd=True'}, 'withsimd' : {'nosimd' : ''}}

	# Update with the test data. These values don't represent independent combinations,
	# but rather just additional data that goes along with other items already present.
	for x in combos:
		x.update(nosimd[x['simdpresent']])

	return combos

# ==============================================================================



# ==============================================================================

# This defines the module name.
modulename = 'bytesfunc'
# We import the array module to test for invalid parameters.
arrayimport = 'import array'


funcname = 'invert'
filenamebase = 'test_' + funcname
filename = filenamebase + '.py'
headerdate = codegen_common.FormatHeaderData(filenamebase, '30-Jan-2020', funcname)

# Add additional header data.
headerdate['modulename'] = modulename
headerdate['arrayimport'] = arrayimport

pyoperator = '~'

with open(filename, 'w') as f:
	# The copyright header.
	f.write(codegen_common.HeaderTemplate % headerdate)


	# Test for basic operation.
	for funcdata in makedata():
		funcdata['funclabel'] = funcname
		funcdata['funcname'] = funcname
		funcdata['pyoperator'] = pyoperator

		f.write(test_template_invert % funcdata)

		#####

	for functype in ('bytes', 'bytearray'):
		funcdata = {'funclabel' : funcname, 'funcname' : funcname, 'pyoperator' : pyoperator,
			'typecode' : functype}

		# Test for invalid parameters. One template should work for all 
		# functions of this style.
		f.write(param_invalid_template % funcdata)

		# Test for invalid optional parameters such as maxlen.
		f.write(param_invalid_opt_template % funcdata)


	# Check for sequence length mismatch. 
	for functype in ('bytes', 'bytearray'):
		f.write(param_invalid_seqlen_template % {'funclabel' : funcname, 'funcname' : funcname, 'typecode' : functype})


	# Check for immutable outputs.
	f.write(param_seq_immutable_template % {'funclabel' : funcname, 'funcname' : funcname})


	f.write(codegen_common.testendtemplate % {'funcname' : funcname, 'modulename' : modulename})

# ==============================================================================

