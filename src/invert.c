//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   invert.c
// Purpose:  Calculate the invert of values in a bytes or bytearray object.
// Language: C
// Date:     19-Jan-2020.
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
#include "bytesparams_invert.h"

#include "simddefs.h"

#ifdef AF_HASSIMD_ARM
#include "arm_neon.h"
#endif

/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* byteslength = The length of the data arrays.
   data = The input data array.
*/
void invert_1(Py_ssize_t byteslength, unsigned char *data) {

	// array index counter.
	Py_ssize_t x;


	for (x = 0; x < byteslength; x++) {
		data[x] = ~data[x];
	}

}

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* byteslength = The length of the data arrays.
   data = The input data array.
   dataout = The output data array.
*/
void invert_2(Py_ssize_t byteslength, unsigned char *data, unsigned char *dataout) {

	// array index counter.
	Py_ssize_t x;


	for (x = 0; x < byteslength; x++) {
		dataout[x] = ~data[x];
	}

}

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   byteslength = The length of the data arrays.
   data = The input data array.
   dataout = The output data array.
*/
// param_arr_none
#if defined(AF_HASSIMD_X86)
void invert_1_x86_simd(Py_ssize_t byteslength, unsigned char *data) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	v2di datasliceleft;
	v2di vopmask = {-1, -1};


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = byteslength - (byteslength % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v2di) __builtin_ia32_lddqu((char *)  &data[index]);
		// The actual SIMD operation. 
		datasliceleft = __builtin_ia32_pxor128(datasliceleft, vopmask);
		// Store the result.
		__builtin_ia32_storedqu((char *) &data[index], (v16qi) datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < byteslength; index++) {
		data[index] = ~data[index];
	}

}


// param_arr_arr
void invert_2_x86_simd(Py_ssize_t byteslength, unsigned char *data, unsigned char *dataout) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	v2di datasliceleft;
	v2di vopmask = {-1, -1};


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = byteslength - (byteslength % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = (v2di) __builtin_ia32_lddqu((char *)  &data[index]);
		// The actual SIMD operation. 
		datasliceleft = __builtin_ia32_pxor128(datasliceleft, vopmask);
		// Store the result.
		__builtin_ia32_storedqu((char *) &dataout[index], (v16qi) datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < byteslength; index++) {
		dataout[index] = ~data[index];
	}

}
#endif

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* The following series of functions reflect the different parameter options possible.
   byteslength = The length of the data arrays.
   data = The input data array.
   dataout = The output data array.
*/
// param_arr_none
#if defined(AF_HASSIMD_ARM)
void invert_1_armv7_simd(Py_ssize_t byteslength, unsigned char *data) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	uint8x8_t datasliceleft;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = byteslength - (byteslength % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = vld1_u8(&data[index]);
		// The actual SIMD operation. 
		datasliceleft = vmvn_u8(datasliceleft);
		// Store the result.
		vst1_u8(&data[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < byteslength; index++) {
		data[index] = ~data[index];
	}

}


// param_arr_arr
void invert_2_armv7_simd(Py_ssize_t byteslength, unsigned char *data, unsigned char *dataout) {

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;

	uint8x8_t datasliceleft;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = byteslength - (byteslength % CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		// Load the data into the vector register.
		datasliceleft = vld1_u8(&data[index]);
		// The actual SIMD operation. 
		datasliceleft = vmvn_u8(datasliceleft);
		// Store the result.
		vst1_u8(&dataout[index], datasliceleft);
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < byteslength; index++) {
		dataout[index] = ~data[index];
	}

}
#endif


/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   byteslength = The length of the data arrays.
   data = The input data array.
   nosimd = If true, disable SIMD acceleration.
*/
void invert_1_select(Py_ssize_t byteslength, int nosimd, unsigned char *data) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (byteslength >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			invert_1_x86_simd(byteslength, data);
		#endif

		#if defined(AF_HASSIMD_ARM)
			invert_1_armv7_simd(byteslength, data);
		#endif
	} else {
	#endif
		invert_1(byteslength, data);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */




/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   byteslength = The length of the data arrays.
   data = The input data array.
   dataout = The output data array.
   nosimd = If true, disable SIMD acceleration.
*/
void invert_2_select(Py_ssize_t byteslength, int nosimd, unsigned char *data, unsigned char *dataout) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (byteslength >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			invert_2_x86_simd(byteslength, data, dataout);
		#endif

		#if defined(AF_HASSIMD_ARM)
			invert_2_armv7_simd(byteslength, data, dataout);
		#endif
	} else {
	#endif
		invert_2(byteslength, data, dataout);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_invert(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_1 bytesdata = ARGSINIT_ONE;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_one(self, args, keywds, "invert");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.error) {
		return NULL;
	}


	// Call the C function.
	if (bytesdata.hasoutputseq) {
		invert_2_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.bytes2.B);
	} else {
		invert_1_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B);
	}



	// Release the buffers. 
	releasebuffers_one(bytesdata);


	// Everything was successful.
	Py_RETURN_NONE;

}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(invert__doc__,
"invert \n\
_____________________________ \n\
\n\
Calculate invert over the values in a bytes or bytearray object.  \n\
\n\
======================  ============================================== \n\
Equivalent to:          [~x for x in sequence1] \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
    invert(sequence1) \n\
    invert(sequence1, outpseq) \n\
    invert(sequence1, maxlen=y) \n\
    invert(sequence1, nosimd=False) \n\
 \n\
* sequence1 - The input bytes or bytearray to be examined. If no output \n\
  bytearray is provided the results will overwrite the input data, in which \n\
  case it must be a bytearray. \n\
* outpseq - The output bytearray. This parameter is optional. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored. \n\
* nosimd - If True, SIMD acceleration is disabled. This parameter is \n\
  optional. The default is FALSE. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "invert" is the name seen inside of Python. 
 "py_invert" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef invert_methods[] = {
	{"invert",  (PyCFunction)py_invert, METH_VARARGS | METH_KEYWORDS, invert__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef invertmodule = {
    PyModuleDef_HEAD_INIT,
    "invert",
    NULL,
    -1,
    invert_methods
};

PyMODINIT_FUNC PyInit_invert(void)
{
    return PyModule_Create(&invertmodule);
};

/*--------------------------------------------------------------------------- */

