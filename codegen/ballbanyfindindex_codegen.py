#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the C code for ball, bany, findindex.
# Language: Python 3.4
# Date:     19-Jan-2020
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

import itertools

import codegen_common


# ==============================================================================

allany_head = """//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   %(funclabel)s.c
// Purpose:  Calculate the %(funclabel)s of values in a bytes or bytearray object.
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
"""

# ==============================================================================

# The basic template for ball.
ops_ball = """
/*--------------------------------------------------------------------------- */
/* Non-SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true for all array elements, or ARR_ERR_NOTFOUND
		 if it was false at least once.
*/
signed int ball_%(opcode)s(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (!(data[index] %(compare_ops)s param1)) {
			return ARR_ERR_NOTFOUND;
		}
	}
	return 1;

}



/*--------------------------------------------------------------------------- */
/* x86 SIMD version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true for all array elements, or ARR_ERR_NOTFOUND
		 if it was false at least once.
*/
#if defined(AF_HASSIMD_X86)
signed int ball_%(opcode)s_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice%(SIMD_x86_compslice)s;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		%(SIMD_x86_ops)s
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (!(data[index] %(compare_ops)s param1)) {
			return ARR_ERR_NOTFOUND;
		}
	}

	return 1;

}

#endif


/*--------------------------------------------------------------------------- */
/* ARMv7 version.
   opcode = The operator or function code to select what to execute.
   arraylen = The length of the data arrays.
   data = The input data array.
   param1 = The parameter to be applied to each array element.
   nosimd = If true, disable SIMD.
   Returns 1 if the condition was true for all array elements, or ARR_ERR_NOTFOUND
		 if it was false at least once.
*/
#if defined(AF_HASSIMD_ARM)
signed int ball_%(opcode)s_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

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
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = %(SIMD_ARM_comp)s(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (%(SIMD_ARM_vresult)s) {
			return ARR_ERR_NOTFOUND;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (!(data[index] %(compare_ops)s param1)) {
			return ARR_ERR_NOTFOUND;
		}
	}

	return 1;

}

#endif



/*--------------------------------------------------------------------------- */
/* This selects the correct function, whether the platform independent non-SIMD
   version, or the architecture appropriate SIMD version.
   arraylen = The length of the data arrays.
   data1 = The first data array.
   param = The parameter to be applied to each array element.
*/
signed int ball_%(opcode)s_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return ball_%(opcode)s_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return ball_%(opcode)s_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return ball_%(opcode)s(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */


"""


# ==============================================================================

# The basic template for the non-SIMD version of bany.
ops_bany = """
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
signed int bany_%(opcode)s(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

	for (index = 0; index < arraylen; index++) {
		if (data[index] %(compare_ops)s param1) {
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
signed int bany_%(opcode)s_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice%(SIMD_x86_compslice)s;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		%(SIMD_x86_ops)s
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] %(compare_ops)s param1) {
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
#if defined(AF_HASSIMD_ARM)
signed int bany_%(opcode)s_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

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
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = %(SIMD_ARM_comp)s(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (%(SIMD_ARM_vresult)s) {
			return 1;
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] %(compare_ops)s param1) {
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
signed int bany_%(opcode)s_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return bany_%(opcode)s_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return bany_%(opcode)s_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return bany_%(opcode)s(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */


"""


# ==============================================================================

