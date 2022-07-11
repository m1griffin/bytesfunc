//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bany.c
// Purpose:  Calculate the bany of values in a bytes or bytearray object.
// Language: C
// Date:     15-Nov-2017.
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
#include "arrayops.h"

#include "bytesparams_allany.h"

#include "simddefs.h"
#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
#include "arm_neon.h"
#endif


/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
signed int bany_eq(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] == param1) {
			return 1;
		}
	}
	return ARR_ERR_NOTFOUND;

}


/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
signed int bany_eq_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Compare the slices.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] == param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
signed int bany_eq_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vceq_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] == param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* ARMv8 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
signed int bany_eq_armv8_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x16_t datasliceleft, datasliceright;
	uint8x16_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];
	uint64x2_t veccombine;
	uint64_t highresult, lowresult;

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1q_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1q_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vceqq_u8(datasliceleft, datasliceright);
		// Combine the result to two 64 bit vectors.
		veccombine = vreinterpretq_u64_u8(resultslice);
		// Get the high and low lanes of the combined vector.
		lowresult = vgetq_lane_u64(veccombine, 0);
		highresult = vgetq_lane_u64(veccombine, 1);
		// Compare the results of the SIMD operation.
		if ((lowresult != 0x0000000000000000) || (highresult != 0x0000000000000000)) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] == param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int bany_eq_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			return bany_eq_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return bany_eq_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return bany_eq_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		return bany_eq(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
signed int bany_gt(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] > param1) {
			return 1;
		}
	}
	return ARR_ERR_NOTFOUND;

}


/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
signed int bany_gt_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice, compslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is greater than. 
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] > param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
signed int bany_gt_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcgt_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] > param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* ARMv8 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
signed int bany_gt_armv8_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x16_t datasliceleft, datasliceright;
	uint8x16_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];
	uint64x2_t veccombine;
	uint64_t highresult, lowresult;

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1q_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1q_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcgtq_u8(datasliceleft, datasliceright);
		// Combine the result to two 64 bit vectors.
		veccombine = vreinterpretq_u64_u8(resultslice);
		// Get the high and low lanes of the combined vector.
		lowresult = vgetq_lane_u64(veccombine, 0);
		highresult = vgetq_lane_u64(veccombine, 1);
		// Compare the results of the SIMD operation.
		if ((lowresult != 0x0000000000000000) || (highresult != 0x0000000000000000)) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] > param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int bany_gt_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			return bany_gt_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return bany_gt_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return bany_gt_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		return bany_gt(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
signed int bany_ge(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] >= param1) {
			return 1;
		}
	}
	return ARR_ERR_NOTFOUND;

}


/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
signed int bany_ge_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice, compslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then a least.
		// one value is less than.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] >= param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
signed int bany_ge_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcge_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] >= param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* ARMv8 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
signed int bany_ge_armv8_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x16_t datasliceleft, datasliceright;
	uint8x16_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];
	uint64x2_t veccombine;
	uint64_t highresult, lowresult;

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1q_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1q_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcgeq_u8(datasliceleft, datasliceright);
		// Combine the result to two 64 bit vectors.
		veccombine = vreinterpretq_u64_u8(resultslice);
		// Get the high and low lanes of the combined vector.
		lowresult = vgetq_lane_u64(veccombine, 0);
		highresult = vgetq_lane_u64(veccombine, 1);
		// Compare the results of the SIMD operation.
		if ((lowresult != 0x0000000000000000) || (highresult != 0x0000000000000000)) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] >= param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int bany_ge_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			return bany_ge_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return bany_ge_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return bany_ge_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		return bany_ge(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
signed int bany_lt(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] < param1) {
			return 1;
		}
	}
	return ARR_ERR_NOTFOUND;

}


/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
signed int bany_lt_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice, compslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is less than.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] < param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
signed int bany_lt_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vclt_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] < param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* ARMv8 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
signed int bany_lt_armv8_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x16_t datasliceleft, datasliceright;
	uint8x16_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];
	uint64x2_t veccombine;
	uint64_t highresult, lowresult;

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1q_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1q_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcltq_u8(datasliceleft, datasliceright);
		// Combine the result to two 64 bit vectors.
		veccombine = vreinterpretq_u64_u8(resultslice);
		// Get the high and low lanes of the combined vector.
		lowresult = vgetq_lane_u64(veccombine, 0);
		highresult = vgetq_lane_u64(veccombine, 1);
		// Compare the results of the SIMD operation.
		if ((lowresult != 0x0000000000000000) || (highresult != 0x0000000000000000)) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] < param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int bany_lt_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			return bany_lt_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return bany_lt_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return bany_lt_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		return bany_lt(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
signed int bany_le(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] <= param1) {
			return 1;
		}
	}
	return ARR_ERR_NOTFOUND;

}


