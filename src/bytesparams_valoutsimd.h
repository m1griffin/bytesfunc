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

/*--------------------------------------------------------------------------- */

#define ARGSINIT_VALOUTSIMD {0, 0, 0, 0, 0, {NULL}, {NULL}}

// Provide a struct for returning data from parsing Python arguments.
struct args_params_valoutsimd {
	char error;
	char bytestype;
	char hasbuffer1;
	int nosimd;
	Py_ssize_t byteslength;
	union dataseq bytes1;
	Py_buffer pybuffer1;
};

/*--------------------------------------------------------------------------- */

struct args_params_valoutsimd getparams_valoutsimd(PyObject *self, PyObject *args, PyObject *keywds, char *funcname);

void releasebuffers_valoutsimd(struct args_params_valoutsimd seqdata);

/*--------------------------------------------------------------------------- */