# The basic template for the non-SIMD version of findindex.
ops_findindex = """
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
Py_ssize_t findindex_%(opcode)s(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 
	// array index counter.
	Py_ssize_t index;

		for (index = 0; index < arraylen; index++) {
			if (data[index] %(compare_ops)s param1) {
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
Py_ssize_t findindex_%(opcode)s_x86_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

	// array index counter. 
	Py_ssize_t index, fineindex; 

	// SIMD related variables.
	Py_ssize_t alignedlength;
	unsigned int y;

	v16qi datasliceleft, datasliceright;
	v16qi resultslice%(SIMD_x86_compslice)s;
	unsigned char compvals[CHARSIMDSIZE];

	// Initialise the comparison values.
	for (y = 0; y < CHARSIMDSIZE; y++) {
		compvals[y] = param1;
	}
	datasliceright = (v16qi) __builtin_ia32_lddqu((char *) compvals);

	// Calculate array lengths for arrays whose lengths which are not even
	// multipes of the SIMD slice length.
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	// On x86 we have to do this in a round-about fashion for some
	// types of comparison operations due to how SIMD works on that
	// platform.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = (v16qi) __builtin_ia32_lddqu((char *) &data[index]);
		%(SIMD_x86_ops)s
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] %(compare_ops)s param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] %(compare_ops)s param1) {
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
Py_ssize_t findindex_%(opcode)s_armv7_simd(Py_ssize_t arraylen, unsigned char *data, unsigned char param1) { 

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
	alignedlength = arraylen - (arraylen %% CHARSIMDSIZE);

	// Perform the main operation using SIMD instructions.
	for (index = 0; index < alignedlength; index += CHARSIMDSIZE) {
		datasliceleft = vld1_u8( &data[index]);
		// The actual SIMD operation. 
		resultslice = %(SIMD_ARM_comp)s(datasliceleft, datasliceright);
		if (%(SIMD_ARM_vresult)s) {
			// Home in on the exact location.
			for (fineindex = index; fineindex < alignedlength; fineindex++) {
				if (data[fineindex] %(compare_ops)s param1) {
					return fineindex;
				}
			}
		}
	}

	// Get the max value within the left over elements at the end of the array.
	for (index = alignedlength; index < arraylen; index++) {
		if (data[index] %(compare_ops)s param1) {
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
Py_ssize_t findindex_%(opcode)s_select(Py_ssize_t arraylen, int nosimd, unsigned char *data1, unsigned char param) { 

	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	if (!nosimd && (arraylen >= (CHARSIMDSIZE * 2))) {
		#if defined(AF_HASSIMD_X86)
			return findindex_%(opcode)s_x86_simd(arraylen, data1, param);
		#endif

		#if defined(AF_HASSIMD_ARM)
			return findindex_%(opcode)s_armv7_simd(arraylen, data1, param);
		#endif
	} else {
	#endif
		return findindex_%(opcode)s(arraylen, data1, param);
	#if defined(AF_HASSIMD_X86) || defined(AF_HASSIMD_ARM)
	}
	#endif

}
/*--------------------------------------------------------------------------- */


"""


# ==============================================================================


# ==============================================================================


