#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the C code for bsum.
# Language: Python 3.4
# Date:     18-Mar-2018
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

# Main heading for bsum and invert.
sumbin_head = """//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   %(funclabel)s.c
// Purpose:  Calculate the %(funclabel)s of values in a bytes or bytearray object.
// Language: C
// Date:     19-Jan-2020.
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
#include "bytesparams_bsum.h"

#include "simddefs.h"

#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
#include "arm_neon.h"
#endif

/*--------------------------------------------------------------------------- */

/* These are for use with bsum to optimize overflow checking performance by 
   determining if an array is short enough that there is no risk that the 
   accumulated sum may overflow when summing that data type. 
   Each value represents the maximum number of array elements for which it is 
   safe to skip overflow checks without risk of integer overflow even if the 
   array is full of the largest values for that type. 
   These are defined for known architectures as there seems to be no platform
   independent means of determining whether it is being compiled for 32 or 64
   bits. Array indexes are limited to a value related to Py_ssize_t. However
   Py_ssize_t will vary depending on whether Python is compiled for 32 or 64 
   bits. There is currently no means of determining the size of Py_ssize_t
   at compile time due to the way it is defined.
*/

#if defined( __x86_64__ ) ||  defined( __i386__ ) ||  defined( __ARM_64BIT_STATE ) ||  defined( __ARM_32BIT_STATE )

// 64 bit architectures.
#if defined( __x86_64__ ) ||  defined( __ARM_64BIT_STATE )

#define SKIPOVFLCHECK 72057594037927936LL

#endif


// 32 bit architectures.
#if defined( __i386__ ) ||  defined( __ARM_32BIT_STATE )

#define SKIPOVFLCHECK 2147483648

#endif


#else
// Default values for unknown architectures which don't trigger the optimization. 

// Array codes B, b
#define SKIPOVFLCHECK 0

#endif

#define skipovflcheck(arraylen) (arraylen <= SKIPOVFLCHECK)

/*--------------------------------------------------------------------------- */

// This defines the "chunk" size used to process integer arrays in pieces small
// enough that overflow cannot occur within the "chunk".
#define LOOPCHUNKSIZE 256


// Integer overflow checks.

// Unsigned integer - new value will cause an integer overflow.
#define loop_willoverflow_unsigned(val, partialsum) (val > (ULLONG_MAX - partialsum))


/*--------------------------------------------------------------------------- */

"""

# ==============================================================================

# The implementation for bsum.
bsum_code = """

/*--------------------------------------------------------------------------- */
/* For array code: B
   arraylen = The length of the data array.
   data = The input data array.
   errflag = Set to true if an overflow error occured in integer operations.
   ignoreerrors = If true, arithmetic overflow checking is disabled.
   Returns: The sum of the array.
*/
unsigned long long bsum_unsigned_char(Py_ssize_t arraylen, unsigned char *data, signed int *errflag, signed int ignoreerrors, signed int nosimd) { 

	// array index counter. 
	Py_ssize_t x; 
	unsigned long long partialsum = 0;

	*errflag = 0;

	#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	if (!nosimd && enoughforsimd(arraylen, CHARSIMDSIZE)) {
		// Overflow checking disabled.
		if (ignoreerrors || skipovflcheck(arraylen)) {
			partialsum = bsum_unsigned_char_simd(arraylen, data);
		} else {
			partialsum = bsum_unsigned_char_simd_ovfl(arraylen, data, errflag);
		}

	} else {
	#endif

		// Overflow checking disabled.
		if (ignoreerrors || skipovflcheck(arraylen)) {
			for (x = 0; x < arraylen; x++) {
				partialsum = partialsum + (unsigned long long) data[x];
			}
		} else {
			// Overflow checking enabled.
			for (x = 0; x < arraylen; x++) {
				if (data[x] > (ULLONG_MAX - partialsum)) { 
					*errflag = ARR_ERR_OVFL;
					return partialsum; 
				}
				partialsum = partialsum + (unsigned long long) data[x];
			}
		}
	#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
	}
	#endif

	return partialsum;
}
/*--------------------------------------------------------------------------- */
"""

