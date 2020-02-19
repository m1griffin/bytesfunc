#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the unit tests for compare operations.
# Language: Python 3.5
# Date:     01-Nov-2019
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

# This template is for compare operations.
test_template_comp = ''' 

##############################################################################
class %(funcname)s_general_%(arrayevenodd)s_arraysize_%(simdpresent)s_simd_%(typecode)s_%(count)s(unittest.TestCase):
	"""Test for basic general function operation using numeric data.
	test_template_comp
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""
		if '%(arrayevenodd)s' == 'even':
			testdatasize = 512
		if '%(arrayevenodd)s' == 'odd':
			testdatasize = 511


		self.data_array_num = %(typecode)s(list(itertools.islice(itertools.cycle(%(data_array_num)s), testdatasize)))
		self.param_array_num_pass = %(param_array_num_pass)s
		self.param_array_num_fail = %(param_array_num_fail)s

		self.data_num_array = %(typecode)s(list(itertools.islice(itertools.cycle(%(data_num_array)s), testdatasize)))
		self.param_num_array_pass = %(param_num_array_pass)s
		self.param_num_array_fail = %(param_num_array_fail)s

		self.data_array_array = %(typecode)s(list(itertools.islice(itertools.cycle(%(data_array_array)s), testdatasize)))
		self.data_array_array_pass = %(typecode)s(list(itertools.islice(itertools.cycle(%(data_array_array_pass)s), testdatasize)))
		self.data_array_array_fail = %(typecode)s(list(itertools.islice(itertools.cycle(%(data_array_array_fail)s), testdatasize)))


	########################################################
	def test_%(funcname)s_basic_array_num_a1(self):
		"""Test %(funcname)s as *array-num* for basic function - Sequence type %(typecode)s.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x %(pyoperator)s testval for x in self.data_array_num])

				result = bytesfunc.%(funcname)s(self.data_array_num, testval %(nosimd)s)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_array_num_a2(self):
		"""Test %(funcname)s as *array-num* for basic function - Sequence type %(typecode)s.
		"""
		for testval in self.param_array_num_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([x %(pyoperator)s testval for x in self.data_array_num])

				result = bytesfunc.%(funcname)s(self.data_array_num, testval %(nosimd)s)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_array_num_a3(self):
		"""Test %(funcname)s as *array-num* for basic function with array limit - Sequence type %(typecode)s.
		"""
		for testval in self.param_array_num_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_array_num) // 2

				expected = all([x %(pyoperator)s testval for x in self.data_array_num[0:limited]])

				result = bytesfunc.%(funcname)s(self.data_array_num, testval, maxlen=limited %(nosimd)s)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_num_array_b1(self):
		"""Test %(funcname)s as *num-array* for basic function - Sequence type %(typecode)s.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval %(pyoperator)s x for x in self.data_num_array])

				result = bytesfunc.%(funcname)s(testval, self.data_num_array %(nosimd)s)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_num_array_b2(self):
		"""Test %(funcname)s as *num-array* for basic function - Sequence type %(typecode)s.
		"""
		for testval in self.param_num_array_fail:
			with self.subTest(msg='Failed with parameter', testval = testval):

				expected = all([testval %(pyoperator)s x for x in self.data_num_array])

				result = bytesfunc.%(funcname)s(testval, self.data_num_array %(nosimd)s)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_num_array_b3(self):
		"""Test %(funcname)s as *num-array* for basic function with array limit - Sequence type %(typecode)s.
		"""
		for testval in self.param_num_array_pass:
			with self.subTest(msg='Failed with parameter', testval = testval):

				limited = len(self.data_num_array) // 2

				expected = all([testval %(pyoperator)s x for x in self.data_num_array[0:limited]])

				result = bytesfunc.%(funcname)s(testval, self.data_num_array, maxlen=limited %(nosimd)s)

				self.assertTrue(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_array_array_c1(self):
		"""Test %(funcname)s as *array-array* for basic function - Sequence type %(typecode)s.
		"""
		expected = all([x %(pyoperator)s y for (x, y) in zip(self.data_array_array, self.data_array_array_pass)])
		result = bytesfunc.%(funcname)s(self.data_array_array, self.data_array_array_pass %(nosimd)s)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_array_array_c2(self):
		"""Test %(funcname)s as *array-array* for basic function - Sequence type %(typecode)s.
		"""
		expected = all([x %(pyoperator)s y for (x, y) in zip(self.data_array_array, self.data_array_array_fail)])
		result = bytesfunc.%(funcname)s(self.data_array_array, self.data_array_array_fail %(nosimd)s)

		self.assertFalse(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


	########################################################
	def test_%(funcname)s_basic_array_array_c3(self):
		"""Test %(funcname)s as *array-array* for basic function with array limit - Sequence type %(typecode)s.
		"""
		limited = len(self.data_array_array) // 2

		expected = all([x %(pyoperator)s y for (x, y) in zip(self.data_array_array[0:limited], self.data_array_array_pass[0:limited])])

		result = bytesfunc.%(funcname)s(self.data_array_array, self.data_array_array_pass, maxlen=limited %(nosimd)s)

		self.assertTrue(result)
		self.assertIsInstance(result, bool)
		self.assertEqual(expected, result)


##############################################################################

'''


