#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the C code for math operations. 
# Language: Python 3.5
# Date:     22-Jan-2020
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

mathops_head = """//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   %(funclabel)s.c
// Purpose:  Calculate the %(funclabel)s of values in a bytes or bytearray object.
// Language: C
// Date:     22-Jan-2020.
//
//------------------------------------------------------------------------------
//
//   Copyright 2014 - 2022    Michael Griffin    <m12.griffin@gmail.com>
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.
//
//------------------------------------------------------------------------------

/*--------------------------------------------------------------------------- */
// This must be defined before "Python.h" in order for the pointers in the
// argument parsing functions to work properly. 
#define PY_SSIZE_T_CLEAN

#include "Python.h"

#include <limits.h>
#include <math.h>

#include "byteserrs.h"

#include "bytesparams_base.h"

#include "bytesparams_two.h"

/*--------------------------------------------------------------------------- */

#include "simddefs.h"

#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
#include "arm_neon.h"
#endif

/*--------------------------------------------------------------------------- */

"""

# ==============================================================================

# For all binary operators with two arguments.
ops_binop = """
/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
void %(funclabel)s_1(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data1[x] = data1[x] %(copname)s param;
	}


}

// param_arr_num_arr
void %(funclabel)s_2(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data3[x] = data1[x] %(copname)s param;
	}

}

// param_num_arr_none
void %(funclabel)s_3(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data2[x] = param %(copname)s data2[x];
	}

}

// param_num_arr_arr
void %(funclabel)s_4(Py_ssize_t arraylen, unsigned char param, unsigned char *data2, unsigned char *data3) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data3[x] = param %(copname)s data2[x];
	}

}



// param_arr_arr_none
void %(funclabel)s_5(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data1[x] = data1[x] %(copname)s data2[x];
	}

}

// param_arr_arr_arr
void %(funclabel)s_6(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2, unsigned char *data3) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data3[x] = data1[x] %(copname)s data2[x];
	}

}
"""


# ==============================================================================


# ==============================================================================



# The actual compare operations using SIMD operations.
ops_simdsupport_x86 = """
/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
#if defined(AF_HASSIMD_X86)
void %(funclabel)s_1_x86_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data1[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s( (v2di) datasliceleft,  (v2di) datasliceright);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data1[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] %(copname)s param;
	}

}



// param_arr_num_arr
void %(funclabel)s_2_x86_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data1[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s( (v2di) datasliceleft,  (v2di) datasliceright);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data3[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] %(copname)s param;
	}

}



// param_num_arr_none
void %(funclabel)s_3_x86_simd(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceright = (v16qi) __builtin_ia32_lddqu((char *) &data2[index]);
		// The actual SIMD operation. 
		datasliceright = %(vopinstr)s( (v2di) datasliceleft,  (v2di) datasliceright);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data2[index], datasliceright);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data2[index] = param %(copname)s data2[index];
	}

}



// param_num_arr_arr
void %(funclabel)s_4_x86_simd(Py_ssize_t arraylen, unsigned char param, unsigned char *data2, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceright = (v16qi) __builtin_ia32_lddqu((char *) &data2[index]);
		// The actual SIMD operation. 
		datasliceright = %(vopinstr)s( (v2di) datasliceleft,  (v2di) datasliceright);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data3[index], datasliceright);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = param %(copname)s data2[index];
	}

}



// param_arr_arr_none
void %(funclabel)s_5_x86_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	v16qi datasliceleft, datasliceright;

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data1[index]);
		datasliceright = (v16qi) __builtin_ia32_lddqu((char *) &data2[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s( (v2di) datasliceleft,  (v2di) datasliceright);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data1[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] %(copname)s data2[index];
	}

}



// param_arr_arr_arr
void %(funclabel)s_6_x86_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	v16qi datasliceleft, datasliceright;

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data1[index]);
		datasliceright = (v16qi) __builtin_ia32_lddqu((char *) &data2[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s( (v2di) datasliceleft,  (v2di) datasliceright);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data3[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] %(copname)s data2[index];
	}

}
#endif

"""
# ==============================================================================


