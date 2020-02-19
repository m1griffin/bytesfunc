//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_base.c
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

/*--------------------------------------------------------------------------- */

/*--------------------------------------------------------------------------- */


/* Determines whether to iterate over the entire length of the bytes or 
   bytearray, or if only part of the sequence is to be used. If for example 
   a sequence which was filtered as part of a previous step is to be operated on, 
   only part of the sequence may contain valid data.
*/
Py_ssize_t adjustbytesmaxlen(Py_ssize_t byteslength, Py_ssize_t bytesmaxlen) {
	if ((bytesmaxlen > 0) && (bytesmaxlen < byteslength)) {
		return bytesmaxlen;
	} else {
		return byteslength;
	}
}

/*--------------------------------------------------------------------------- */


/* Create the format string from two substrings, one the base format and one
 * with the name of the C extension.
 * basestr = The first part of the desired format string.
 * funcname = The name of the function to be added to the end.
 * formatstr = The output string.
 * Assert: The lengths of basestr and funcname are less than the size of formatstr.
*/
void makefmtstr(char *basestr, char *funcname, char *formatstr) {

	// Make sure there won't be a string overflow. While the sizes are fixed,
	// we could have a programming error.
	assert((strlen(basestr) + strlen(funcname)) < FMTSTRLEN);

	strcat(strcpy(formatstr, basestr), funcname);
}


/*--------------------------------------------------------------------------- */

/* Determines if the Python object is an bytes object.
 * dataobj = The object to be tested.
 * Returns TRUE if a bytes object, otherwise returns FALSE.
*/
char isbytesobjtype(PyObject *dataobj) {

	if (dataobj == NULL) { return 0; }

	// Check if is bytes object.
	return (strcmp(dataobj->ob_type->tp_name, "bytes") == 0);

}



/* Determines if the Python object is an bytearray object.
 * dataobj = The object to be tested.
 * Returns TRUE if a bytearray object, otherwise returns FALSE.
*/
char isbytearrayobjtype(PyObject *dataobj) {

	if (dataobj == NULL) { return 0; }

	// Check if is bytearray object.
	return (strcmp(dataobj->ob_type->tp_name, "bytearray") == 0);

}


/*--------------------------------------------------------------------------- */

/* Determines whether to iterate over the entire length of the sequence, or if
   only part of the sequence is to be used. If for example a sequence which was
   filtered as part of a previous step is to be operated on, only part of the
   sequence may contain valid data.
*/
Py_ssize_t adjustseqmaxlen(Py_ssize_t seqlength, Py_ssize_t seqmaxlen) {
	if ((seqmaxlen > 0) && (seqmaxlen < seqlength)) {
		return seqmaxlen;
	} else {
		return seqlength;
	}
}

/*--------------------------------------------------------------------------- */

// Unsigned data is not checked for overflow by the PyArg_ParseTuple template 
// strings. This means we must use a larger data size and then check manually
// to see if it is withing the expected range.

// Returns true if the parameter is within the correct range for an unsigned char.
// B
char isunsignedcharrange(unsigned long long x) {
	return ((x <= UCHAR_MAX) && (x >= 0));
}

// Is signed integer data in the range of unsigned char data.
char isunsignedcharrangewithsigned(long long x) {
	return ((x <= UCHAR_MAX) && (x >= 0));
}

/*--------------------------------------------------------------------------- */


/*--------------------------------------------------------------------------- */

/* Take a single python parameter object and get the data. This could be an
   integer, bytes object, or bytearray.
   
   dataobj = A parameter as a PyObject (not parsed).
   paramobjdata = A structure which will be used to return the data extracted
     from dataobj. Different fields will be valid depending on what the type of
     data in dataobj was. 
   hasbuffer = If 1, a buffer handle was obtained and must be released. If 0,
     there is no buffer to be released (either not a buffer object, or was not
     obtained.
   paramoverflow = If non-zero, a parameter overflowed, otherwise OK.
   Returns 0 if OK, otherwise non-zero.

*/
int get_paramdata(PyObject *dataobj, struct paramsdata *paramobjdata, char *hasbuffer, char *paramoverflow) {

	// Used to track overflows in integer conversions.
	int intparamoverflow = 0;
	// temporary variables for parsing data.
	long long llintparam;
	unsigned long long ullintparam;
	Py_buffer datapy;


	*hasbuffer = 0;
	*paramoverflow = 0;

	// Parameter is a sequence.
	if (PyObject_CheckBuffer(dataobj)) {
		// Check that this is actually an bytes object or bytearray 
		// and not some other buffer type.
		if(!isbytesobjtype(dataobj) && !isbytearrayobjtype(dataobj)) {
			paramobjdata->paramtype = paramobj_error;
			return -1;
		}

		// Not entirely sure if PyBUF_ND is the correct flag.
		if (PyObject_GetBuffer(dataobj, &datapy, PyBUF_ND)) {
			paramobjdata->paramtype = paramobj_error;
			return -2;
		}

		paramobjdata->pybuffer = datapy;

		// Determine whether bytes or bytearray.
		if (isbytesobjtype(dataobj)) {
			paramobjdata->paramtype = paramobj_bytes;
		} else {
			paramobjdata->paramtype = paramobj_bytearray;
		}
		paramobjdata->byteseq.buf = datapy.buf;
		*hasbuffer = 1;
		return 0;

	// Not an array, so expect a number.
	} else {
		// Parameter is an integer.
		if (PyLong_Check(dataobj)) {
			// Check if a signed long long.
			llintparam = PyLong_AsLongLongAndOverflow(dataobj, &intparamoverflow);
			// No overflow, so we can treat it as a signed long long.
			if (!intparamoverflow) {
				if (isunsignedcharrangewithsigned(llintparam)) {
					paramobjdata->ucharparam = (char) llintparam;
					paramobjdata->paramtype = paramobj_uchar;
					return 0;
				} else {
					*hasbuffer = 1;
					paramobjdata->paramtype = paramobj_error;
					return -3;
				}

			// If it overflowed, it could be an unsigned long long.
			} else {
				ullintparam = PyLong_AsUnsignedLongLong(dataobj);

				// An overflow happened. The integer is too large to represent
				// as a native integer.
				if ((ullintparam == (unsigned long long)-1) && PyErr_Occurred()) {
					paramobjdata->paramtype = paramobj_error;
					*paramoverflow = 1;
					return -4;
				}
				if (isunsignedcharrange(ullintparam)) {
					paramobjdata->ucharparam = ullintparam;
					paramobjdata->paramtype = paramobj_uchar;
					return 0;
				} else {
					*hasbuffer = 1;
					paramobjdata->paramtype = paramobj_error;
					return -1;
				}
			}

		// Parameter is not of a supported type.
		} else {
			paramobjdata->paramtype = paramobj_error;
			return -5;
		}
	}

	// If we reach this point, something has gone wrong.
	return -6;
}


/*--------------------------------------------------------------------------- */