# ==============================================================================

# This template tests with numbers in various positions.
test_template_numpos = ''' 


##############################################################################
class %(funcname)s_numpos_%(typecode)s(unittest.TestCase):
	"""Test with a single fail value in different array positions.
	test_template_numpos
	"""


	########################################################
	def setUp(self):
		"""Initialise. The test data is generated from the script itself.
		"""
		self.testarraylen = 159

		test_data1 = [%(test_data1)s] * self.testarraylen
		self.data1 = %(typecode)s(test_data1)

		self.testval1 = self.data1[0]

		self.data1_fail = [%(test_data1)s] * self.testarraylen
		self.data1_fail[-1] = %(test_data1fail)s
		self.data1fail = %(typecode)s(self.data1_fail)

		test_data2 = [%(test_data2)s] * self.testarraylen
		self.data2 = %(typecode)s(test_data2)

		self.testval2 = self.data2[0]

		self.data2_fail = [%(test_data2)s] * self.testarraylen
		self.data2_fail[-1] = %(test_data2fail)s
		self.data2fail = %(typecode)s(self.data2_fail)



	########################################################
	def test_%(funcname)s_numpos_array_num_a1(self):
		"""Test %(funcname)s as *array-num* for failing with different data positions in array - Sequence type %(typecode)s.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x %(pyoperator)s self.testval2 for x in self.data1fail])

				result = bytesfunc.%(funcname)s(self.data1fail, self.testval2)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			# Shift the data one position.
			self.data1_fail.append(self.data1_fail.pop(0))
			self.data1fail = %(typecode)s(self.data1_fail)


	########################################################
	def test_%(funcname)s_numpos_num_array_b1(self):
		"""Test %(funcname)s as *num-array* for failing with different data positions in array - Sequence type %(typecode)s.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([self.testval1 %(pyoperator)s x for x in self.data2fail])

				result = bytesfunc.%(funcname)s(self.testval1, self.data2fail)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data2_fail.append(self.data2_fail.pop(0))
			self.data2fail = %(typecode)s(self.data2_fail)


	########################################################
	def test_%(funcname)s_numpos_array_array_c1(self):
		"""Test %(funcname)s as *array-array* for failing with different data positions in array 1 - Sequence type %(typecode)s.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x %(pyoperator)s y for x,y in zip(self.data1fail, self.data2)])

				result = bytesfunc.%(funcname)s(self.data1fail, self.data2)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data1_fail.append(self.data1_fail.pop(0))
			self.data1fail = %(typecode)s(self.data1_fail)


	########################################################
	def test_%(funcname)s_numpos_array_array_c2(self):
		"""Test %(funcname)s as *array-array* for failing with different data positions in array 2 - Sequence type %(typecode)s.
		"""
		for testpos in range(self.testarraylen):
			with self.subTest(msg='Failed with posistion', testpos = testpos):

				expected = all([x %(pyoperator)s y for x,y in zip(self.data1, self.data2fail)])

				result = bytesfunc.%(funcname)s(self.data1, self.data2fail)

				self.assertFalse(result)
				self.assertIsInstance(result, bool)
				self.assertEqual(expected, result)

			
			# Shift the data one position.
			self.data2_fail.append(self.data2_fail.pop(0))
			self.data2fail = %(typecode)s(self.data2_fail)


##############################################################################

'''