# The actual shift operations using SIMD operations.
# This is a special version for x86-64 lshift and rshift only. This 
# implements array shifted by a constant only, as shift by a vector
# (array shifted by elements in another array) do not appear to work
# when handled by GCC built-in functions. 
# x86 does not have SIMD operations for all data types. This version implements
# it for small data sizes by using shift from a larger size together with
# a mask to mask off bits which should fall off the end. The shift operation
# therefore should be the one for array type "I". 
ops_simdsupport_shift_mask_x86 = """
/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
#if defined(AF_HASSIMD_X86)
void %(funclabel)s_1_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	// The mask and shift operations are done using a different data
	// type than the parameters passed to the function. We always use
	// the largest x86 shift operation available, which is unsigned int
	v4si datasliceleft, vmaskslice;

	// This mask gets rid of the bits which would otherwise get shifted
	// into the adjoining vector element.
	unsigned int maskvals[] = {%(vmaskvalues)s};
	unsigned int compvals[INTSIMDSIZE];
	unsigned int selectedmask;
	unsigned int y;

	// Select the mask value based on how many positions we are required
	// to shift. This is limited to the number of masks defined.
	if ((param > 7) || (param < 0)) {
		selectedmask = 0;
	} else {
		selectedmask = maskvals[param];
	}
	
	// Initialise the mask values.
	for (y = 0; y < INTSIMDSIZE; y++) {
		compvals[y] = selectedmask;
	}
	vmaskslice = (v4si) __builtin_ia32_lddqu((char *) compvals);


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v4si) __builtin_ia32_lddqu((char *) &data1[index]);

		// Mask off the bits that would otherwise overflow into the adjacent byte.
		datasliceleft = (v4si) __builtin_ia32_pand128( (v2di) datasliceleft,  (v2di) vmaskslice);

		// The actual SIMD operation. This should always be the lshift or rshift
		// operation for unsigned integer.
		datasliceleft = %(vopinstr)s(datasliceleft, (int) param);

		// Store the result.
		__builtin_ia32_storedqu((char *) &data1[index], (v16qi) datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] %(copname)s param;
	}

}



// param_arr_num_arr
void %(funclabel)s_2_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	// The mask and shift operations are done using a different data
	// type than the parameters passed to the function. We always use
	// the largest x86 shift operation available, which is unsigned int
	v4si datasliceleft, vmaskslice;

	// This mask gets rid of the bits which would otherwise get shifted
	// into the adjoining vector element.
	unsigned int maskvals[] = {%(vmaskvalues)s};
	unsigned int compvals[INTSIMDSIZE];
	unsigned int selectedmask, y;

	// Select the mask value based on how many positions we are required
	// to shift. This is limited to the number of masks defined.
	if ((param > 7) || (param < 0)) {
		selectedmask = 0;
	} else {
		selectedmask = maskvals[param];
	}
	
	// Initialise the mask values.
	for (y = 0; y < INTSIMDSIZE; y++) {
		compvals[y] = selectedmask;
	}
	vmaskslice = (v4si) __builtin_ia32_lddqu((char *) compvals);


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v4si) __builtin_ia32_lddqu((char *) &data1[index]);

		// Mask off the bits that would otherwise overflow into the adjacent byte.
		datasliceleft = (v4si) __builtin_ia32_pand128( (v2di) datasliceleft,  (v2di) vmaskslice);

		// The actual SIMD operation. This should always be the lshift or rshift
		// operation for unsigned integer.
		datasliceleft = %(vopinstr)s(datasliceleft, (int) param);

		// Store the result.
		__builtin_ia32_storedqu((char *) &data3[index], (v16qi) datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] %(copname)s param;
	}

}
#endif


"""


# ==============================================================================



# ==============================================================================

