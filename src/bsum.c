//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bsum.c
// Purpose:  Calculate the bsum of values in a bytes or bytearray object.
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

/*--------------------------------------------------------------------------- */



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
"bsum \n\
_____________________________ \n\
\n\
Calculate the arithmetic sum of an bytes or bytearray sequence.  \n\
\n\
======================  ============================================== \n\
Equivalent to:          sum(sequence) \n\
======================  ============================================== \n\
\n\
Call formats: \n\
\n\
  result = bsum(sequence) \n\
  result = bsum(sequence, maxlen=y) \n\
  result = bsum(sequence, matherrors=False) \n\
\n\
* sequence - An input bytes or bytearray to be examined. \n\
* maxlen - Limit the length of the sequence used. This must be a valid \n\
  positive integer. If a zero or negative length, or a value which is \n\
  greater than the actual length of the sequence is specified, this \n\
  parameter is ignored. \n\
* matherrors - If True, checks for numerical errors including integer \n\
  overflow are ignored. \n\
* result - The sum of the sequence. \n\
");


/*--------------------------------------------------------------------------- */

/* A list of all the methods defined by this module. 
 "bsum" is the name seen inside of Python. 
 "py_bsum" is the name of the C function handling the Python call. 
 "METH_VARGS" tells Python how to call the handler. 
 The {NULL, NULL} entry indicates the end of the method definitions. */
static PyMethodDef bsum_methods[] = {
	{"bsum",  (PyCFunction)py_bsum, METH_VARARGS | METH_KEYWORDS, bsum__doc__}, 
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef bsummodule = {
    PyModuleDef_HEAD_INIT,
    "bsum",
    NULL,
    -1,
    bsum_methods
};

PyMODINIT_FUNC PyInit_bsum(void)
{
    return PyModule_Create(&bsummodule);
};

/*--------------------------------------------------------------------------- */