# ==============================================================================


# The template used to generate the tests for testing invalid array and
# numeric parameter types.
param_invalid_template = '''

##############################################################################
class %(funcname)s_param_errors_%(typecode)s(unittest.TestCase):
	"""Test for invalid array and numeric parameters.
	param_invalid_template
	"""


	########################################################
	def setUp(self):
		"""Initialise.
		"""

		self.data1 = %(typecode)s(%(test_op_x)s)
		self.data2 = %(typecode)s(%(test_op_y)s)

		self.testval1 = self.data1[-1]
		self.testval2 = self.data2[-1]
		

		# Create some sequence equivalents which are different than the correct ones.
		self.badarray1str = ''.join([str(x) for x in self.data1])
		self.badarray1list = list(self.data1)

		self.badarray2str = ''.join([str(x) for x in self.data2])
		self.badarray2list = list(self.data2)


	########################################################
	def test_%(funcname)s_array_num_a1(self):
		"""Test %(funcname)s as *array-num* for string sequence - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.badarray1str, self.testval2)


	########################################################
	def test_%(funcname)s_array_num_a2(self):
		"""Test %(funcname)s as *array-num* for list sequence - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.badarray1list, self.testval2)



	########################################################
	def test_%(funcname)s_array_num_b1(self):
		"""Test %(funcname)s as *array-num* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, -1)


	########################################################
	def test_%(funcname)s_array_num_b2(self):
		"""Test %(funcname)s as *array-num* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, 256)


	########################################################
	def test_%(funcname)s_array_num_b3(self):
		"""Test %(funcname)s as *array-num* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, 5.0)


	########################################################
	def test_%(funcname)s_array_num_b4(self):
		"""Test %(funcname)s as *array-num* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.testval2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, 'a')



	########################################################
	def test_%(funcname)s_num_array_c1(self):
		"""Test %(funcname)s as *num-array* for string sequence - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.testval1, self.badarray2str)


	########################################################
	def test_%(funcname)s_num_array_c2(self):
		"""Test %(funcname)s as *num-array* for list sequence - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.testval1, self.badarray2list)



	########################################################
	def test_%(funcname)s_num_array_d1(self):
		"""Test %(funcname)s as *num-array* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(-1, self.data2)


	########################################################
	def test_%(funcname)s_num_array_d2(self):
		"""Test %(funcname)s as *num-array* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(256, self.data2)


	########################################################
	def test_%(funcname)s_num_array_d3(self):
		"""Test %(funcname)s as *num-array* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(5.0, self.data2)


	########################################################
	def test_%(funcname)s_num_array_d4(self):
		"""Test %(funcname)s as *num-array* for incompatible number - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.testval1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s('a', self.data2)



	########################################################
	def test_%(funcname)s_array_array_e1(self):
		"""Test %(funcname)s as *array-array* for incompatible second array - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, self.badarray2str)


	########################################################
	def test_%(funcname)s_array_array_e2(self):
		"""Test %(funcname)s as *array-array* for incompatible second array - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.data2)
		

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, self.badarray2list)



	########################################################
	def test_%(funcname)s_array_array_f1(self):
		"""Test %(funcname)s as *array-array* for incompatible first array - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.data2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.badarray1str, self.data2)


	########################################################
	def test_%(funcname)s_array_array_f2(self):
		"""Test %(funcname)s as *array-array* for incompatible first array - Sequence type %(typecode)s.
		"""
		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.data1, self.data2)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.badarray1list, self.data2)



	########################################################
	def test_%(funcname)s_no_params_g1(self):
		"""Test %(funcname)s with no parameters - Sequence type %(typecode)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s()


	########################################################
	def test_%(funcname)s_too_many_params_g2(self):
		"""Test %(funcname)s with no parameters - Sequence type %(typecode)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.data1, self.data2, self.data1)


	########################################################
	def test_%(funcname)s_two_numeric_params_g3(self):
		"""Test %(funcname)s with two numeric parameters - Sequence type %(typecode)s.
		"""
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.testval1, self.testval2)



##############################################################################

'''

