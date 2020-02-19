//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_allany.c
// Purpose:  Common functions for arrayfunc.
// Language: C
// Date:     28-Nov-2017
//
//------------------------------------------------------------------------------
//
//   Copyright 2014 - 2018    Michael Griffin    <m12.griffin@gmail.com>
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
#include "arrayops.h"
#include "bytesparams_allany.h"

/*--------------------------------------------------------------------------- */

// The list of keyword arguments. All argument must be listed, whether we 
// intend to use them for keywords or not. 
static char *kwlist_allany[] = {"op", "data", "param", "maxlen", "nosimd", NULL};

/*--------------------------------------------------------------------------- */

/* Release the buffers which represent the arrays. This function checks if the
 * 	array object was not intiailised.
 * bytesdata = Structure which contains the three array buffers to be released.
 * Returns: Nothing.
*/
void releasebuffers_allany(struct args_params_allany bytesdata) {
	if (bytesdata.hasbuffer1) {
		PyBuffer_Release(&bytesdata.pybuffer1);
		bytesdata.hasbuffer1 = 0;
	}

}

/*--------------------------------------------------------------------------- */

/* Get the parameters passed from Python with a function which takes one input 
 * 		array and one input value, or two input arrays, plus an optional
 * 		output array.
 * self, args, keywds = The parameters of the same name passed from the PyObject
 * 		function which forms the original entry point.
 * funcname = A string which represents the C extension name. This is passed to
 * 		PyArg_ParseTupleAndKeywords for error reporting.
 * Returns: A structure which contains the parameter data.
*/
struct args_params_allany getparams_allany(PyObject *self, PyObject *args, PyObject *keywds, char *funcname) {


	// This is used for constructing parameter format strings. The size must
	// be able to hold the largest string, which will be determined by the 
	// names of the functions which use this.
	char formatstr[FMTSTRLEN];
	

	// This is used to return the parsed parameters.
	struct args_params_allany bytesdata = ARGSINIT_ALLANY;

	PyObject *dataobj1 = NULL;
	PyObject *opstr = NULL;

	struct paramsdata paramobjdata1;


	// How long the array is.
	Py_ssize_t byteslength;


	// Number of elements to work on. If zero or less, ignore this parameter.
	Py_ssize_t bytesmaxlen = 0;
	// If True, SIMD processing is disabled.
	int nosimd = 0;
	// The integer parameter value. We check later to see if it is in range.
	int paramval = 0;


	char paramoverflow = 0;
	signed int opcode = 0;



	// -----------------------------------------------------


	// This section determines the type of the arrays. We do this by parsing
	// the parameters as objects. We then examine the parameters 

	// Construct the format string. This is constructed dynamically because
	// we must be able to call this same function from different C extensions.
	makefmtstr("UOi|ni:", funcname, formatstr);

	// Import the raw objects. 
	if (!PyArg_ParseTupleAndKeywords(args, keywds, formatstr, kwlist_allany, &opstr, 
					&dataobj1, &paramval, &bytesmaxlen, &nosimd)) {
		ErrMsgParameterError();
		bytesdata.error = 1;
		return bytesdata;
	}

	// Convert the command string to an integer.
	opcode = opstrdecode(opstr);

	// Check if the command string is valid.
	if (opcode < 0) {
		ErrMsgOperatorNotValidforthisFunction();
		bytesdata.error = 2;
		// Release the buffers. 
		releasebuffers_allany(bytesdata);
		return bytesdata;
	}


	// Parse the second parameter. 
	if (get_paramdata(dataobj1, &paramobjdata1, &bytesdata.hasbuffer1, &paramoverflow)) {
		if (paramoverflow) {
			ErrMsgArithOverflowParam();
		} else {
			ErrMsgParameterError();
		}
		bytesdata.error = 3;
		releasebuffers_allany(bytesdata);
		return bytesdata;
	}


	// The second parameter must be a bytes or bytearray object.
	if ((paramobjdata1.paramtype != paramobj_bytes) && (paramobjdata1.paramtype != paramobj_bytearray)) {
		ErrMsgParameterError();
		bytesdata.error = 4;
		releasebuffers_allany(bytesdata);
		return bytesdata;
	}


	// Get the raw array length.
	byteslength = paramobjdata1.pybuffer.len;


	// Check that the parameter value is in range.
	if ((paramval < 0) || (paramval > 255)) {
		ErrMsgArithOverflowParam();
		bytesdata.error = 5;
		releasebuffers_allany(bytesdata);
		return bytesdata;
	}


	bytesdata.error = 0;
	bytesdata.opcode = opcode;
	bytesdata.byteslength = adjustbytesmaxlen(byteslength, bytesmaxlen);
	bytesdata.nosimd = nosimd;
	bytesdata.bytes1.buf = paramobjdata1.byteseq.buf;
	bytesdata.pybuffer1 = paramobjdata1.pybuffer;
	bytesdata.param = paramval;


	return bytesdata;

}


/*--------------------------------------------------------------------------- */

