//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_comp.c
// Purpose:  Common functions for bytesfunc.
// Language: C
// Date:     31-Oct-2019
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
#include "bytesparams_comp.h"


/*--------------------------------------------------------------------------- */

// The list of keyword arguments. All argument must be listed, whether we 
// intend to use them for keywords or not. 
static char *kwlist_comp[] = {"data1", "data2", "maxlen", "nosimd", NULL};

/*--------------------------------------------------------------------------- */

/* Release the buffers which represent the sequences. This function checks if the
 * sequence object was not intialised.
 * bytesdata = Structure which contains the buffers to be released.
 * Returns: Nothing.
*/
void releasebuffers_comp(struct args_params_comp bytesdata) {
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

/* Get the parameters passed from Python with a function which takes one input 
 * 		sequence and one input value, or two input sequences.
 * self, args, keywds = The parameters of the same name passed from the PyObject
 * 		function which forms the original entry point.
 * funcname = A string which represents the C extension name. This is passed to
 * 		PyArg_ParseTupleAndKeywords for error reporting.
 * Returns: A structure which contains the parameter data.
*/
struct args_params_comp getparams_comp(PyObject *self, PyObject *args, PyObject *keywds, char *funcname) {


	// This is used for constructing parameter format strings. The size must
	// be able to hold the largest string, which will be determined by the 
	// names of the functions which use this.
	char formatstr[FMTSTRLEN];
	

	// This is used to return the parsed parameters.
	struct args_params_comp bytesdata = ARGSINIT_COMP;

	PyObject *dataobj1 = NULL;
	PyObject *dataobj2 = NULL;

	struct paramsdata paramobjdata1, paramobjdata2;


	// How long the sequence is.
	Py_ssize_t byteslength;

	// The numeric parameter which may or may not be present.
	unsigned char parampy = 0;

	// Number of elements to work on. If zero or less, ignore this parameter.
	Py_ssize_t bytesmaxlen = 0;
	// If True, SIMD processing is disabled.
	int nosimd = 0;


	char paramoverflow = 0;

	// The category of the parameters. That is, what type (sequence, number, none)
	// of each parameter. 
	enum paramcats paramcat;

	// Track which of the parameters is a bytes or bytearray object. 
	int param1issequence, param2issequence;
	

	// -----------------------------------------------------


	// This section determines the type of the sequence. We do this by parsing
	// the parameters as objects. We then examine the parameters 

	// Construct the format string. This is constructed dynamically because
	// we must be able to call this same function from different C extensions.
	makefmtstr("OO|ni:", funcname, formatstr);

	// Import the raw objects. 
	if (!PyArg_ParseTupleAndKeywords(args, keywds, formatstr, kwlist_comp, &dataobj1, 
							&dataobj2, &bytesmaxlen, &nosimd)) {
		ErrMsgParameterError();
		bytesdata.error = 2;
		return bytesdata;
	}


	// Parse the first object parameter. 
	if (get_paramdata(dataobj1, &paramobjdata1, &bytesdata.hasbuffer1, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 3;
		releasebuffers_comp(bytesdata);
		return bytesdata;
	}

	// Parse the second object parameter. 
	if (get_paramdata(dataobj2, &paramobjdata2, &bytesdata.hasbuffer2, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 4;
		releasebuffers_comp(bytesdata);
		return bytesdata;
	}

	// Determine which of the parameters are bytes or bytearrays. For the purposes of the functions
	// we are dealing with here it doesn't matter which of the two they are as they do not
	// alter the data.
	param1issequence = ((paramobjdata1.paramtype == paramobj_bytes) || (paramobjdata1.paramtype == paramobj_bytearray));
	param2issequence = ((paramobjdata2.paramtype == paramobj_bytes) || (paramobjdata2.paramtype == paramobj_bytearray));


	// Either the first or second parameter (or both) must be an bytes or bytearray sequence.
	if ((!param1issequence) && (!param2issequence)) {
		ErrMsgParameterError();
		bytesdata.error = 5;
		releasebuffers_comp(bytesdata);
		return bytesdata;
	}


	// Both parameters are bytes or bytearray sequences.
	if (param1issequence && param2issequence) {
		if (paramobjdata1.pybuffer.len != paramobjdata2.pybuffer.len) {
			ErrMsgParameterError();
			bytesdata.error = 7;
			releasebuffers_comp(bytesdata);
			return bytesdata;
		} else {
			// This keeps track of the pattern of parameters.
			paramcat = param_arr_arr;
			// The number of bytes.
			byteslength = paramobjdata1.pybuffer.len;
		}
	} else {
		// The first parameter is a bytes or bytearray sequence and the 
		// second is an integer.
		if (param1issequence && (!param2issequence)) {
			parampy = paramobjdata2.ucharparam;

			// This keeps track of the pattern of parameters.
			paramcat = param_arr_num;
			// The number of bytes.
			byteslength = paramobjdata1.pybuffer.len;
		} else {
			// The second parameter is a bytes or bytearray sequence and the 
			// first is an integer.
			if ((!param1issequence) && param2issequence) {
				parampy = paramobjdata1.ucharparam;

				// This keeps track of the pattern of parameters.
				paramcat = param_num_arr;
				// The number of bytes.
				byteslength = paramobjdata2.pybuffer.len;
			} else {
				// An invalid parameter combination. This should have been
				// caught previously, but we check it again.
				ErrMsgParameterError();
				bytesdata.error = 8;
				releasebuffers_comp(bytesdata);
				return bytesdata;
			}
		}
	}



	bytesdata.error = 0;
	bytesdata.byteslength = adjustbytesmaxlen(byteslength, bytesmaxlen);
	bytesdata.nosimd = nosimd;
	bytesdata.bytes1.buf = paramobjdata1.byteseq.buf;
	bytesdata.bytes2.buf = paramobjdata2.byteseq.buf;
	bytesdata.pybuffer1 = paramobjdata1.pybuffer;
	bytesdata.pybuffer2 = paramobjdata2.pybuffer;
	bytesdata.param = parampy;
	bytesdata.paramcat = paramcat;


	return bytesdata;

}


/*--------------------------------------------------------------------------- */

