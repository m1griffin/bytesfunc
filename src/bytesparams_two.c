//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_two.c
// Purpose:  Common functions for arrayfunc.
// Language: C
// Date:     28-Nov-2017
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
#include "bytesparams_two.h"


/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

// The list of keyword arguments. All argument must be listed, whether we 
// intend to use them for keywords or not. 
static char *kwlist_2wsimdwomath[] = {"data1", "data2", "dataout", "maxlen", "nosimd", NULL};

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

/* Release the buffers which represent the arrays. This function checks if the
 * 	array object was initialised before releasing it.
 * bytesdata = Structure which contains the three array buffers to be released.
 * Returns: Nothing.
*/
void releasebuffers_two(struct args_params_2 bytesdata) {

	if (bytesdata.hasbuffer1) {
		PyBuffer_Release(&bytesdata.pybuffer1);
		bytesdata.hasbuffer1 = 0;
	}

	if (bytesdata.hasbuffer2) {
		PyBuffer_Release(&bytesdata.pybuffer2);
		bytesdata.hasbuffer2 = 0;
	}

	if (bytesdata.hasbuffer3) {
		PyBuffer_Release(&bytesdata.pybuffer3);
		bytesdata.hasbuffer3 = 0;
	}

}

/*--------------------------------------------------------------------------- */

/* Determines if the Python object is a bytes or bytearray object.
 * dataobj = The object to be tested.
 * Returns TRUE if a bytes or bytearray object, otherwise returns FALSE.
*/
char isseqobjtype(enum paramtypes paramtype) {
	return ((paramtype == paramobj_bytes) || (paramtype == paramobj_bytearray));
}

/*--------------------------------------------------------------------------- */

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
struct args_params_2 getparams_two(PyObject *self, PyObject *args, PyObject *keywds, char *funcname) {


	// This is used for constructing parameter format strings. The size must
	// be able to hold the largest string, which will be determined by the 
	// names of the functions which use this.
	char formatstr[FMTSTRLEN];
	

	// This is used to return the parsed parameters.
	struct args_params_2 bytesdata = ARGSINIT_TWO;

	PyObject *dataobj1 = NULL;
	PyObject *dataobj2 = NULL;
	PyObject *dataobj3 = NULL;


	struct paramsdata paramobjdata1, paramobjdata2, paramobjdata3;


	// How long the array is.
	Py_ssize_t byteslength;

	// The numeric parameter which may or may not be present.
	unsigned char parampy = 0;

	// Number of elements to work on. If zero or less, ignore this parameter.
	Py_ssize_t bytesmaxlen = 0;

	// If True, SIMD processing is disabled.
	int nosimd = 0;

	// The integer parameter value. We check later to see if it is in range.
	char paramoverflow = 0;

	// If true, the parameter is a sequence. If false, it is assumed
	// to be an integer in the range 0 - 255.
	int param1isseq = 0;
	int param2isseq = 0;

	// If true, then there is a third parameter for data output.
	int hasoutputseq = 0;
	// If true, then the output sequence is mutable (a bytearray).
	int outputmutable = 0;


	// The category of the parameters. That is, what type (array, number, none)
	// of each parameter. 
	enum paramcats paramcat = param_arr_num_none;
	// If true the sequences are all the same length (required).
	int validparamlength = 0;


	// -----------------------------------------------------


	// This section determines the type of the arrays. We do this by parsing
	// the parameters as objects. 

	// Construct the format string. This is constructed dynamically because
	// we must be able to call this same function from different C extensions.
	makefmtstr("OO|Oni:", funcname, formatstr);

	// Import the raw objects. 
	if (!PyArg_ParseTupleAndKeywords(args, keywds, formatstr, kwlist_2wsimdwomath, &dataobj1, 
							&dataobj2, &dataobj3, &bytesmaxlen, &nosimd)) {
		ErrMsgParameterError();
		bytesdata.error = 2;
		return bytesdata;
	}


