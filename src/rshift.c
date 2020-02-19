//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   rshift.c
// Purpose:  Calculate the rshift of values in a bytes or bytearray object.
// Language: C
// Date:     22-Jan-2020.
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

#include "bytesparams_two.h"

/*--------------------------------------------------------------------------- */

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
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
void rshift_1(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data1[x] = data1[x] >> param;
	}


}

// param_arr_num_arr
void rshift_2(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data3[x] = data1[x] >> param;
	}

}

// param_num_arr_none
void rshift_3(Py_ssize_t arraylen, unsigned char param, unsigned char *data2) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data2[x] = param >> data2[x];
	}

}

// param_num_arr_arr
void rshift_4(Py_ssize_t arraylen, unsigned char param, unsigned char *data2, unsigned char *data3) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data3[x] = param >> data2[x];
	}

}



// param_arr_arr_none
void rshift_5(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data1[x] = data1[x] >> data2[x];
	}

}

// param_arr_arr_arr
void rshift_6(Py_ssize_t arraylen, unsigned char *data1, unsigned char *data2, unsigned char *data3) {

	// array index counter.
	Py_ssize_t x;

	for (x = 0; x < arraylen; x++) {
		data3[x] = data1[x] >> data2[x];
	}

}

/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   data2 = The second data array.
   data3 = The third data array.
   param = The parameter to be applied to each array element.
*/
// param_arr_num_none
#if defined(AF_HASSIMD_ARM)
void rshift_1_armv7_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft;
	int8x8_t datasliceright;
	signed char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = -(signed char)param;
	}
	datasliceright = vld1_s8(compvals);


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = vld1_u8(&data1[index]);
		// The actual SIMD operation. 
		datasliceleft = vshl_u8(datasliceleft, datasliceright);
		// Store the result.
		vst1_u8(&data1[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data1[index] = data1[index] >> param;
	}

}



// param_arr_num_arr
void rshift_2_armv7_simd(Py_ssize_t arraylen, unsigned char *data1, unsigned char param, unsigned char *data3) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	uint8x8_t datasliceleft;
	int8x8_t datasliceright;
	signed char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = -(signed char)param;
	}
	datasliceright = vld1_s8(compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = vld1_u8(&data1[index]);
		// The actual SIMD operation. 
		datasliceleft = vshl_u8(datasliceleft, datasliceright);
		// Store the result.
		vst1_u8(&data3[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		data3[index] = data1[index] >> param;
	}

}
#endif


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
void rshift_1_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) {

	#if defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		rshift_1_armv7_simd(arraylen, data1, param);
	} else {
	#endif
		rshift_1(arraylen, data1, param);
	#if defined(AF_HASSIMD_ARM)
	}
	#endif

}

// param_arr_num_arr
void rshift_2_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param, unsigned char *data3) {

	#if defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		rshift_2_armv7_simd(arraylen, data1, param, data3);
	} else {
	#endif
		rshift_2(arraylen, data1, param, data3);
	#if defined(AF_HASSIMD_ARM)
	}
	#endif

}


/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_rshift(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_2 bytesdata = ARGSINIT_TWO;


	// -----------------------------------------------------


	// Get the parameters passed from Python. 
	bytesdata = getparams_two(self, args, keywds, "rshift");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.error) {
		return NULL;
	}

	// Call the C function.
	// Select the correct implementation.
	switch (bytesdata.paramcat) {
		case param_arr_num_none : {
			rshift_1_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		case param_arr_num_arr : {
			rshift_2_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param, bytesdata.bytes3.B);
			break;
		}
		case param_num_arr_none : {
			rshift_3(bytesdata.byteslength, bytesdata.param, bytesdata.bytes2.B);
			break;
		}
		case param_num_arr_arr : {
			rshift_4(bytesdata.byteslength, bytesdata.param, bytesdata.bytes2.B, bytesdata.bytes3.B);
			break;
		}
		case param_arr_arr_none : {
			rshift_5(bytesdata.byteslength, bytesdata.bytes1.B, bytesdata.bytes2.B);
			break;
		}
		case param_arr_arr_arr : {
			rshift_6(bytesdata.byteslength, bytesdata.bytes1.B, bytesdata.bytes2.B, bytesdata.bytes3.B);
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
PyDoc_STRVAR(rshift__doc__,
"rshift \n\
_____________________________ \n\
\n\
Calculate rshift over the values in a bytes or bytearray object. \n\
\n\
======================  ============================================== \n\
Equivalent to:          [x >> param for x in sequence1] \n\
or                      [param >> x for x in sequence1] \n\
or                      [x >> y for x,y in zip(sequence1, sequence2)] \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  rshift(sequence1, param) \n\
  rshift(sequence1, param, outpsequence) \n\
  rshift(param, sequence1) \n\
  rshift(param, sequence1, outpsequence) \n\
  rshift(sequence1, sequence2) \n\
  rshift(sequence1, sequence2, outpsequence) \n\
  rshift(sequence1, param, maxlen=y) \n\
  rshift(sequence1, param, nosimd=False) \n\
\n\
* sequence1 - The first input data bytes or bytearray sequence to be \n\
  examined. If no output sequence is provided the results will overwrite \n\
  the input data. \n\
* param - A non-sequence numeric parameter. \n\
* sequence2 - A second input data sequence. Each element in this sequence is \n\
  applied to the corresponding element in the first sequence. \n\
* outpsequence - The output sequence. This parameter is optional. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored. \n\
* nosimd - If True, SIMD acceleration is disabled. This parameter is \n\
  optional. The default is FALSE. \n");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "rshift" is the name seen inside of Python. 
 "py_rshift" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef rshift_methods[] = {
	{"rshift",  (PyCFunction)py_rshift, METH_VARARGS | METH_KEYWORDS, rshift__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef rshiftmodule = {
    PyModuleDef_HEAD_INIT,
    "rshift",
    NULL,
    -1,
    rshift_methods
};

PyMODINIT_FUNC PyInit_rshift(void)
{
    return PyModule_Create(&rshiftmodule);
};

/*--------------------------------------------------------------------------- */