# The actual compare operations using SIMD operations.
ops_simdsupport_arm = """
/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
#if defined(%(SIMD_platform)s)
void %(funclabel)s_1_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	%(vsimdattr)s datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceright = %(vloadop)s(compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = %(vloadop)s(&data1[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data1[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] %(copname)s param;
	}

}



// param_arr_num_arr
void %(funclabel)s_2_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	%(vsimdattr)s datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceright = %(vloadop)s(compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = %(vloadop)s(&data1[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data3[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] %(copname)s param;
	}

}



// param_num_arr_none
void %(funclabel)s_3_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	%(vsimdattr)s datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceleft = %(vloadop)s(compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceright = %(vloadop)s(&data2[index]);
		// The actual SIMD operation. The compiler generates the correct instruction.
		datasliceright = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data2[index], datasliceright);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data2[index] = param %(copname)s data2[index];
	}

}



// param_num_arr_arr
void %(funclabel)s_4_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char param, unsigned char *data2, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	%(vsimdattr)s datasliceleft, datasliceright;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param;
	}
	datasliceleft = %(vloadop)s(compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceright = %(vloadop)s(&data2[index]);
		// The actual SIMD operation. The compiler generates the correct instruction.
		datasliceright = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data3[index], datasliceright);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = param %(copname)s data2[index];
	}

}



// param_arr_arr_none
void %(funclabel)s_5_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	%(vsimdattr)s datasliceleft, datasliceright;

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = %(vloadop)s(&data1[index]);
		datasliceright = %(vloadop)s(&data2[index]);
		// The actual SIMD operation. The compiler generates the correct instruction.
		datasliceleft = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data1[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] %(copname)s data2[index];
	}

}



// param_arr_arr_arr
void %(funclabel)s_6_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	%(vsimdattr)s datasliceleft, datasliceright;

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = %(vloadop)s(&data1[index]);
		datasliceright = %(vloadop)s(&data2[index]);
		// The actual SIMD operation. The compiler generates the correct instruction.
		datasliceleft = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data3[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] %(copname)s data2[index];
	}

}
#endif

"""

# ==============================================================================

# The actual compare operations using SIMD operations. Shift operations have
# more limited support in terms of the forms of the equations.
ops_simdsupport_shift_arm = """
/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
#if defined(%(SIMD_platform)s)
void %(funclabel)s_1_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	%(vsimdattr)s datasliceleft;
	%(vsimdattr2)s datasliceright;
	signed char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = %(vshift_sign)s(signed char)param;
	}
	datasliceright = %(vloadop2)s(compvals);


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = %(vloadop)s(&data1[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data1[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] %(copname)s param;
	}

}



// param_arr_num_arr
void %(funclabel)s_2_%(funcplat)s_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	%(vsimdattr)s datasliceleft;
	%(vsimdattr2)s datasliceright;
	signed char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = %(vshift_sign)s(signed char)param;
	}
	datasliceright = %(vloadop2)s(compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = %(vloadop)s(&data1[index]);
		// The actual SIMD operation. 
		datasliceleft = %(vopinstr)s(datasliceleft, datasliceright);
		// Store the result.
		%(vstoreop)s(&data3[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] %(copname)s param;
	}

}
#endif

"""

# ==============================================================================

# ==============================================================================

# Functions to select the SIMD or non-SIMD version of the function.
binops_select = """
/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD acceleration.
*/
// param_arr_num_none
void %(funclabel)s_1_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_1_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_1_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_1_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		%(funclabel)s_1(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}

// param_arr_num_arr
void %(funclabel)s_2_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param, unsigned char *data3) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_2_x86_simd(arraylen, data1, param, data3);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_2_armv7_simd(arraylen, data1, param, data3);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_2_armv8_simd(arraylen, data1, param, data3);
		#endif

	} else {
	#endif
		%(funclabel)s_2(arraylen, data1, param, data3);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}

// param_num_arr_none
void %(funclabel)s_3_select(Py_ssize_t arraylen, int nosimd, unsigned char param, unsigned char *data2) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_3_x86_simd(arraylen, param, data2);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_3_armv7_simd(arraylen, param, data2);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_3_armv8_simd(arraylen, param, data2);
		#endif

	} else {
	#endif
		%(funclabel)s_3(arraylen, param, data2);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}

// param_num_arr_arr
void %(funclabel)s_4_select(Py_ssize_t arraylen, int nosimd, unsigned char param, unsigned char *data2, unsigned char *data3) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_4_x86_simd(arraylen, param, data2, data3);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_4_armv7_simd(arraylen, param, data2, data3);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_4_armv8_simd(arraylen, param, data2, data3);
		#endif

	} else {
	#endif
		%(funclabel)s_4(arraylen, param, data2, data3);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}

// param_arr_arr_none
void %(funclabel)s_5_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char *data2) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_5_x86_simd(arraylen, data1, data2);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_5_armv7_simd(arraylen, data1, data2);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_5_armv8_simd(arraylen, data1, data2);
		#endif

	} else {
	#endif
		%(funclabel)s_5(arraylen, data1, data2);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}

// param_arr_arr_arr
void %(funclabel)s_6_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char *data2, unsigned char *data3) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_6_x86_simd(arraylen, data1, data2, data3);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_6_armv7_simd(arraylen, data1, data2, data3);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_6_armv8_simd(arraylen, data1, data2, data3);
		#endif

	} else {
	#endif
		%(funclabel)s_6(arraylen, data1, data2, data3);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}


/*--------------------------------------------------------------------------- */

"""