# ==============================================================================

# The template used to generate the tests for testing invalid parameter types
# for errors flag and maxlen.
param_invalid_opt_template = '''

##############################################################################
class %(funcname)s_param_errors_opt_%(typecode)s(unittest.TestCase):
	"""Test for invalid errors and maxlen parameters. The errors does not
	exist with these functions.
	param_invalid_opt_template
	"""

	########################################################
	def setUp(self):
		"""Initialise.
		"""

		self.inparray1a = %(typecode)s(%(test_op_x)s)
		self.inparray1b = copy.copy(self.inparray1a)
		self.inparray2a = %(typecode)s(%(test_op_y)s)
		self.inparray2b = copy.copy(self.inparray2a)

		self.testmaxlen = len(self.inparray1a) // 2


	########################################################
	def test_%(funcname)s_array_num_a1(self):
		"""Test %(funcname)s as *array-num* for matherrors=True - Sequence type %(typecode)s.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.inparray1a, inpvalue)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.inparray1a, inpvalue, matherrors=True)


	########################################################
	def test_%(funcname)s_array_num_a2(self):
		"""Test %(funcname)s as *array-num* for maxlen='a' - Sequence type %(typecode)s.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.inparray1a, inpvalue, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.inparray1a, inpvalue, maxlen='a')


	########################################################
	def test_%(funcname)s_array_num_a3(self):
		"""Test %(funcname)s as *array-num* for nosimd='a' - Sequence type %(typecode)s.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.inparray1a, inpvalue, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.inparray1a, inpvalue, nosimd='a')


	########################################################
	def test_%(funcname)s_num_array_c1(self):
		"""Test %(funcname)s as *num-array* for matherrors=True - Sequence type %(typecode)s.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(inpvalue, self.inparray1a)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(inpvalue, self.inparray1a, matherrors=True)


	########################################################
	def test_%(funcname)s_num_array_c2(self):
		"""Test %(funcname)s as *num-array* for maxlen='a' - Sequence type %(typecode)s.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(inpvalue, self.inparray1a, maxlen=self.testmaxlen)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(inpvalue, self.inparray1a, maxlen='a')


	########################################################
	def test_%(funcname)s_num_array_c3(self):
		"""Test %(funcname)s as *num-array* for nosimd='a' - Sequence type %(typecode)s.
		"""
		inpvalue = self.inparray2a[0]

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(inpvalue, self.inparray1a, nosimd=True)


		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(inpvalue, self.inparray1a, nosimd='a')


	########################################################
	def test_%(funcname)s_array_array_e1(self):
		"""Test %(funcname)s as *array-array* for matherrors=True - Sequence type %(typecode)s.
		"""

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.inparray1a, self.inparray2a)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.inparray1a, self.inparray2a, matherrors=True)


	########################################################
	def test_%(funcname)s_array_array_e2(self):
		"""Test %(funcname)s as *array-array* for maxlen='a' - Sequence type %(typecode)s.
		"""

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.inparray1a, self.inparray2a, maxlen=self.testmaxlen)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.inparray1a, self.inparray2a, maxlen='a')


	########################################################
	def test_%(funcname)s_array_array_e3(self):
		"""Test %(funcname)s as *array-array* for nosimd='a' - Sequence type %(typecode)s.
		"""

		# This version is expected to pass.
		result = bytesfunc.%(funcname)s(self.inparray1a, self.inparray2a, nosimd=True)

		# This is the actual test.
		with self.assertRaises(TypeError):
			result = bytesfunc.%(funcname)s(self.inparray1a, self.inparray2a, nosimd='a')


##############################################################################

'''

# ==============================================================================


# ==============================================================================

# This data is used to create tests for test_template_numpos.

