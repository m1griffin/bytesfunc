//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   findindex.c
// Purpose:  Calculate the findindex of values in a bytes or bytearray object.
// Language: C
// Date:     15-Nov-2017.
//
//------------------------------------------------------------------------------
//
//   Copyright 2014 - 2020    Michael Griffin    <m12.griffin@gmail.com>
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
#ifdef AF_HASSIMD_ARM
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
Py_ssize_t findindex_eq(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] == param1) {
				return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
Py_ssize_t findindex_eq_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

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
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] == param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] == param1) {
			return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM)
Py_ssize_t findindex_eq_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vceq_u8(datasliceleft, datasliceright);
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] == param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] == param1) {
			return index;
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
Py_ssize_t findindex_eq_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_eq_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_eq_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_eq(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
Py_ssize_t findindex_gt(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] > param1) {
				return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
Py_ssize_t findindex_gt_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

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
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] > param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] > param1) {
			return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM)
Py_ssize_t findindex_gt_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcgt_u8(datasliceleft, datasliceright);
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] > param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] > param1) {
			return index;
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
Py_ssize_t findindex_gt_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_gt_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_gt_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_gt(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
Py_ssize_t findindex_ge(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] >= param1) {
				return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
Py_ssize_t findindex_ge_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is greater than or equal to.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] >= param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] >= param1) {
			return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM)
Py_ssize_t findindex_ge_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcge_u8(datasliceleft, datasliceright);
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] >= param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] >= param1) {
			return index;
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
Py_ssize_t findindex_ge_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_ge_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_ge_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_ge(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
Py_ssize_t findindex_lt(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] < param1) {
				return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
Py_ssize_t findindex_lt_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

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
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] < param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] < param1) {
			return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM)
Py_ssize_t findindex_lt_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vclt_u8(datasliceleft, datasliceright);
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] < param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] < param1) {
			return index;
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
Py_ssize_t findindex_lt_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_lt_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_lt_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_lt(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
Py_ssize_t findindex_le(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] <= param1) {
				return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
Py_ssize_t findindex_le_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

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
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] <= param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] <= param1) {
			return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM)
Py_ssize_t findindex_le_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vcle_u8(datasliceleft, datasliceright);
		if (vreinterpret_u64_u8(resultslice) != 0x0000000000000000) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] <= param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] <= param1) {
			return index;
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
Py_ssize_t findindex_le_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_le_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_le_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_le(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
Py_ssize_t findindex_ne(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] != param1) {
				return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_X86)
Py_ssize_t findindex_ne_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

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
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] != param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] != param1) {
			return index;
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
   Returns the array index of the first matching instance, or ARR_ERR_NOTFOUND,
		if it was not found.
*/
#if defined(AF_HASSIMD_ARM)
Py_ssize_t findindex_ne_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

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
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = vceq_u8(datasliceleft, datasliceright);
		if (vreinterpret_u64_u8(resultslice) != 0xffffffffffffffff) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] != param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] != param1) {
			return index;
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
Py_ssize_t findindex_ne_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_ne_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_ne_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_ne(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_findindex(PyObject *self, PyObject *args, PyObject *keywds) {


	// The error code returned by the function.
	Py_ssize_t resultcode = 0;

	// This is used to hold the parsed parameters.
	struct args_params_allany bytesdata = ARGSINIT_ALLANY;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_allany(self, args, keywds, "findindex");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.error) {
		return NULL;
	}


	// The length of the data array.
	if (bytesdata.byteslength < 1) {
		// Release the buffers. 
		releasebuffers_allany(bytesdata);
		ErrMsgArrayLengthErr();
		return NULL;
	}


	/* Call the C function for the requested operation. */
	switch(bytesdata.opcode) {
		// AF_EQ
		case OP_AF_EQ: {
			resultcode = findindex_eq_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_GT
		case OP_AF_GT: {
			resultcode = findindex_gt_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_GE
		case OP_AF_GE: {
			resultcode = findindex_ge_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_LT
		case OP_AF_LT: {
			resultcode = findindex_lt_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_LE
		case OP_AF_LE: {
			resultcode = findindex_le_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_NE
		case OP_AF_NE: {
			resultcode = findindex_ne_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
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



	// Adjust the result code if the data was not found, so that we don't leak
	// internal error codes to user space (and cause problems if they change).
	if (resultcode < 0) {
		resultcode = -1;
	}

	// Return the number of items filtered through.
	return PyLong_FromSsize_t(resultcode);


}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(findindex__doc__,
"findindex \n\
_____________________________ \n\
\n\
Calculate findindex over the values a bytes or bytearray object. \n\
\n\
======================  ============================================== \n\
Equivalent to:          [x for x,y in enumerate(array) if y > param][0] \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  result = findindex(opstr, sequence, param) \n\
  result = findindex(opstr, sequence, param, maxlen=y) \n\
  result = findindex(opstr, sequence, param, nosimd=False) \n\
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
* result - The resulting index. This will be negative if no match was found. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "findindex" is the name seen inside of Python. 
 "py_findindex" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef findindex_methods[] = {
	{"findindex",  (PyCFunction)py_findindex, METH_VARARGS | METH_KEYWORDS, findindex__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef findindexmodule = {
    PyModuleDef_HEAD_INIT,
    "findindex",
    NULL,
    -1,
    findindex_methods
};

PyMODINIT_FUNC PyInit_findindex(void)
{
    return PyModule_Create(&findindexmodule);
};

/*--------------------------------------------------------------------------- */