# ==============================================================================

# Functions to select the SIMD or non-SIMD version of the function.
# This is for lshift and rshift only, as these only implement SIMD for some
# parameter forms.
binops_select_shift = """
/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD acceleration.
*/
// param_arr_num_none
void %(funclabel)s_1_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {

		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_1_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_1_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_1_armv8_simd(arraylen, data1, param);
		#endif
		
	} else {
	#endif
		%(funclabel)s_1(arraylen, data1, param);
	#if  defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}

// param_arr_num_arr
void %(funclabel)s_2_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param, unsigned char *data3) {

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {

		#if defined(AF_HASSIMD_X86)
			%(funclabel)s_2_x86_simd(arraylen, data1, param, data3);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			%(funclabel)s_2_armv7_simd(arraylen, data1, param, data3);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			%(funclabel)s_2_armv8_simd(arraylen, data1, param, data3);
		#endif

	} else {
	#endif
		%(funclabel)s_2(arraylen, data1, param, data3);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}


/*--------------------------------------------------------------------------- */

"""


# ==============================================================================


# ==============================================================================

binops_params = """
/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_%(funclabel)s(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_2 bytesdata = ARGSINIT_TWO;


	// -----------------------------------------------------


	// Get the parameters passed from Python. 
	bytesdata = getparams_two(self, args, keywds, "%(funclabel)s");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.errorcode) {
		return NULL;
	}

	// Call the C function.
	// Select the correct implementation.
	switch (bytesdata.paramcat) {
		case param_arr_num_none : {
			%(funclabel)s_1_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		case param_arr_num_arr : {
			%(funclabel)s_2_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param, bytesdata.bytes3.B);
			break;
		}
		case param_num_arr_none : {
			%(funclabel)s_3%(paramselect)s(bytesdata.arraylen,%(paramnosimd)s bytesdata.param, bytesdata.bytes2.B);
			break;
		}
		case param_num_arr_arr : {
			%(funclabel)s_4%(paramselect)s(bytesdata.arraylen,%(paramnosimd)s bytesdata.param, bytesdata.bytes2.B, bytesdata.bytes3.B);
			break;
		}
		case param_arr_arr_none : {
			%(funclabel)s_5%(paramselect)s(bytesdata.arraylen,%(paramnosimd)s bytesdata.bytes1.B, bytesdata.bytes2.B);
			break;
		}
		case param_arr_arr_arr : {
			%(funclabel)s_6%(paramselect)s(bytesdata.arraylen,%(paramnosimd)s bytesdata.bytes1.B, bytesdata.bytes2.B, bytesdata.bytes3.B);
			break;
		}
	}

	// Release the buffers. 
	releasebuffers_two(bytesdata);


	// Everything was successful.
	Py_RETURN_NONE;

}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(%(funclabel)s__doc__,
"%(funclabel)s \\n\\
_____________________________ \\n\\
\\n\\
Calculate %(funclabel)s over the values in a bytes or bytearray object. \\n\\
\\n\\
======================  ============================================== \\n\\
Equivalent to:          [x %(opcodedocs)s param for x in sequence1] \\n\\
or                      [param %(opcodedocs)s x for x in sequence1] \\n\\
or                      [x %(opcodedocs)s y for x,y in zip(sequence1, sequence2)] \\n\\
======================  ============================================== \\n\\
\\n\\
Call formats: \\n\\
\\n\\
  %(funclabel)s(sequence1, param) \\n\\
  %(funclabel)s(sequence1, param, outpsequence) \\n\\
  %(funclabel)s(param, sequence1) \\n\\
  %(funclabel)s(param, sequence1, outpsequence) \\n\\
  %(funclabel)s(sequence1, sequence2) \\n\\
  %(funclabel)s(sequence1, sequence2, outpsequence) \\n\\
  %(funclabel)s(sequence1, param, maxlen=y) \\n\\
  %(funclabel)s(sequence1, param, nosimd=False) \\n\\
\\n\\
* sequence1 - The first input data bytes or bytearray sequence to be \\n\\
  examined. If no output sequence is provided the results will overwrite \\n\\
  the input data. \\n\\
* param - A non-sequence numeric parameter. \\n\\
* sequence2 - A second input data sequence. Each element in this sequence is \\n\\
  applied to the corresponding element in the first sequence. \\n\\
* outpsequence - The output sequence. This parameter is optional. \\n\\
* maxlen - Limit the length of the sequence used. This must be a valid \\n\\
  positive integer. If a zero or negative length, or a value which is \\n\\
  greater than the actual length of the sequence is specified, this \\n\\
  parameter is ignored. \\n\\
* nosimd - If True, SIMD acceleration is disabled. This parameter is \\n\\
  optional. The default is FALSE. \\n\\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "%(funclabel)s" is the name seen inside of Python. 
 "py_%(funclabel)s" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef %(funclabel)s_methods[] = {
	{"%(funclabel)s",  (PyCFunction)py_%(funclabel)s, METH_VARARGS | METH_KEYWORDS, %(funclabel)s__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef %(funclabel)smodule = {
    PyModuleDef_HEAD_INIT,
    "%(funclabel)s",
    NULL,
    -1,
    %(funclabel)s_methods
};

PyMODINIT_FUNC PyInit_%(funclabel)s(void)
{
    return PyModule_Create(&%(funclabel)smodule);
};

/*--------------------------------------------------------------------------- */

"""