# First parameter.
numposdata1 = {
	'eq' : '5',
	'gt' : '6',
	'ge' : '6',
	'lt' : '5',
	'le' : '6',
	'ne' : '5',
}

# First parameter to cause no match.
numposdata1fail = {
	'eq' : '4',
	'gt' : '5',
	'ge' : '4',
	'lt' : '7',
	'le' : '8',
	'ne' : '6',
}


# Second parameter.
numposdata2 = {
	'eq' : '5',
	'gt' : '5',
	'ge' : '5',
	'lt' : '6',
	'le' : '7',
	'ne' : '6',
}

# Second parameter to cause no match.
numposdata2fail = {
	'eq' : '4',
	'gt' : '7',
	'ge' : '7',
	'lt' : '4',
	'le' : '5',
	'ne' : '5',
}


# ==============================================================================

# Test data for the template test_template_comp.
# This contains lists of test values to allow multiple tests sets
# with the same template. This allows a broader range of data to
# be tested.
# This is in a format which is easier to view in an editor, rather than
# easier to extract.
testdata = {
	'eq' : 
	{
	'data_array_num' :        ([10, 10, 10],           [210, 210, 210]),
	'param_array_num_pass' :  ([10, 10, 10, 10, 10],   [210, 210, 210, 210, 210]),
	'param_array_num_fail' :  ([210, 11, 0, 255, 210], [10, 211, 0, 255, 10]),

	'param_num_array_pass' :  ([10, 10, 10, 10, 10],   [210, 210, 210, 210, 210]),
	'param_num_array_fail' :  ([210, 11, 0, 255, 210], [10, 211, 0, 255, 10]),
	'data_num_array' :        ([10, 10, 10],           [210, 210, 210]),

	'data_array_array' :      ([10, 10, 10],           [210, 210, 210]),
	'data_array_array_pass' : ([10, 10, 10],           [210, 210, 210]),
	'data_array_array_fail' : ([12, 9, 245],           [212, 9, 45]),
	},

	'gt' : 
	{
	'data_array_num' :        ([10, 20, 30],           [210, 220, 230]),
	'param_array_num_pass' :  ([9, 2, 0, 5, 6],        [60, 70, 80, 90, 100]),
	'param_array_num_fail' :  ([31, 35, 210, 255, 40], [231, 232, 233, 234, 255]),

	'param_num_array_pass' :  ([10, 20, 30],           [222, 255, 237, 241, 250]),
	'param_num_array_fail' :  ([0, 1, 4, 3, 2],        [100, 200, 0, 3, 10]),
	'data_num_array' :        ([9, 8, 9, 5, 6],        [219, 218, 221]),

	'data_array_array' :      ([10, 11, 22],           [250, 100, 150]),
	'data_array_array_pass' : ([9, 8, 0],              [99, 98, 88]),
	'data_array_array_fail' : ([253, 100, 200],        [251, 252, 255]),
	},

	'ge' : 
	{
	'data_array_num' :        ([10, 20, 30],           [210, 220, 230],           [10, 10, 10]),
	'param_array_num_pass' :  ([9, 2, 0, 5, 6],        [60, 70, 80, 90, 100],     [10, 10, 10, 10, 10]),
	'param_array_num_fail' :  ([31, 35, 210, 255, 40], [231, 232, 233, 234, 255], [210, 11, 50, 255, 210]),

	'param_num_array_pass' :  ([10, 20, 30],           [222, 255, 237, 241, 250], [10, 10, 10, 10, 10]),
	'param_num_array_fail' :  ([0, 1, 4, 3, 2],        [100, 200, 0, 3, 10],      [8, 7, 0, 1, 9]),
	'data_num_array' :        ([9, 8, 9, 5, 6],        [219, 218, 221],           [10, 10, 10]),

	'data_array_array' :      ([10, 11, 22],           [250, 100, 150],           [10, 10, 10]),
	'data_array_array_pass' : ([9, 8, 0],              [99, 98, 88],              [10, 10, 10]),
	'data_array_array_fail' : ([253, 100, 200],        [251, 252, 255],           [12, 109, 245]),
	},


	'lt' : 
	{
	'data_array_num' :        ([10, 20, 30],           [210, 220, 230]),
	'param_array_num_pass' :  ([31, 35, 210, 255, 40], [231, 232, 233, 234, 255]),
	'param_array_num_fail' :  ([9, 2, 0, 5, 6],        [60, 70, 80, 90, 100]),

	'param_num_array_pass' :  ([0, 1, 4, 3, 2],        [100, 200, 0, 3, 10]),
	'param_num_array_fail' :  ([10, 20, 30],           [222, 255, 237, 241, 250]),
	'data_num_array' :        ([9, 8, 9, 5, 6],        [219, 218, 221]),

	'data_array_array' :      ([10, 11, 22],           [250, 100, 150]),
	'data_array_array_pass' : ([253, 100, 200],        [251, 252, 255]),
	'data_array_array_fail' : ([9, 8, 0],              [99, 98, 88]),
	},

	'le' : 
	{
	'data_array_num' :        ([10, 20, 30],           [210, 220, 230],           [10, 10, 10]),
	'param_array_num_pass' :  ([31, 35, 210, 255, 40], [231, 232, 233, 234, 255], [10, 10, 10, 10, 10]),
	'param_array_num_fail' :  ([9, 2, 0, 5, 6],        [60, 70, 80, 90, 100],     [9, 7, 5, 8, 0]),

	'param_num_array_pass' :  ([0, 1, 4, 3, 2],        [100, 200, 0, 3, 10],      [10, 10, 10, 10, 10]),
	'param_num_array_fail' :  ([10, 20, 30],           [222, 255, 237, 241, 250], [210, 11, 50, 255, 210]),
	'data_num_array' :        ([9, 8, 9, 5, 6],        [219, 218, 221],           [10, 10, 10]),

	'data_array_array' :      ([10, 11, 22],           [250, 100, 150],           [10, 10, 10]),
	'data_array_array_pass' : ([253, 100, 200],        [251, 252, 255],           [10, 10, 10]),
	'data_array_array_fail' : ([9, 8, 0],              [99, 98, 88],              [9, 7, 5, 8, 0]),
	},

	'ne' : 
	{
	'data_array_num' :        ([10, 10, 10],           [210, 210, 210]),
	'param_array_num_pass' :  ([210, 11, 0, 255, 210], [10, 211, 0, 255, 10]),
	'param_array_num_fail' :  ([10, 10, 10, 10, 10],   [210, 210, 210, 210, 210]),

	'param_num_array_pass' :  ([210, 11, 0, 255, 210], [10, 211, 0, 255, 10]),
	'param_num_array_fail' :  ([10, 10, 10, 10, 10],   [210, 210, 210, 210, 210]),
	'data_num_array' :        ([10, 10, 10],           [210, 210, 210]),

	'data_array_array' :      ([10, 10, 10],           [210, 210, 210]),
	'data_array_array_pass' : ([12, 9, 245],           [212, 9, 45]),
	'data_array_array_fail' : ([10, 10, 10],           [210, 210, 210]),
	},

}