# ==============================================================================
# Template for integer SIMD support for ARMv7 and ARMv8 only.
ops_simdsupport_arm_innerloop = """
/*--------------------------------------------------------------------------- */

/* For array code: B
   arraylen = The length of the data array.
   data = The input data array.
   Returns: The sum of the array.
*/
// This inner loop is used to sum small chunks of the array.
%(simdplatform)s
unsigned long long innerloop_bsum_unsigned_char%(simdfunclabel)s(Py_ssize_t arraylen, unsigned char *data) { 

	// array index counter. 
	Py_ssize_t x, alignedlength; 
	unsigned int y;
	unsigned long long partialsum = 0;

	unsigned short sumvals[CHARSIMDSIZE / 2];
	%(simdattr)s dataslice;
	%(simdattr2)s resultslice;


	// Initialise the accumulator.
	resultslice = %(simdinitaccu)s(0);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = calcalignedlength(arraylen, CHARSIMDSIZE);

	// Use SIMD.
	for (x = 0; x < alignedlength; x += CHARSIMDSIZE) {

		// Load the data into the vector register.
		dataslice = %(simdload)s( &data[x]);

		// The actual SIMD operation. 
		resultslice = %(simdop)s(resultslice, dataslice);

	}

	// Add up the values within the slice.
	%(simdop2)s(sumvals, resultslice);
	for (y = 0; y < (CHARSIMDSIZE / 2); y++) {
		partialsum = partialsum + sumvals[y];
	}

	// Add the values within the left over elements at the end of the array.
	for (x = alignedlength; x < arraylen; x++) {
		partialsum = partialsum + (unsigned long long) data[x];
	}

	return partialsum;

}
#endif

"""

# This is needed only once.
ops_simdsupport_arm_outerloop = """

/*--------------------------------------------------------------------------- */
/* For array code: B
   arraylen = The length of the data array.
   data = The input data array.
   Returns: The sum of the array.
*/
// Version without error checking.
#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
unsigned long long bsum_unsigned_char_simd(Py_ssize_t arraylen, unsigned char *data) { 

	Py_ssize_t x, loopremaining, loopchunk;
	unsigned long long partialsum = 0;

	for(x=0; x < arraylen; x += LOOPCHUNKSIZE) {
		// The array is summed in "chunks" using SIMD and then each
		// chunk added to the total.
		loopremaining = arraylen - x;
		loopchunk = (loopremaining >  LOOPCHUNKSIZE) ? LOOPCHUNKSIZE : loopremaining;

		// Add the chunk to the grand total.
#if defined(AF_HASSIMD_ARMv7_32BIT)
		partialsum = partialsum + innerloop_bsum_unsigned_char_armv7_simd(loopchunk, &data[x]);
#endif

#if defined(AF_HASSIMD_ARM_AARCH64)
		partialsum = partialsum + innerloop_bsum_unsigned_char_armv8_simd(loopchunk, &data[x]);
#endif


	}

	return partialsum;

}
#endif

/*--------------------------------------------------------------------------- */

/* For array code: B
   arraylen = The length of the data array.
   data = The input data array.
   errflag = Set to true if an error occured.
   Returns: The sum of the array.
*/
#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)
unsigned long long bsum_unsigned_char_simd_ovfl(Py_ssize_t arraylen, unsigned char *data, signed int *errflag) { 

	unsigned long long partialsum = 0;
	unsigned long long chunksum;
	Py_ssize_t x, loopremaining, loopchunk;

	for(x=0; x < arraylen; x += LOOPCHUNKSIZE) {
		// The array is summed in "chunks" using SIMD and then each
		// chunk added to the total.
		loopremaining = arraylen - x;
		loopchunk = (loopremaining >  LOOPCHUNKSIZE) ? LOOPCHUNKSIZE : loopremaining;

		// Add up one "chunk" of the array.
#if defined(AF_HASSIMD_ARMv7_32BIT)
		chunksum = innerloop_bsum_unsigned_char_armv7_simd(loopchunk, &data[x]);
#endif

#if defined(AF_HASSIMD_ARM_AARCH64)
		chunksum = innerloop_bsum_unsigned_char_armv8_simd(loopchunk, &data[x]);
#endif

		// Check for overflow.
		if (loop_willoverflow_unsigned(chunksum, partialsum)) {
			*errflag = ARR_ERR_OVFL;
			return partialsum; 
		}

		// Add the chunk to the grand total.
		partialsum = partialsum + chunksum;
	}

	return partialsum;

}
#endif

/*--------------------------------------------------------------------------- */

"""


# ==============================================================================

