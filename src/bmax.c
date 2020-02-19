//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bmax.c
// Purpose:  Calculate the bmax of values in a bytes or bytearray object.
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
   Returns: The maximum value found.
*/
unsigned char bmax(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x; 
	unsigned char maxfound;

	maxfound = data[0];
	for(x = 0; x < arraylen; x++) {
		if (data[x] > maxfound) {
			maxfound = data[x];
		}
	}

	return maxfound;
}
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For x86-64 SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The maximum value found.
*/
#if defined(AF_HASSIMD_X86)
unsigned char bmax_x86_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char maxfound;

	unsigned char maxvals[CHARSIMDSIZE];
	v16qi maxslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Initialise the comparison values.
	maxslice = (v16qi) __builtin_ia32_lddqu((char *) &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = (v16qi) __builtin_ia32_lddqu((char *) &data[x]);
		maxslice = __builtin_ia32_pmaxub128 (maxslice, dataslice);
	}

	// Find the max within the slice.
	__builtin_ia32_storedqu((char *) maxvals,   maxslice);
	maxfound = maxvals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (maxvals[y] > maxfound) {
			maxfound = maxvals[y];
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] > maxfound) {
			maxfound = data[x];
		}
	}

	return maxfound;
}
#endif
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For ARMv7 NEON SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The maximum value found.
*/
#if defined(AF_HASSIMD_ARM)
unsigned char bmax_armv7_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char maxfound;

	unsigned char maxvals[CHARSIMDSIZE];
	uint8x8_t maxslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen % CHARSIMDSIZE);

	// Initialise the comparison values.
	maxslice = vld1_u8( &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = vld1_u8( &data[x]);
		maxslice = vmax_u8 (maxslice, dataslice);
	}

	// Find the max within the slice.
	vst1_u8( maxvals,   maxslice);
	maxfound = maxvals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (maxvals[y] > maxfound) {
			maxfound = maxvals[y];
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] > maxfound) {
			maxfound = data[x];
		}
	}

	return maxfound;
}
#endif
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The maximum value found.
*/
unsigned char bmax_select(Py_ssize_t arraylen, int nosimd, unsigned char *data) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return bmax_x86_simd(arraylen, data);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return bmax_armv7_simd(arraylen, data);
		#endif
	} else {
	#endif
		return bmax(arraylen, data);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_bmax(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_valoutsimd bytesdata = ARGSINIT_VALOUTSIMD;


	// The output will be an integer.
	unsigned char result;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_valoutsimd(self, args, keywds, "bmax");


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
	result = bmax_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B);

	// Release the buffers. 
	releasebuffers_valoutsimd(bytesdata);

	return PyLong_FromUnsignedLong( (unsigned long) result);


}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(bmax__doc__,
"bmax \n\
_____________________________ \n\
\n\
Calculate bmax over the values in an array.  \n\
\n\
======================  ============================================== \n\
Equivalent to:          max(sequence) \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  result = bmax(sequence) \n\
  result = bmax(sequence, maxlen=y) \n\
  result = bmax(sequence, nosimd=False) \n\
\n\
* sequence - The input bytes or bytearray to be examined. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored. \n\
* nosimd - If True, SIMD acceleration is disabled if present. \n\
  The default is False (SIMD acceleration is enabled if present). \n\
* result = The maximum of all the values in the sequence. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "bmax" is the name seen inside of Python. 
 "py_bmax" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef bmax_methods[] = {
	{"bmax",  (PyCFunction)py_bmax, METH_VARARGS | METH_KEYWORDS, bmax__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef bmaxmodule = {
    PyModuleDef_HEAD_INIT,
    "bmax",
    NULL,
    -1,
    bmax_methods
};

PyMODINIT_FUNC PyInit_bmax(void)
{
    return PyModule_Create(&bmaxmodule);
};

/*--------------------------------------------------------------------------- */