# ==============================================================================



# ==============================================================================

# x86 SIMD instructions.
simdop_x86 = {
	'lshift' : '__builtin_ia32_pslldi128',
	'rshift' : '__builtin_ia32_psrldi128',
	'and_' : '(v16qi) __builtin_ia32_pand128', 
	'or_' : '(v16qi) __builtin_ia32_por128', 
	'xor' : '(v16qi) __builtin_ia32_pxor128',
}

# Used for lshift and rshift operations where a larger SIMD size is used 
# combined with a shift. X86 does not directly support SIMD shift operations
# on all relevant data types.
lshiftmaskbasic = ['ff', '7f', '3f', '1f', '0f', '07', '03', '01']
vmaskvalues_lshift = ', '.join(['0x%s' % (x * 4) for x in lshiftmaskbasic])

rshiftmaskbasic = ['ff', 'fe', 'fc', 'f8', 'f0', 'e0', 'c0', '80']
vmaskvalues_rshift = ', '.join(['0x%s' % (x * 4) for x in rshiftmaskbasic])


# Masks for x86 SIMD shift instructions.
simdop_x86_mask = {
	'lshift' : vmaskvalues_lshift,
	'rshift' : vmaskvalues_rshift,
	'and_' : '', 
	'or_' : '', 
	'xor' : '',
}
# ==============================================================================

# For ARMv7 NEON 32 bit.

# Left and right shift use the same instruction, with the sign of the
# second parameter controlling the shift direction.
vopinstr_armv7 = {
	'lshift' : 'vshl_u8', 
	'rshift' : 'vshl_u8',
	'and_' : 'vand_u8', 
	'or_' : 'vorr_u8', 
	'xor' : 'veor_u8',
}

