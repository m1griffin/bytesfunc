//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   gt.c
// Purpose:  Calculate the gt of values in a bytes or bytearray object.
// Language: C
// Date:     02-Nov-2019.
//
//------------------------------------------------------------------------------
//
//   Copyright 2014 - 2019    Michael Griffin    <m12.griffin@gmail.com>
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
#include "bytesparams_comp.h"

#include "simddefs.h"


#ifdef AF_HASSIMD_ARM
#include "arm_neon.h"
#endif

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num
char gt_1(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter.
	Py_ssize_t x;

	for(x = 0; x < arraylen; x++) {
		if (!(data1[x] > param)) { return 0; }
	}

	return 1;

}


// param_num_arr
char gt_3(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

	// array index counter.
	Py_ssize_t x;

	for(x = 0; x < arraylen; x++) {
		if (!(param > data2[x])) { return 0; }
	}

	return 1;

}


// param_arr_arr
char gt_5(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter.
	Py_ssize_t x;

	for(x = 0; x < arraylen; x++) {
		if (!(data1[x] > data2[x])) { return 0; }
	}

	return 1;

}


/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num
#if defined(AF_HASSIMD_X86)
char gt_1_x86_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) { 

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
		compvals[y] = param;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *)  compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for(index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *)  &data1[index]);
		// Make sure they're not equal.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		if (!(__builtin_ia32_pmovmskb128((v16qi) resultslice) == 0x0000)) {
			return 0;
		}
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if ((__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff)) {
			return 0;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(index = alignedlength; index < arraylen; index++) {
		if (!(data1[index] > param)) {
			return 0;
		}
	}

	return 1;

}


// param_num_arr
char gt_3_x86_simd(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

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
		compvals[y] = param;
	}
	datasliceleft = (v16qi) __builtin_ia32_lddqu((char *)  compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for(index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceright = (v16qi) __builtin_ia32_lddqu((char *)  &data2[index]);
		// Make sure they're not equal.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		if (!(__builtin_ia32_pmovmskb128((v16qi) resultslice) == 0x0000)) {
			return 0;
		}
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (!(__builtin_ia32_pmovmskb128((v16qi) resultslice) == 0xffff)) {
			return 0;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(index = alignedlength; index < arraylen; index++) {
		if (!(param > data2[index])) {
			return 0;
		}
	}

	return 1;

}


// param_arr_arr
char gt_5_x86_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice, compslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for(index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *)  &data1[index]);
		datasliceright = (v16qi) __builtin_ia32_lddqu((char *)  &data2[index]);
		// Make sure they're not equal.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		if (!(__builtin_ia32_pmovmskb128((v16qi) resultslice) == 0x0000)) {
			return 0;
		}
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (!(__builtin_ia32_pmovmskb128((v16qi) resultslice) == 0xffff)) {
			return 0;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(index = alignedlength; index < arraylen; index++) {
		if (!(data1[index] > data2[index])) {
			return 0;
		}
	}

	return 1;

}

#endif


/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num
#if defined(AF_HASSIMD_ARM)
char gt_1_armv7_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) { 

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
		compvals[y] = param;
	}
	datasliceright = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for(index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data1[index]);
		// The actual SIMD operation. 
		resultslice = vcgt_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (!(vreinterpret_u64_u8(resultslice) == 0xffffffffffffffff)) {
			return 0;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(index = alignedlength; index < arraylen; index++) {
		if (!(data1[index] > param)) {
			return 0;
		}
	}

	return 1;

}


