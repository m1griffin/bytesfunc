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

/*--------------------------------------------------------------------------- */

// The maximum length of dynamically created format strings.
#define FMTSTRLEN 25

/*--------------------------------------------------------------------------- */


// The data arrays. Each element represents a different data type.
union dataseq {
	uint8_t *buf;
	unsigned char *B;
};


// The categories that a parameter can fall into.
enum paramtypes
{ 
	paramobj_error,
	paramobj_bytes,
	paramobj_bytearray,
	paramobj_uchar,
};

// This holds both sequence and numeric (integer) data values.
// This is used to parse the parameters.
struct paramsdata {
	char bytescode;
	unsigned char ucharparam;
	Py_buffer pybuffer;
	union dataseq byteseq;
	enum paramtypes paramtype;
};

/*--------------------------------------------------------------------------- */

Py_ssize_t adjustbytesmaxlen(Py_ssize_t byteslength, Py_ssize_t bytesmaxlen);
	
void makefmtstr(char *basestr, char *funcname, char *formatstr);

int get_paramdata(PyObject *dataobj, struct paramsdata *paramobjdata, char *hasbuffer, char *paramoverflow);

char isbytesobjtype(PyObject *dataobj);
char isbytearrayobjtype(PyObject *dataobj);

/*--------------------------------------------------------------------------- */