# Parsing the params.
bsum_params = """
/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_bsum(PyObject *self, PyObject *args, PyObject *keywds) {


	// This is used to hold the parsed parameters.
	struct args_params_bsum bytesdata = ARGSINIT_BSUM;

	// The sum of the array, as a python object.
	PyObject *sumreturn;

	// Indicates an error.
	signed int errflag = 0;

	// Arithmetic result.
	unsigned long long resultull = 0;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_bsum(self, args, keywds, "bsum");

	// If there was an error, we count on the parameter parsing function to 
	// release the buffers if this was necessary.
	if (bytesdata.errorcode) {
		return NULL;
	}


	// The length of the data array.
	if (bytesdata.arraylen < 1) {
		// Release the buffers. 
		releasebuffers_bsum(bytesdata);
		ErrMsgArrayLengthErr();
		return NULL;
	}


	// Call the implementing function.
	resultull = bsum_unsigned_char(bytesdata.arraylen, bytesdata.bytes1.B, &errflag, bytesdata.ignoreerrors, bytesdata.nosimd);
	sumreturn = PyLong_FromUnsignedLongLong(resultull);

	// Release the buffers. 
	releasebuffers_bsum(bytesdata);


	// Signal the errors.

	if (errflag == ARR_ERR_OVFL) {
		ErrMsgArithOverflowCalc();
		return NULL;
	}


	return sumreturn;

}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(bsum__doc__,
"bsum \\n\\
_____________________________ \\n\\
\\n\\
Calculate the arithmetic sum of an bytes or bytearray sequence.  \\n\\
\\n\\
======================  ============================================== \\n\\
Equivalent to:          sum(sequence) \\n\\
======================  ============================================== \\n\\
\\n\\
Call formats: \\n\\
\\n\\
  result = bsum(sequence) \\n\\
  result = bsum(sequence, maxlen=y) \\n\\
  result = bsum(sequence, matherrors=False) \\n\\
  result = bsum(sequence, nosimd=False) \\n\\
\\n\\
* sequence - An input bytes or bytearray to be examined. \\n\\
* maxlen - Limit the length of the sequence used. This must be a valid \\n\\
  positive integer. If a zero or negative length, or a value which is \\n\\
  greater than the actual length of the sequence is specified, this \\n\\
  parameter is ignored. \\n\\
* matherrors - If True, checks for numerical errors including integer \\n\\
  overflow are ignored. \\n\\
* nosimd - If True, SIMD acceleration is disabled if present. The \\n\\
  default is False (SIMD acceleration is enabled if present). \\n\\
* result - The sum of the sequence. \\n\\
");

"""

# ==============================================================================


footer_boilerplate = """
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

# Supported SIMD platforms.
SIMD_platform_ARMv7 = '#if defined(AF_HASSIMD_ARMv7_32BIT)'
SIMD_platform_ARM64v8 = '#if defined(AF_HASSIMD_ARM_AARCH64)'
SIMD_platform_ARM = '#if defined(AF_HASSIMD_ARMv7_32BIT) || defined(AF_HASSIMD_ARM_AARCH64)'


# SIMD support.
simd_armv7 = {
	'simdplatform' : SIMD_platform_ARMv7,
	'simdfunclabel' : '_armv7_simd',
	'simdattr' : 'uint8x8_t',
	'simdattr2' : 'uint16x4_t',
	'simdinitaccu' : 'vdup_n_u16',
	'simdload' : 'vld1_u8',
	'simdop' : 'vpadal_u8',
	'simdop2' : 'vst1_u16',
}

simd_armv8 = {
	'simdplatform' : SIMD_platform_ARM64v8,
	'simdfunclabel' : '_armv8_simd',
	'simdattr' : 'uint8x16_t',
	'simdattr2' : 'uint16x8_t',
	'simdinitaccu' : 'vdupq_n_u16',
	'simdload' : 'vld1q_u8',
	'simdop' : 'vpadalq_u8',
	'simdop2' : 'vst1q_u16',
}

# ==============================================================================


funcname = 'bsum'

# Create the source code based on templates.
filename = funcname + '.c'
with open(filename, 'w') as f:
	# The copyright notice and common includes.
	f.write(sumbin_head % {'funclabel' : funcname})
	# The implementing code.

	# SIMD support for ARMv7
	f.write(ops_simdsupport_arm_innerloop % simd_armv7)
	# SIMD support for ARMv8
	f.write(ops_simdsupport_arm_innerloop % simd_armv8)

	# Platform independent SIMD.
	f.write(ops_simdsupport_arm_outerloop)

	f.write(bsum_code)
	f.write(bsum_params)
	# The boilerplate at the end.
	f.write(footer_boilerplate % {'funclabel' : funcname})


