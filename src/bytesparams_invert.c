//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_invert.c
// Purpose:  Common functions for a bytes or bytearray.
// Language: C
// Date:     30-Jan-2020
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
#include "bytesparams_invert.h"


/*--------------------------------------------------------------------------- */


// The list of keyword arguments. All argument must be listed, whether we 
// intend to use them for keywords or not. 
static char *kwlist_invert[] = {"data", "dataout", "maxlen", "nosimd", NULL};


/*--------------------------------------------------------------------------- */

/* Release the buffers which represent the sequences. This function checks if the
 * 	sequences object was not intiailised.
 * bytesdata = Structure which contains the buffers to be released.
 * Returns: Nothing.
*/
void releasebuffers_one(struct args_params_1 bytesdata) {
	if (bytesdata.hasbuffer1) {
		PyBuffer_Release(&bytesdata.pybuffer1);
		bytesdata.hasbuffer1 = 0;
	}

	if (bytesdata.hasbuffer2) {
		PyBuffer_Release(&bytesdata.pybuffer2);
		bytesdata.hasbuffer2 = 0;
	}
}

/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */


/* Get the parameters passed from Python with a function which takes one or
 * 		optionally, two arrays.
 * self, args, keywds = The parameters of the same name passed from the PyObject
 * 		function which forms the original entry point.
 * funcname = A string which represents the C extension name. This is passed to
 * 		PyArg_ParseTupleAndKeywords for error reporting.
 * Returns: A structure which contains the parameter data.
*/
struct args_params_1 getparams_one(PyObject *self, PyObject *args, PyObject *keywds, char *funcname) {


	// This is used to return the parsed parameters.
	struct args_params_1 bytesdata = ARGSINIT_ONE;

	PyObject *dataobj1 = NULL;
	PyObject *dataobj2 = NULL;

	struct paramsdata paramobjdata1, paramobjdata2;

	// How long the array is.
	Py_ssize_t byteslength;

	// Number of elements to work on. If zero or less, ignore this parameter.
	Py_ssize_t bytesmaxlen = 0;

	// If True, SIMD processing is disabled.
	int nosimd = 0;

	char paramoverflow = 0;

	// If true, then there is a third parameter for data output.
	int hasoutputseq = 0;
	// If true, then the output sequence is mutable (a bytearray).
	int outputmutable = 0;
	// If true the sequences are all the same length (required).
	int validparamlength = 0;


	char formatstr[FMTSTRLEN];

	// -----------------------------------------------------


	// This section determines the type of the arrays.

	// Construct the format string. This is constructed dynamically because
	// we must be able to call this same function from different C extensions.
	makefmtstr("O|Oni:", funcname, formatstr);

	// Import the raw objects. 
	if (!PyArg_ParseTupleAndKeywords(args, keywds, formatstr, kwlist_invert, &dataobj1, 
							&dataobj2, &bytesmaxlen, &nosimd)) {
		ErrMsgParameterError();
		bytesdata.error = 1;
		return bytesdata;
	}



	// Parse the first object parameter. 
	if (get_paramdata(dataobj1, &paramobjdata1, &bytesdata.hasbuffer1, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 2;
		releasebuffers_one(bytesdata);
		return bytesdata;
	}


	// Parse the second object parameter. This one is optional.
	if (dataobj2 != NULL) {
		if (get_paramdata(dataobj2, &paramobjdata2, &bytesdata.hasbuffer2, &paramoverflow)) {
			ErrMsgParameterError();
			bytesdata.error = 3;
			releasebuffers_one(bytesdata);
			return bytesdata;
		}
	
		hasoutputseq = 1;
	} else {
		hasoutputseq = 0;
	}


	// Get the seqeuence length.
	byteslength = paramobjdata1.pybuffer.len;

	// Check if the sequences are compatible with respect to length
	// and if the output is mutable (writable).
	if (hasoutputseq) {
		validparamlength = (byteslength == paramobjdata2.pybuffer.len);
		outputmutable = isbytearrayobjtype(dataobj2);
	} else {
		validparamlength = 1;
		outputmutable = isbytearrayobjtype(dataobj1);
	}

	// If the output is not mutable, signal the error.
	if (!outputmutable) {
		ErrMsgOutputNotMutableParam();
		bytesdata.error = 4;
		releasebuffers_one(bytesdata);
		return bytesdata;
	}


	// All sequences must be the same length.
	if (!validparamlength) {
		ErrMsgArrayLengthMismatch();
		bytesdata.error = 5;
		releasebuffers_one(bytesdata);
		return bytesdata;
	}


	// Collect the parameter data for return to the calling function.
	bytesdata.error = 0;
	bytesdata.hasoutputseq = hasoutputseq;
	bytesdata.nosimd = nosimd;
	bytesdata.byteslength = adjustbytesmaxlen(byteslength, bytesmaxlen);
	bytesdata.bytes1.buf = paramobjdata1.byteseq.buf;
	bytesdata.bytes2.buf = paramobjdata2.byteseq.buf;
	bytesdata.pybuffer1 = paramobjdata1.pybuffer;
	bytesdata.pybuffer2 = paramobjdata2.pybuffer;


	return bytesdata;


}


/*--------------------------------------------------------------------------- */