# For ARMv8 NEON 64 bit.
vopinstr_armv8 = {
	'lshift' : 'vshlq_u8', 
	'rshift' : 'vshlq_u8',
	'and_' : 'vandq_u8', 
	'or_' : 'vorrq_u8', 
	'xor' : 'veorq_u8',
}



vshift_sign_arm = {
	'lshift' : '',
	'rshift' : '-',
	'and_' : '',
	'or_' : '',
	'xor' : '',
}


# ==============================================================================


# ==============================================================================


# The function operations implemented, and their C equivalent operators.
copname = {
	'lshift' : '<<', 
	'rshift' : '>>',
	'and_' : '&', 
	'or_' : '|', 
	'xor' : '^',
}


# The functions which are implemented by this program.
completefuncnames = copname.keys()

# Documentation.
opcodedocs = {
	'lshift' : '<<', 
	'rshift' : '>>',
	'and_' : '&', 
	'or_' : '|', 
	'xor' : '^',
}



# ==============================================================================

for funcname in completefuncnames:


	# Create the source code based on templates.
	filename = funcname + '.c'
	with open(filename, 'w') as f:

		f.write(mathops_head % {'funclabel' : funcname})

		f.write(ops_binop % {'funclabel' : funcname,
						'copname' : copname[funcname]
						})


		# A different template is required for lshift, rshift than for
		# the other operations.
		if funcname in ('lshift', 'rshift'):
			simdsupport_arm_tmpl = ops_simdsupport_shift_arm
			simdsupport_x86_tmpl = ops_simdsupport_shift_mask_x86
		else:
			simdsupport_arm_tmpl = ops_simdsupport_arm
			simdsupport_x86_tmpl = ops_simdsupport_x86


		# x86-64 SIMD operations.
		f.write(simdsupport_x86_tmpl % {
						'funclabel' : funcname,
						'funcplat' : 'x86',
						'copname' : copname[funcname],
						'vopinstr' : simdop_x86[funcname],
						'vmaskvalues' : simdop_x86_mask[funcname],
						})


		# ARMv7 SIMD operations.
		f.write(simdsupport_arm_tmpl % {'SIMD_platform' : 'AF_HASSIMD_ARMv7_32BIT',
						'funclabel' : funcname,
						'funcplat' : 'armv7',
						'copname' : copname[funcname],
						'vopinstr' : vopinstr_armv7[funcname],
						'vshift_sign' : vshift_sign_arm[funcname],
						'vsimdattr' : 'uint8x8_t',
						'vsimdattr2' : 'int8x8_t',
						'vloadop' : 'vld1_u8',
						'vloadop2' : 'vld1_s8',
						'vstoreop' : 'vst1_u8',
						})

		# ARMv8 SIMD operations.
		f.write(simdsupport_arm_tmpl % {'SIMD_platform' : 'AF_HASSIMD_ARM_AARCH64',
						'funclabel' : funcname,
						'funcplat' : 'armv8',
						'copname' : copname[funcname],
						'vopinstr' : vopinstr_armv8[funcname],
						'vshift_sign' : vshift_sign_arm[funcname],
						'vsimdattr' : 'uint8x16_t',
						'vsimdattr2' : 'int8x16_t',
						'vloadop' : 'vld1q_u8',
						'vloadop2' : 'vld1q_s8',
						'vstoreop' : 'vst1q_u8',
						})


		# Functions to select SIMD or non-SIMD code.
		# lshift and rshift require a different template as they do
		# not implement x86 SIMD for all parameter forms.
		if funcname in ('lshift', 'rshift'):
			f.write(binops_select_shift % {'funclabel' : funcname})
			paramselect = ''
			paramnosimd = ''
		else:
			f.write(binops_select % {'funclabel' : funcname})
			paramselect = '_select'
			paramnosimd = ' bytesdata.nosimd,'


		# Construct the case structure to select the correct parameter form.
		f.write(binops_params % {'funclabel' : funcname,
								'paramselect' : paramselect,
								'paramnosimd' : paramnosimd,
								'opcodedocs' : opcodedocs[funcname], 
								})




# ==============================================================================

