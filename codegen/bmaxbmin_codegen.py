#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the C code for bmax, bmin.
# Language: Python 3.6
# Date:     01-Nov-2019
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

opstemplate = """//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   %(funclabel)s.c
// Purpose:  Calculate the %(funclabel)s of values in a bytes or bytearray object.
// Language: C
// Date:     30-Oct-2019.
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

#include "simddefs.h"
#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
#include "arm_neon.h"
#endif

#include "bytesparams_base.h"
#include "bytesparams_valoutsimd.h"


/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */
/* arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The %(optype)simum value found.
*/
unsigned char %(funclabel)s(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x; 
	unsigned char %(optype)sfound;

	%(optype)sfound = data[0];
	for(x = 0; x < arraylen; x++) {
		if (data[x] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = data[x];
		}
	}

	return %(optype)sfound;
}
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For x86-64 SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The %(optype)simum value found.
*/
#if defined(AF_HASSIMD_X86)
unsigned char %(funclabel)s_x86_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char %(optype)sfound;

	unsigned char %(optype)svals[CHARSIMDSIZE];
	v16qi %(optype)sslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Initialise the comparison values.
	%(optype)sslice = (v16qi) __builtin_ia32_lddqu((char *) &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = (v16qi) __builtin_ia32_lddqu((char *) &data[x]);
		%(optype)sslice = %(simdvalues_x86)s (%(optype)sslice, dataslice);
	}

	// Find the %(optype)s within the slice.
	__builtin_ia32_storedqu((char *) %(optype)svals,   %(optype)sslice);
	%(optype)sfound = %(optype)svals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (%(optype)svals[y] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = %(optype)svals[y];
		}
	}

	// Get the %(optype)s value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = data[x];
		}
	}

	return %(optype)sfound;
}
#endif
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For ARMv7 NEON SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The %(optype)simum value found.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT)
unsigned char %(funclabel)s_armv7_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char %(optype)sfound;

	unsigned char %(optype)svals[CHARSIMDSIZE];
	uint8x8_t %(optype)sslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Initialise the comparison values.
	%(optype)sslice = vld1_u8( &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = vld1_u8( &data[x]);
		%(optype)sslice = %(simdvalues_armv7)s (%(optype)sslice, dataslice);
	}

	// Find the %(optype)s within the slice.
	vst1_u8( %(optype)svals,   %(optype)sslice);
	%(optype)sfound = %(optype)svals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (%(optype)svals[y] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = %(optype)svals[y];
		}
	}

	// Get the %(optype)s value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = data[x];
		}
	}

	return %(optype)sfound;
}
#endif
/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */
/* For ARMv8 NEON SIMD.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The %(optype)simum value found.
*/
#if defined(AF_HASSIMD_ARM_AARCH64)
unsigned char %(funclabel)s_armv8_simd(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned char %(optype)sfound;

	unsigned char %(optype)svals[CHARSIMDSIZE];
	uint8x16_t %(optype)sslice, dataslice;


	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Initialise the comparison values.
	%(optype)sslice = vld1q_u8( &data[0]);

	// Use SIMD.
	for(x = CHARSIMDSIZE; x < alignedlength; x += CHARSIMDSIZE) {
		dataslice = vld1q_u8( &data[x]);
		%(optype)sslice = %(simdvalues_armv8)s (%(optype)sslice, dataslice);
	}

	// Find the %(optype)s within the slice.
	vst1q_u8( %(optype)svals,   %(optype)sslice);
	%(optype)sfound = %(optype)svals[0];
	for (y = 1; y < CHARSIMDSIZE; y++) {
		if (%(optype)svals[y] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = %(optype)svals[y];
		}
	}

	// Get the %(optype)s value within the left over elements at the end of the array.
	for(x = alignedlength; x < arraylen; x++) {
		if (data[x] %(compare_ops)s %(optype)sfound) {
			%(optype)sfound = data[x];
		}
	}

	return %(optype)sfound;
}
#endif
/*--------------------------------------------------------------------------- */



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data = The input data array.
   Returns: The %(optype)simum value found.
*/
unsigned char %(funclabel)s_select(Py_ssize_t arraylen, int nosimd, unsigned char *data) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return %(funclabel)s_x86_simd(arraylen, data);
		#endif

		#if defined(AF_HASSIMD_ARMv7_32BIT)
			return %(funclabel)s_armv7_simd(arraylen, data);
		#endif

		#if defined(AF_HASSIMD_ARM_AARCH64)
			return %(funclabel)s_armv8_simd(arraylen, data);
		#endif

	} else {
	#endif
		return %(funclabel)s(arraylen, data);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

}
/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_%(funclabel)s(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_valoutsimd bytesdata = ARGSINIT_VALOUTSIMD;


	// The output will be an integer.
	unsigned char result;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_valoutsimd(self, args, keywds, "%(funclabel)s");


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
	result = %(funclabel)s_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B);

	// Release the buffers. 
	releasebuffers_valoutsimd(bytesdata);

	return PyLong_FromUnsignedLong( (unsigned long) result);


}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(%(funclabel)s__doc__,
"%(funclabel)s \\n\\
_____________________________ \\n\\
\\n\\
Calculate %(funclabel)s over the values in an array.  \\n\\
\\n\\
======================  ============================================== \\n\\
Equivalent to:          %(optype)s(sequence) \\n\\
======================  ============================================== \\n\\
\\n\\
Call formats: \\n\\
\\n\\
  result = %(funclabel)s(sequence) \\n\\
  result = %(funclabel)s(sequence, maxlen=y) \\n\\
  result = %(funclabel)s(sequence, nosimd=False) \\n\\
\\n\\
* sequence - The input bytes or bytearray to be examined. \\n\\
* maxlen - Limit the length of the sequence used. This must be a valid \\n\\
  positive integer. If a zero or negative length, or a value which is \\n\\
  greater than the actual length of the sequence is specified, this \\n\\
  parameter is ignored. \\n\\
* nosimd - If True, SIMD acceleration is disabled if present. \\n\\
  The default is False (SIMD acceleration is enabled if present). \\n\\
* result = The %(optype)simum of all the values in the sequence. \\n\\
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

optype = {'bmax' : 'max', 'bmin' : 'min'}
compare_ops = {'bmax' : '>', 'bmin' : '<'}
simdvalues_x86 = {'bmax' : '__builtin_ia32_pmaxub128', 'bmin' : '__builtin_ia32_pminub128'}
simdvalues_armv7 = {'bmax' : 'vmax_u8', 'bmin' : 'vmin_u8'}
simdvalues_armv8 = {'bmax' : 'vmaxq_u8', 'bmin' : 'vminq_u8'}


# ==============================================================================

for funcname in ('bmax', 'bmin'):

	filename = funcname + '.c'

	with open(filename, 'w') as f:

		f.write(opstemplate % {'funclabel' : funcname,
								'optype' : optype[funcname],
								'compare_ops' : compare_ops[funcname],
								'simdvalues_x86' : simdvalues_x86[funcname],
								'simdvalues_armv7' : simdvalues_armv7[funcname],
								'simdvalues_armv8' : simdvalues_armv8[funcname],
								})


# ==============================================================================
