#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the C code for bsum.
# Language: Python 3.4
# Date:     18-Mar-2018
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
#include "bytesparams_bsum.h"

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
unsigned long long bsum_unsigned_char(Py_ssize_t arraylen, unsigned char *data, signed int *errflag, signed int ignoreerrors) { 

	// array index counter. 
	Py_ssize_t x; 
	unsigned long long partialsum = 0;

	*errflag = 0;
	// Overflow checking disabled.
	if (ignoreerrors) {
		for (x = 0; x < arraylen; x++) {
			partialsum = partialsum + data[x];
		}
	} else {
		// Overflow checking enabled.
		for (x = 0; x < arraylen; x++) {
			if (data[x] > (ULLONG_MAX - partialsum)) { 
				*errflag = ARR_ERR_OVFL;
				return partialsum; 
			}
			partialsum = partialsum + data[x];
		}
	}

	return partialsum;
}
/*--------------------------------------------------------------------------- */

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
	if (bytesdata.error) {
		return NULL;
	}


	// The length of the data array.
	if (bytesdata.byteslength < 1) {
		// Release the buffers. 
		releasebuffers_bsum(bytesdata);
		ErrMsgArrayLengthErr();
		return NULL;
	}


	// Call the implementing function.
	resultull = bsum_unsigned_char(bytesdata.byteslength, bytesdata.bytes1.B, &errflag, bytesdata.ignoreerrors);
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
\\n\\
* sequence - An input bytes or bytearray to be examined. \\n\\
* maxlen - Limit the length of the sequence used. This must be a valid \\n\\
  positive integer. If a zero or negative length, or a value which is \\n\\
  greater than the actual length of the sequence is specified, this \\n\\
  parameter is ignored. \\n\\
* matherrors - If True, checks for numerical errors including integer \\n\\
  overflow are ignored. \\n\\
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


funcname = 'bsum'

# Create the source code based on templates.
filename = funcname + '.c'
with open(filename, 'w') as f:
	# The copyright notice and common includes.
	f.write(sumbin_head % {'funclabel' : funcname})
	# The implementing code.
	f.write(bsum_code)
	# The boilerplate at the end.
	f.write(footer_boilerplate % {'funclabel' : funcname})