# ==============================================================================

# Used for testing parameters.
param_test_data = {
	'eq' : {'test_op_x' : [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5], 
			'test_op_y' : [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5], 
			'test_op_y_fail' : [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6]},
	'gt' : {'test_op_x' : [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6], 
			'test_op_y' : [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5], 
			'test_op_y_fail' : [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]},
	'ge' : {'test_op_x' : [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6], 
			'test_op_y' : [6,5,6,5,6,5,6,5,6,5,6,5,6,5,6,5,6,5,6,5], 
			'test_op_y_fail' : [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]},
	'lt' : {'test_op_x' : [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5], 
			'test_op_y' : [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6], 
			'test_op_y_fail' : [4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3]},
	'le' : {'test_op_x' : [6,5,6,5,6,5,6,5,6,5,6,5,6,5,6,5,6,5,6,5], 
			'test_op_y' : [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6], 
			'test_op_y_fail' : [4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3,4,3]},
	'ne' : {'test_op_x' : [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5], 
			'test_op_y' : [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6], 
			'test_op_y_fail' : [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]},
}



# ==============================================================================

pyoperator = {
	'eq' : '==',
	'gt' : '>',
	'ge' : '>=',
	'lt' : '<',
	'le' : '<=',
	'ne' : '!=',
}



def makedata(funcname):
	'''Make the combinations of data options for tests.
	'''
	# Get the data for one specific op.
	op = testdata[funcname]

	# Get how many tests are present. These should all be the same, so
	# we look for the maximum in order to detect errors.
	numtests = max([len(op[x]) for x in op])
	mintests = min([len(op[x]) for x in op])
	if numtests != mintests:
		print('Error! This is a mismatch in the number of data sets for ', funcname)

	count = tuple([('count', x) for x in range(0, numtests)])

	typelabel = (('typecode', 'bytes'), ('typecode', 'bytearray'))
	arrayevenodd = (('arrayevenodd', 'even'), ('arrayevenodd', 'odd'))
	simdpresent = (('simdpresent', 'nosimd'), ('simdpresent', 'withsimd'))

	# This creates all the combinations of test data.
	combos = [dict(x) for x in itertools.product(typelabel, arrayevenodd, simdpresent, count)]

	opdata = {}
	# Cycle through the sets of test data.
	for testnum in range(numtests):
		# Get the data for one set of tests.
		#opdata.append(dict([(x, op[x][testnum]) for x in op]))
		opdata[testnum] = dict([(x, op[x][testnum]) for x in op])

	nosimd = {'nosimd' : {'nosimd' : ', nosimd=True'}, 'withsimd' : {'nosimd' : ''}}

	# Update with the test data. These values don't represent independent combinations,
	# but rather just additional data that goes along with other items already present.
	for x in combos:
		x.update(nosimd[x['simdpresent']])
		x.update(opdata[x['count']])
		x['funcname'] = funcname
		x['pyoperator'] = pyoperator[funcname]
	#
	return combos



