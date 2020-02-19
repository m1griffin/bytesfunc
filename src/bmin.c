//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bmin.c
// Purpose:  Calculate the bmin of values in a bytes or bytearray object.
// Language: C
// Date:     30-Oct-2019.
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

#include "simddefs.h"
#ifdef AF_HASSIMD_ARM
#include "arm_neon.h"
#endif

#include "bytesparams_base.h"
#include "bytesparams_valoutsimd.h"


/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */
/* arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The minimum value found.
*/
unsigned char bmin(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x; 
	unsigned char minfound;

	minfound = data[0];
	for(x = 0; x < arraylen; x++) {
		if (data[x] < minfound) {
			minfound = data[x];
		}
	}

	return minfound;
}
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For x86-64 SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The minimum value found.
*/
#if defined(AF_HASSIMD_X86)
unsigned char bmin_x86_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char minfound;

	unsigned char minvals[CHARSIMDSIZE];
	v16qi minslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Initialise the comparison values.
	minslice = (v16qi) __builtin_ia32_lddqu((char *) &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = (v16qi) __builtin_ia32_lddqu((char *) &data[x]);
		minslice = __builtin_ia32_pminub128 (minslice, dataslice);
	}

	// Find the min within the slice.
	__builtin_ia32_storedqu((char *) minvals,   minslice);
	minfound = minvals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (minvals[y] < minfound) {
			minfound = minvals[y];
		}
	}

	// Get the min value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] < minfound) {
			minfound = data[x];
		}
	}

	return minfound;
}
#endif
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For ARMv7 NEON SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The minimum value found.
*/
#if defined(AF_HASSIMD_ARM)
unsigned char bmin_armv7_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char minfound;

	unsigned char minvals[CHARSIMDSIZE];
	uint8x8_t minslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Initialise the comparison values.
	minslice = vld1_u8( &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = vld1_u8( &data[x]);
		minslice = vmin_u8 (minslice, dataslice);
	}

	// Find the min within the slice.
	vst1_u8( minvals,   minslice);
	minfound = minvals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (minvals[y] < minfound) {
			minfound = minvals[y];
		}
	}

	// Get the min value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] < minfound) {
			minfound = data[x];
		}
	}

	return minfound;
}
#endif
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The minimum value found.
*/
unsigned char bmin_select(Py_ssize_t arraylen, int nosimd, unsigned char *data) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return bmin_x86_simd(arraylen, data);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return bmin_armv7_simd(arraylen, data);
		#endif
	} else {
	#endif
		return bmin(arraylen, data);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_bmin(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_valoutsimd bytesdata = ARGSINIT_VALOUTSIMD;


	// The output will be an integer.
	unsigned char result;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_valoutsimd(self, args, keywds, "bmin");


	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.error) {
		return NULL;
	}


	// The length of the bytes or bytearray.
	if (bytesdata.byteslength < 1) {
		// Release the buffers. 
		releasebuffers_valoutsimd(bytesdata);
		ErrMsgArrayLengthErr();
		return NULL;
	}

	// Call the calculation function.
	result = bmin_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B);

	// Release the buffers. 
	releasebuffers_valoutsimd(bytesdata);

	return PyLong_FromUnsignedLong( (unsigned long) result);


}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(bmin__doc__,
"bmin \n\
_____________________________ \n\
\n\
Calculate bmin over the values in an array.  \n\
\n\
======================  ============================================== \n\
Equivalent to:          min(sequence) \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  result = bmin(sequence) \n\
  result = bmin(sequence, maxlen=y) \n\
  result = bmin(sequence, nosimd=False) \n\
\n\
* sequence - The input bytes or bytearray to be examined. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored. \n\
* nosimd - If True, SIMD acceleration is disabled if present. \n\
  The default is False (SIMD acceleration is enabled if present). \n\
* result = The minimum of all the values in the sequence. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "bmin" is the name seen inside of Python. 
 "py_bmin" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef bmin_methods[] = {
	{"bmin",  (PyCFunction)py_bmin, METH_VARARGS | METH_KEYWORDS, bmin__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef bminmodule = {
    PyModuleDef_HEAD_INIT,
    "bmin",
    NULL,
    -1,
    bmin_methods
};

PyMODINIT_FUNC PyInit_bmin(void)
{
    return PyModule_Create(&bminmodule);
};

/*--------------------------------------------------------------------------- */