allany_params = """
/*--------------------------------------------------------------------------- */

/* The wrapper to the underlying C function */
static PyObject *py_%(funclabel)s(PyObject *self, PyObject *args, PyObject *keywds) {


	// The error code returned by the function.
	%(resultcode)s resultcode = 0;

	// This is used to hold the parsed parameters.
	struct args_params_allany bytesdata = ARGSINIT_ALLANY;

	// -----------------------------------------------------


	// Get the parameters passed from Python.
	bytesdata = getparams_allany(self, args, keywds, "%(funclabel)s");

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
			resultcode = %(funclabel)s_eq_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_GT
		case OP_AF_GT: {
			resultcode = %(funclabel)s_gt_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_GE
		case OP_AF_GE: {
			resultcode = %(funclabel)s_ge_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_LT
		case OP_AF_LT: {
			resultcode = %(funclabel)s_lt_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_LE
		case OP_AF_LE: {
			resultcode = %(funclabel)s_le_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
			break;
		}
		// AF_NE
		case OP_AF_NE: {
			resultcode = %(funclabel)s_ne_select(bytesdata.byteslength, bytesdata.nosimd, bytesdata.bytes1.B, bytesdata.param);
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


%(return_result)s

}


/*--------------------------------------------------------------------------- */


/* The module doc string */
PyDoc_STRVAR(%(funclabel)s__doc__,
"%(funclabel)s \\n\\
_____________________________ \\n\\
\\n\\
Calculate %(funclabel)s over the values a bytes or bytearray object. \\n\\
\\n\\
======================  ============================================== \\n\\
Equivalent to:          %(opcodedocs)s \\n\\
======================  ============================================== \\n\\
\\n\\
Call formats: \\n\\
\\n\\
  result = %(funclabel)s(opstr, sequence, param) \\n\\
  result = %(funclabel)s(opstr, sequence, param, maxlen=y) \\n\\
  result = %(funclabel)s(opstr, sequence, param, nosimd=False) \\n\\
\\n\\
* opstr - The arithmetic comparison operation as a string. \\n\\
          These are: '==', '>', '>=', '<', '<=', '!='. \\n\\
* sequence - An input bytes or bytearray to be examined. \\n\\
* param - A non-array numeric parameter. \\n\\
* maxlen - Limit the length of the sequence used. This must be a valid \\n\\
  positive integer. If a zero or negative length, or a value which is \\n\\
  greater than the actual length of the sequence is specified, this \\n\\
  parameter is ignored. \\n\\
* nosimd - If True, SIMD acceleration is disabled if present. \\n\\
  The default is False (SIMD acceleration is enabled if present). \\n\\
* %(resultdoc)s \\n\\
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



# Template for the return of the result code for ball or bany.
allany_return = '''
	// Return whether compare was OK.
	if (resultcode == ARR_ERR_NOTFOUND) {
		Py_RETURN_FALSE;
	} else {
		Py_RETURN_TRUE;
	}
'''

# Template for the return of the index position for findindex.
findindex_return = '''
	// Adjust the result code if the data was not found, so that we don't leak
	// internal error codes to user space (and cause problems if they change).
	if (resultcode < 0) {
		resultcode = -1;
	}

	// Return the number of items filtered through.
	return PyLong_FromSsize_t(resultcode);
'''


return_templates = {'ball' : allany_return, 
			'bany' : allany_return, 
			'findindex' : findindex_return
}


# ==============================================================================


# ==============================================================================


# SIMD code for x86. These handle the comparison operations. This must be
# done in a round about way for x86 due to the way it works on that platform.
# This set covers unsigned integer operations only.

# For ball
# param_arr_num
SIMD_x86_uint_ball_templates = {
'eq' : '''// Compare the slices.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return ARR_ERR_NOTFOUND;
		}''',
'ge' : '''// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return ARR_ERR_NOTFOUND;
		}''',
'gt' : '''// Make sure they're not equal.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return ARR_ERR_NOTFOUND;
		}
		// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return ARR_ERR_NOTFOUND;
		}''',
'le' : '''// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return ARR_ERR_NOTFOUND;
		}''',
'lt' : '''// Make sure they're not equal.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return ARR_ERR_NOTFOUND;
		}
		// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then the test
		// has failed.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return ARR_ERR_NOTFOUND;
		}''',
'ne' : '''// Compare for equality.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return ARR_ERR_NOTFOUND;
		}''',
}


# ==============================================================================

# This set covers unsigned integer operations only.
# For bany.

# param_arr_num
SIMD_x86_uint_bany_templates = {
'eq' : '''// Compare the slices.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return 1;
		}''',
'ge' : '''// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then a least.
		// one value is less than.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return 1;
		}''',
'gt' : '''// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is greater than. 
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return 1;
		}''',
'le' : '''// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is less than or equal to.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {
			return 1;
		}''',
'lt' : '''// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is less than.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return 1;
		}''',
'ne' : '''// Compare for equality.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {
			return 1;
		}''',
}


# ==============================================================================

# This set covers unsigned integer operations only.
# For findindex.

# param_arr_num
SIMD_x86_uint_findindex_templates = {
'eq' : '''// Compare the slices.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {''',
'ge' : '''// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is greater than or equal to.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {''',
'gt' : '''// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is greater than. 
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Check the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {''',
'le' : '''// Find the maximum values. 
		compslice = __builtin_ia32_pmaxub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is less than or equal to.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0x0000) {''',
'lt' : '''// Find the minimum values. 
		compslice = __builtin_ia32_pminub128(datasliceleft, datasliceright);
		// If this is different from our compare parameter, then at
		// least one value is less than.
		resultslice = __builtin_ia32_pcmpeqb128(compslice, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {''',
'ne' : '''// Compare for equality.
		resultslice = __builtin_ia32_pcmpeqb128(datasliceleft, datasliceright);
		// Compare the results of the SIMD operation.
		if (__builtin_ia32_pmovmskb128((v16qi) resultslice) != 0xffff) {''',
}



# ==============================================================================

# SIMD templates for x86. These make the compare decisions and are 
# substituted into the main SIMD template.
SIMD_x86_SIMD_int_templates = {
	'ball' : SIMD_x86_uint_ball_templates, 
	'bany' : SIMD_x86_uint_bany_templates,
	'findindex' : SIMD_x86_uint_findindex_templates,
}


# ==============================================================================
# Which compare operations need an additional vector for intermediate results.
# This depends both upon array type and function.

compslice = ', compslice'

# For ball
SIMD_x86_compslice_uint_ball = {
	'eq' : '',
	'ge' : compslice,
	'gt' : compslice,
	'le' : compslice,
	'lt' : compslice,
	'ne' : ''
}


# For bany.
SIMD_x86_compslice_uint_bany = {
	'eq' : '',
	'ge' : compslice,
	'gt' : compslice,
	'le' : compslice,
	'lt' : compslice,
	'ne' : ''
}


# For findindex.
SIMD_x86_compslice_uint_findindex = {
	'eq' : '',
	'ge' : compslice,
	'gt' : compslice,
	'le' : compslice,
	'lt' : compslice,
	'ne' : ''
}


SIMD_x86_compslice = {
	'ball' : SIMD_x86_compslice_uint_ball, 
	'bany' : SIMD_x86_compslice_uint_bany, 
	'findindex' : SIMD_x86_compslice_uint_findindex
}



# ==============================================================================


# ==============================================================================

# For ARM NEON.

# Compare result to see if OK. 
# 'ne' must be handled differently. 

# ball
arm_vresult_8_ball = 'vreinterpret_u64_u8(resultslice) != 0xffffffffffffffff'
arm_vresult_8_ne_ball = 'vreinterpret_u64_u8(resultslice) != 0x0000000000000000'

arm_vreslt_8_total_ball = {
		'eq' : arm_vresult_8_ball,
		'ge' : arm_vresult_8_ball,
		'gt' : arm_vresult_8_ball,
		'le' : arm_vresult_8_ball,
		'lt' : arm_vresult_8_ball,
		'ne' : arm_vresult_8_ne_ball,
		}


# bany
arm_vresult_8_bany = 'vreinterpret_u64_u8(resultslice) != 0x0000000000000000'
arm_vresult_8_ne_bany = 'vreinterpret_u64_u8(resultslice) != 0xffffffffffffffff'

arm_vreslt_8_total_bany = {
		'eq' : arm_vresult_8_bany,
		'ge' : arm_vresult_8_bany,
		'gt' : arm_vresult_8_bany,
		'le' : arm_vresult_8_bany,
		'lt' : arm_vresult_8_bany,
		'ne' : arm_vresult_8_ne_bany,
		}


# findindex
arm_vresult_8_findindex = 'vreinterpret_u64_u8(resultslice) != 0x0000000000000000'
arm_vresult_8_ne_findindex = 'vreinterpret_u64_u8(resultslice) != 0xffffffffffffffff'

arm_vreslt_8_total_findindex = {
		'eq' : arm_vresult_8_findindex,
		'ge' : arm_vresult_8_findindex,
		'gt' : arm_vresult_8_findindex,
		'le' : arm_vresult_8_findindex,
		'lt' : arm_vresult_8_findindex,
		'ne' : arm_vresult_8_ne_findindex,
		}


arm_vresult = {
	'ball' : arm_vreslt_8_total_ball, 
	'bany' : arm_vreslt_8_total_bany, 
	'findindex' : arm_vreslt_8_total_findindex,
}



# The ARM SIMD ops for compare. The NE op must be combined with a 
# different vresult as there is no actual not equal op.
arm_simdops = {
	'eq' : 'vceq_u8',
	'ge' : 'vcge_u8',
	'gt' : 'vcgt_u8',
	'le' : 'vcle_u8',
	'lt' : 'vclt_u8',
	'ne' : 'vceq_u8'
}


# ==============================================================================

# ==============================================================================


maindescription = 'Returns True if all elements in an array meet the selected criteria.'

# The original date of the platform independent C code.
ccodedate = '08-May-2014'


# The functions which are implemented by this program.
completefuncnames = ('ball', 'bany', 'findindex')

# The non-SIMD implementation of the operation. 
ops_calls = {'ball' : ops_ball, 
			'bany' : ops_bany, 
			'findindex' : ops_findindex
}


# The return codes for each function.
resultcodetemplates = {'ball' : 'signed int', 
			'bany' : 'signed int', 
			'findindex' : 'Py_ssize_t'
}

# The comparison operator names and symbols.
operations = (('eq', '=='), ('gt', '>'), ('ge', '>='), ('lt', '<'), ('le', '<='), ('ne', '!='))


# Used for the help text in the function.
bany_docs = '''result - A boolean value corresponding to the result of all the \\n\\
  comparison operations. If any comparison operations result in true, \\n\\
  the return value will be true. If all of them result in false, the \\n\\
  return value will be false.'''

ball_docs = '''result - A boolean value corresponding to the result of all the \\n\\
  comparison operations. If all comparison operations result in true, \\n\\
  the return value will be true. If any of them result in false, the \\n\\
  return value will be false.'''

findindex_docs = 'result - The resulting index. This will be negative if no match was found.'

resultdoc = {'ball' : bany_docs, 
			'bany' : ball_docs, 
			'findindex' : findindex_docs
}

opcodedocs = {'ball' : 'all([(x > param) for x in array])', 
			'bany' : 'any([(x > param) for x in array])', 
			'findindex' : '[x for x,y in enumerate(array) if y > param][0]'
}


# ==============================================================================



# ==============================================================================
# Output the generated code.


# Output the functions which implement the individual implementation functions.
for funcname in completefuncnames:

	filename = funcname + '.c'

	# Select the implementation template for the current function.
	optemplate = ops_calls[funcname]

	with open(filename, 'w') as f:
		f.write(allany_head % {'funclabel' : funcname})


		# Each compare operation.
		for opcode, compareop in operations:

			f.write(optemplate % {'opcode' : opcode,
						'compare_ops' : compareop,
						'funclabel' : funcname,
						'opcode' : opcode,
						'compare_ops' : compareop,
						'SIMD_x86_compslice' : SIMD_x86_compslice[funcname][opcode],
						'SIMD_x86_ops' : SIMD_x86_SIMD_int_templates[funcname][opcode],
						'SIMD_ARM_comp' : arm_simdops[opcode],
						'SIMD_ARM_vresult' : arm_vresult[funcname][opcode],
						})



		#####

		# The program entry point and parameter parsing and code.
		f.write(allany_params % {'funclabel' : funcname,
								'return_result' : return_templates[funcname],
								'opcodedocs' : opcodedocs[funcname],
								'resultdoc' : resultdoc[funcname],
								'resultcode' : resultcodetemplates[funcname],
								})



# ==============================================================================