// param_num_arr
char gt_3_armv7_simd(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

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
		compvals[y] = param;
	}
	datasliceleft = vld1_u8( compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for(index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceright = vld1_u8( &data2[index]);
		// The actual SIMD operation. 
		resultslice = vcgt_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (!(vreinterpret_u64_u8(resultslice) == 0xffffffffffffffff)) {
			return 0;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(index = alignedlength; index < arraylen; index++) {
		if (!(param > data2[index])) {
			return 0;
		}
	}

	return 1;

}


// param_arr_arr
char gt_5_armv7_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	uint8x8_t datasliceleft, datasliceright;
	uint8x8_t resultslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for(index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data1[index]);
		datasliceright = vld1_u8( &data2[index]);
		// The actual SIMD operation. 
		resultslice = vcgt_u8(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (!(vreinterpret_u64_u8(resultslice) == 0xffffffffffffffff)) {
			return 0;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(index = alignedlength; index < arraylen; index++) {
		if (!(data1[index] > data2[index])) {
			return 0;
		}
	}

	return 1;

}

#endif


/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   param = The parameter to be applied to each array element.
*/
char gt_1_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return gt_1_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return gt_1_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return gt_1(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   param = The parameter to be applied to each array element.
*/
char gt_3_select(Py_ssize_t arraylen, int nosimd, unsigned char param, unsigned char *data2) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return gt_3_x86_simd(arraylen, param, data2);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return gt_3_armv7_simd(arraylen, param, data2);
		#endif
	} else {
	#endif
		return gt_3(arraylen, param, data2);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   param = The parameter to be applied to each array element.
*/
char gt_5_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char *data2) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return gt_5_x86_simd(arraylen, data1, data2);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return gt_5_armv7_simd(arraylen, data1, data2);
		#endif
	} else {
	#endif
		return gt_5(arraylen, data1, data2);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_gt(PyObject *self, PyObject *args, PyObject *keywds) {


	// The error code returned by the function.
	char resultcode = 0;

	// This is used to hold the parsed parameters.
	struct args_params_comp bytesdata = ARGSINIT_COMP;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_comp(self, args, keywds, "gt");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.error) {
		return NULL;
	}


	switch (bytesdata.paramcat) {
		case param_arr_num : {
			resultcode = gt_1_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		case param_num_arr : {
			resultcode = gt_3_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.param, bytesdata.bytes2.B);
			break;
		}
		case param_arr_arr : {
			resultcode = gt_5_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.bytes2.B);
			break;
		}
	}


	// Release the buffers. 
	releasebuffers_comp(bytesdata);


	// Return whether compare was OK.
	if (resultcode) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}

}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(gt__doc__,
"gt \n\
_____________________________ \n\
\n\
Calculate gt over the values in a bytes or bytearray object.  \n\
\n\
======================  ============================================== \n\
Equivalent to:          all([x > param for x in sequence]) \n\
or                      all([param > x for x in sequence]) \n\
or                      all([x > y for x,y in zip(sequence1, sequence2)]) \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  result = gt(sequence1, param) \n\
  result = gt(param, sequence1) \n\
  result = gt(sequence1, sequence2) \n\
  result = gt(sequence1, param, maxlen=y) \n\
  result = gt(sequence1, param, nosimd=False) \n\
\n\
* sequence1 - An input bytes or bytearray to be examined. \n\
* sequence2 - An input bytes or bytearray to be examined. \n\
* param - A integer numeric input parameter in the range 0 - 255.  \n\
* The first and second parameters are compared to each other. If one \n\
  parameter is a sequence and the other is an integer, the integer \n\
  is compared to each element in the sequence. If both parameters are \n\
  sequences, each element of one sequence is compared to the \n\
  corresponding element of the other sequence. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored.  \n\
* nosimd - If True, SIMD acceleration is disabled if present.  \n\
  The default is False (SIMD acceleration is enabled if present). \n\
* result - A boolean value corresponding to the result of all the \n\
  comparison operations. If all comparison operations result in true, \n\
  the return value will be true. If any of them result in false, the \n\
  return value will be false. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "gt" is the name seen inside of Python. 
 "py_gt" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef gt_methods[] = {
	{"gt",  (PyCFunction)py_gt, METH_VARARGS | METH_KEYWORDS, gt__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef gtmodule = {
    PyModuleDef_HEAD_INIT,
    "gt",
    NULL,
    -1,
    gt_methods
};

PyMODINIT_FUNC PyInit_gt(void)
{
    return PyModule_Create(&gtmodule);
};

/*--------------------------------------------------------------------------- */

