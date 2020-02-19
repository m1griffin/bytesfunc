//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_bsum.c
// Purpose:  Common functions for bytesfunc.
// Language: C
// Date:     19-Jan-2020
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

#include "Python.h"

#include <string.h>
#include <limits.h>

#include "byteserrs.h"
#include "bytesparams_base.h"
#include "bytesparams_bsum.h"

/*--------------------------------------------------------------------------- */


// The list of keyword arguments. All argument must be listed, whether we 
// intend to use them for keywords or not. 
static char *kwlist[] = {"data", "matherrors", "maxlen", NULL};


/*--------------------------------------------------------------------------- */

/* Release the buffers which represent the arrays. This function checks if the
 * 	array object was not intiailised.
 * array1 (Py_buffer) = The array object.
 * Returns: Nothing.
*/
void releasebuffers_bsum(struct args_params_bsum bytesdata) {
	if (bytesdata.hasbuffer1) {
		PyBuffer_Release(&bytesdata.pybuffer1);
		bytesdata.hasbuffer1 = 0;
	}
}

/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */


/* Get the parameters passed from Python with a function which takes one array.
 * self, args, keywds = The parameters of the same name passed from the PyObject
 * 		function which forms the original entry point.
 * funcname = A string which represents the C extension name. This is passed to
 * 		PyArg_ParseTupleAndKeywords for error reporting.
 * Returns: A structure which contains the parameter data.
*/
struct args_params_bsum getparams_bsum(PyObject *self, PyObject *args, PyObject *keywds, char *funcname) {


	// This is used to return the parsed parameters.
	struct args_params_bsum bytesdata = ARGSINIT_BSUM;

	PyObject *dataobj1 = NULL;

	struct paramsdata paramobjdata1;

	// Number of elements to work on. If zero or less, ignore this parameter.
	Py_ssize_t bytesmaxlen = 0;
	Py_ssize_t byteslength;

	// If true, *disabled* overflow checking.
	unsigned int ignoreerrors = 0;


	char formatstr[FMTSTRLEN];

	char paramoverflow = 0;

	// -----------------------------------------------------


	// This section determines the type of the arrays.

	// Construct the format string. This is constructed dynamically because
	// we must be able to call this same function from different C extensions.
	makefmtstr("O|in:", funcname, formatstr);

	// Import the raw objects. 
	if (!PyArg_ParseTupleAndKeywords(args, keywds, formatstr, kwlist, &dataobj1, 
							&ignoreerrors, &bytesmaxlen)) {
		ErrMsgParameterError();
		bytesdata.error = 1;
		return bytesdata;
	}


	// Parse the first object parameter. 
	if (get_paramdata(dataobj1, &paramobjdata1, &bytesdata.hasbuffer1, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 2;
		releasebuffers_bsum(bytesdata);
		return bytesdata;
	}


	// The first parameter must be a bytes or bytearray.
	if ((paramobjdata1.paramtype != paramobj_bytes) && (paramobjdata1.paramtype != paramobj_bytearray)) {
		ErrMsgParameterError();
		bytesdata.error = 3;
		releasebuffers_bsum(bytesdata);
		return bytesdata;
	}


	// The number of bytes.
	byteslength = paramobjdata1.pybuffer.len;


	// Collect the parameter data for return to the calling function.
	bytesdata.error = 0;
	bytesdata.ignoreerrors = ignoreerrors;
	bytesdata.byteslength = adjustbytesmaxlen(byteslength, bytesmaxlen);
	bytesdata.bytes1.buf = paramobjdata1.byteseq.buf;
	bytesdata.pybuffer1 = paramobjdata1.pybuffer;


	return bytesdata;

}


/*--------------------------------------------------------------------------- */