/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
signed int bany_le_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice, compslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is less than or equal to.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] <= param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
signed int bany_le_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcle_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] <= param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* ARMv8 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
signed int bany_le_armv8_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x16_t datasliceleft, datasliceright;
	uint8x16_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];
	uint64x2_t veccombine;
	uint64_t highresult, lowresult;

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1q_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1q_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcleq_u8(datasliceleft, datasliceright);
		// Combine the result to two 64 bit vectors.
		veccombine = vreinterpretq_u64_u8(resultslice);
		// Get the high and low lanes of the combined vector.
		lowresult = vgetq_lane_u64(veccombine, 0);
		highresult = vgetq_lane_u64(veccombine, 1);
		// Compare the results of the SIMD operation.
		if ((lowresult != 0x0000000000000000) || (highresult != 0x0000000000000000)) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] <= param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int bany_le_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			return bany_le_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return bany_le_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return bany_le_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		return bany_le(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
signed int bany_ne(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] != param1) {
			return 1;
		}
	}
	return ARR_ERR_NOTFOUND;

}


/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
signed int bany_ne_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Compare for equality.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] != param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
signed int bany_ne_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vceq_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (vreinterpret_u64_u8(resultslice) != 0xffffffffffffffff) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] != param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* ARMv8 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true at least once, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
signed int bany_ne_armv8_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x16_t datasliceleft, datasliceright;
	uint8x16_t resultslice;
	unsigned char compvals[CHARSIMDSIZE];
	uint64x2_t veccombine;
	uint64_t highresult, lowresult;

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = vld1q_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1q_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vceqq_u8(datasliceleft, datasliceright);
		// Combine the result to two 64 bit vectors.
		veccombine = vreinterpretq_u64_u8(resultslice);
		// Get the high and low lanes of the combined vector.
		lowresult = vgetq_lane_u64(veccombine, 0);
		highresult = vgetq_lane_u64(veccombine, 1);
		// Compare the results of the SIMD operation.
		if ((lowresult != 0xffffffffffffffff) || (highresult != 0xffffffffffffffff)) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] != param1) {
			return 1;
		}
	}

	return ARR_ERR_NOTFOUND;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int bany_ne_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		#if defined(AF_HASSIMD_X86)
			return bany_ne_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return bany_ne_armv7_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return bany_ne_armv8_simd(arraylen, data1, param);
		#endif

	} else {
	#endif
		return bany_ne(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_bany(PyObject *self, PyObject *args, PyObject *keywds) {


	// The error code returned by the function.
	signed int resultcode = 0;

	// This is used to hold the parsed parameters.
	struct args_params_allany bytesdata = ARGSINIT_ALLANY;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_allany(self, args, keywds, "bany");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.errorcode) {
		return NULL;
	}


	// The length of the data array.
	if (bytesdata.arraylen < 1) {
		// Release the buffers. 
		releasebuffers_allany(bytesdata);
		ErrMsgArrayLengthErr();
		return NULL;
	}


	/* Call the C function for the requested operation. */
	switch(bytesdata.opcode) {
		// AF_EQ
		case OP_AF_EQ: {
			resultcode = bany_eq_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_GT
		case OP_AF_GT: {
			resultcode = bany_gt_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_GE
		case OP_AF_GE: {
			resultcode = bany_ge_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_LT
		case OP_AF_LT: {
			resultcode = bany_lt_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_LE
		case OP_AF_LE: {
			resultcode = bany_le_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_NE
		case OP_AF_NE: {
			resultcode = bany_ne_select(bytesdata.arraylen, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// The operation code is unknown.
		default: {
			resultcode = ARR_ERR_INVALIDOP;
		}
	}


	// Release the buffers. 
	releasebuffers_allany(bytesdata);


	// Signal the errors.
	if (resultcode == ARR_ERR_INVALIDOP) {
		ErrMsgOperatorNotValidforthisFunction();
		return NULL;
	}



	// Return whether compare was OK.
	if (resultcode == ARR_ERR_NOTFOUND) {
		Py_RETURN_FALSE;
	} else {
		Py_RETURN_TRUE;
	}


}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(bany__doc__,
"bany \n\
_____________________________ \n\
\n\
Calculate bany over the values a bytes or bytearray object. \n\
\n\
======================  ============================================== \n\
Equivalent to:          any([(x > param) for x in array]) \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  result = bany(opstr, sequence, param) \n\
  result = bany(opstr, sequence, param, maxlen=y) \n\
  result = bany(opstr, sequence, param, nosimd=False) \n\
\n\
* opstr - The arithmetic comparison operation as a string. \n\
          These are: '==', '>', '>=', '<', '<=', '!='. \n\
* sequence - An input bytes or bytearray to be examined. \n\
* param - A non-array numeric parameter. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored. \n\
* nosimd - If True, SIMD acceleration is disabled if present. \n\
  The default is False (SIMD acceleration is enabled if present). \n\
* result - A boolean value corresponding to the result of all the \n\
  comparison operations. If all comparison operations result in true, \n\
  the return value will be true. If any of them result in false, the \n\
  return value will be false. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "bany" is the name seen inside of Python. 
 "py_bany" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef bany_methods[] = {
	{"bany",  (PyCFunction)py_bany, METH_VARARGS | METH_KEYWORDS, bany__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef banymodule = {
    PyModuleDef_HEAD_INIT,
    "bany",
    NULL,
    -1,
    bany_methods
};

PyMODINIT_FUNC PyInit_bany(void)
{
    return PyModule_Create(&banymodule);
};

/*--------------------------------------------------------------------------- */