	// Parse the first object parameter. 
	if (get_paramdata(dataobj1, &paramobjdata1, &bytesdata.hasbuffer1, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 3;
		releasebuffers_two(bytesdata);
		return bytesdata;
	}

	// Parse the second object parameter. 
	if (get_paramdata(dataobj2, &paramobjdata2, &bytesdata.hasbuffer2, &paramoverflow)) {
		ErrMsgParameterError();
		bytesdata.error = 4;
		releasebuffers_two(bytesdata);
		return bytesdata;
	}

	// Parse the third object parameter. This one is optional.
	if (dataobj3 != NULL) {
		if (get_paramdata(dataobj3, &paramobjdata3, &bytesdata.hasbuffer3, &paramoverflow)) {
			ErrMsgParameterError();
			bytesdata.error = 5;
			releasebuffers_two(bytesdata);
			return bytesdata;
		}

		hasoutputseq = 1;
	} else {
		hasoutputseq = 0;
	}


	// Check if the first or second parameters are sequences.
	param1isseq = isseqobjtype(paramobjdata1.paramtype);
	param2isseq = isseqobjtype(paramobjdata2.paramtype);



	// Now determine the parameter pattern.
	if (param1isseq && !param2isseq) {
		if (hasoutputseq) {
			paramcat = param_arr_num_arr;
		} else {
			paramcat = param_arr_num_none;
		}
	}

	if (!param1isseq && param2isseq) {
		if (hasoutputseq) {
			paramcat = param_num_arr_arr;
		} else {
			paramcat = param_num_arr_none;
		}
	}

	if (param1isseq && param2isseq) {
		if (hasoutputseq) {
			paramcat = param_arr_arr_arr;
		} else {
			paramcat = param_arr_arr_none;
		}
	}


	// Check to ensure that the output parameter is writeable (bytearray).
	// Also, get the numeric integer parameter if it is present.
	// Also, get the sequence length.
	switch (paramcat) {
		case param_arr_num_none : {
			outputmutable = isbytearrayobjtype(dataobj1);
			parampy = paramobjdata2.ucharparam;
			byteslength = paramobjdata1.pybuffer.len;
			validparamlength = 1;
			break;
		}
		case param_arr_num_arr : {
			outputmutable = isbytearrayobjtype(dataobj3);
			parampy = paramobjdata2.ucharparam;
			byteslength = paramobjdata1.pybuffer.len;
			validparamlength = (byteslength == paramobjdata3.pybuffer.len);
			break;
		}
		case param_num_arr_none : {
			outputmutable = isbytearrayobjtype(dataobj2);
			parampy = paramobjdata1.ucharparam;
			byteslength = paramobjdata2.pybuffer.len;
			validparamlength = 1;
			break;
		}
		case param_num_arr_arr : {
			outputmutable = isbytearrayobjtype(dataobj3);
			parampy = paramobjdata1.ucharparam;
			byteslength = paramobjdata2.pybuffer.len;
			validparamlength = (byteslength == paramobjdata3.pybuffer.len);
			break;
		}
		case param_arr_arr_none : {
			outputmutable = isbytearrayobjtype(dataobj1);
			byteslength = paramobjdata1.pybuffer.len;
			validparamlength = (byteslength == paramobjdata2.pybuffer.len);
			break;
		}
		case param_arr_arr_arr : {
			outputmutable = isbytearrayobjtype(dataobj3);
			byteslength = paramobjdata1.pybuffer.len;
			validparamlength = ((byteslength == paramobjdata2.pybuffer.len) && (byteslength == paramobjdata3.pybuffer.len));
			break;
		}
		// The parameter pattern is invalid.
		default : {
			ErrMsgParameterError();
			bytesdata.error = 6;
			releasebuffers_two(bytesdata);
			return bytesdata;
			break;
		}
	}

	// If the output is not mutable, signal the error.
	if (!outputmutable) {
		ErrMsgOutputNotMutableParam();
		bytesdata.error = 7;
		releasebuffers_two(bytesdata);
		return bytesdata;
	}


	// All sequences must be the same length.
	if (!validparamlength) {
		ErrMsgArrayLengthMismatch();
		bytesdata.error = 8;
		releasebuffers_two(bytesdata);
		return bytesdata;
	}



	// Collect the parameter data for return to the calling function.
	bytesdata.error = 0;
	bytesdata.nosimd = nosimd;
	bytesdata.paramcat = paramcat;
	bytesdata.byteslength = adjustbytesmaxlen(byteslength, bytesmaxlen);
	bytesdata.bytes1.buf = paramobjdata1.byteseq.buf;
	bytesdata.bytes2.buf = paramobjdata2.byteseq.buf;
	bytesdata.bytes3.buf = paramobjdata3.byteseq.buf;
	bytesdata.pybuffer1 = paramobjdata1.pybuffer;
	bytesdata.pybuffer2 = paramobjdata2.pybuffer;
	bytesdata.pybuffer3 = paramobjdata3.pybuffer;
	bytesdata.param = parampy;
	bytesdata.paramcat = paramcat;


	return bytesdata;

}
