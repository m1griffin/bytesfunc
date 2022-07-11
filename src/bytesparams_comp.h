//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   bytesparams_comp.c
// Purpose:  Functions for parsing parameters for functions which take two params.
// Language: C
// Date:     31-Oct-2019
//
//------------------------------------------------------------------------------
//
//   Copyright 2014 - 2022    Michael Griffin    <m12.griffin@gmail.com>
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

#include <stdbool.h>

/*--------------------------------------------------------------------------- */

#define ARGSINIT_COMP {0, 0, 0, 0, 0, {NULL}, {NULL}, {NULL}, {NULL}, 0, 0}


enum paramcats
{
	param_arr_num,
	param_num_arr,
	param_arr_arr,
};


// Provide a struct for returning data from parsing Python arguments.
struct args_params_comp {
	int errorcode;
	Py_ssize_t arraylen;
	int nosimd;
	bool hasbuffer1;
	bool hasbuffer2;
	union dataseq bytes1;
	union dataseq bytes2;
	Py_buffer pybuffer1;
	Py_buffer pybuffer2;
	unsigned char param;
	enum paramcats paramcat;
};

/*--------------------------------------------------------------------------- */

struct args_params_comp getparams_comp(PyObject *self, PyObject *args, PyObject *keywds, char *funcname);

void releasebuffers_comp(struct args_params_comp bytesdata);

/*--------------------------------------------------------------------------- */
