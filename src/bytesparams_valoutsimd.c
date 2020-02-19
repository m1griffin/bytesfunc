//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_valoutsimd.c
// Purpose:  Common functions for bytesfunc.
// Language: C
// Date:     30-Oct-2019
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

#include "Python.h"

#include <string.h>
#include <limits.h>

#include "byteserrs.h"
#include "bytesparams_base.h"
#include "bytesparams_valoutsimd.h"

/*--------------------------------------------------------------------------- */



// The list of keyword arguments. All argument must be listed, whether we 
// intend to use them for keywords or not. 
static char *kwlist[] = {"data", "maxlen", "nosimd", NULL};


/*--------------------------------------------------------------------------- */

/* Release the buffers which represent the sequences. This function checks if the
 * bytes or bytearray object was not intiailised.
 * seq1 (Py_buffer) = The bytes or bytearray object.
 * Returns: Nothing.
*/
void releasebuffers_valoutsimd(struct args_params_valoutsimd bytesdata) {
	if (bytesdata.hasbuffer1) {
		PyBuffer_Release(&bytesdata.pybuffer1);
		bytesdata.hasbuffer1 = 0;
	}
}

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

/* Get the parameters passed from Python with a function which takes one sequence.
 * self, args, keywds = The parameters of the same name passed from the PyObject
 * 		function which forms the original entry point.
 * funcname = A string which represents the C extension name. This is passed to
 * 		PyArg_ParseTupleAndKeywords for error reporting.
 * Returns: A structure which contains the parameter data.
*/
struct args_params_valoutsimd getparams_valoutsimd(PyObject *self, PyObject *args, PyObject *keywds, char *funcname) {


	// This is used to return the parsed parameters.
	struct args_params_valoutsimd bytesdata = ARGSINIT_VALOUTSIMD;

	PyObject *dataobj1 = NULL;

	struct paramsdata paramobjdata1;

	// Number of elements to work on. If zero or less, ignore this parameter.
	Py_ssize_t bytesmaxlen = 0;
	Py_ssize_t byteslength;

	// If True, SIMD processing is disabled.
	int nosimd = 0;

	// This is used to track the types of each bytes or bytearray object.
	char bytestype = 0;

	char formatstr[FMTSTRLEN];

	char paramoverflow = 0;

	// -----------------------------------------------------


	// This section determines the type of the bytes or bytearray object.

	// Construct the format string. This is constructed dynamically because
	// we must be able to call this same function from different C extensions.
	makefmtstr("O|ni:", funcname, formatstr);

	// Import the raw objects. 
	if (!PyArg_ParseTupleAndKeywords(args, keywds, formatstr, kwlist, &dataobj1, 
							&bytesmaxlen, &nosimd)) {
		ErrMsgParameterError();
		bytesdata.error = 1;
		return bytesdata;
	}

	// Parse the first object parameter. 
	if (get_paramdata(dataobj1, &paramobjdata1, &bytesdata.hasbuffer1, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 2;
		releasebuffers_valoutsimd(bytesdata);
		return bytesdata;
	}


	// The first parameter must be an bytes or bytearray.
	if ((paramobjdata1.paramtype != paramobj_bytes) && (paramobjdata1.paramtype != paramobj_bytearray)) {
		ErrMsgParameterError();
		bytesdata.error = 3;
		releasebuffers_valoutsimd(bytesdata);
		return bytesdata;
	}

	// The bytes or bytearray type.
	bytestype = paramobjdata1.bytescode;

	// Get the raw bytes or bytesarray length.
	byteslength = paramobjdata1.pybuffer.len;


	// Collect the parameter data for return to the calling function.
	bytesdata.error = 0;
	bytesdata.bytestype = bytestype;
	bytesdata.nosimd = nosimd;
	bytesdata.byteslength = adjustbytesmaxlen(byteslength, bytesmaxlen);
	bytesdata.bytes1.buf = paramobjdata1.byteseq.buf;
	bytesdata.pybuffer1 = paramobjdata1.pybuffer;


	return bytesdata;

}


/*--------------------------------------------------------------------------- */