# ==============================================================================

# This defines the module name.
modulename = 'bytesfunc'
# We don't import the array module for bytesfunc.
arrayimport = ''

for funcname in pyoperator:

	filenamebase = 'test_' + funcname
	filename = filenamebase + '.py'
	headerdate = codegen_common.FormatHeaderData(filenamebase, '01-Nov-2019', funcname)

	# Add additional header data.
	headerdate['modulename'] = modulename
	headerdate['arrayimport'] = arrayimport

	# One function (one output file). 
	with open(filename, 'w') as f:
		# The copyright header.
		f.write(codegen_common.HeaderTemplate % headerdate)

		#####

		# Test for invalid parameters. One template should work for all 
		# functions of this style.
		for typecode in ('bytes', 'bytearray'):
			funcdata = {'funcname' : funcname,
					'typecode' : typecode,
					'test_op_x' : param_test_data[funcname]['test_op_x'],
					'test_op_y' : param_test_data[funcname]['test_op_y'],
					}

			f.write(param_invalid_template % funcdata)

		#####

		# Test for invalid optional parameters such as errors and maxlen.
		for typecode in ('bytes', 'bytearray'):
			funcdata = {'funcname' : funcname,
					'typecode' : typecode,
					'test_op_x' : param_test_data[funcname]['test_op_x'],
					'test_op_y' : param_test_data[funcname]['test_op_y'],
					}
			f.write(param_invalid_opt_template % funcdata)

		#####

		# Tests for detailed functionality of operations.
		for funcdata in makedata(funcname):
			f.write(test_template_comp % funcdata)

		#####


		# Check each array type.
		# Shift the comparison data through the array to see if the
		# position makes any difference to the failure.
		for typecode in ('bytes', 'bytearray'):
			funcdata = {'funcname' : funcname,
					'typecode' : typecode,
					'pyoperator' : pyoperator[funcname],
					'test_data1' : numposdata1[funcname],
					'test_data1fail' : numposdata1fail[funcname],
					'test_data2' : numposdata2[funcname],
					'test_data2fail' : numposdata2fail[funcname]
					}

			f.write(test_template_numpos % funcdata)

		#####


		f.write(codegen_common.testendtemplate % {'funcname' : funcname, 'modulename' : modulename})

# ==============================================================================

