//------------------------------------------------------------------------------
// Project:  bytesfunc
// Module:   byteserrs.h
// Purpose:  Common error definitions.
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

/*--------------------------------------------------------------------------- */

#include "Python.h"

/*--------------------------------------------------------------------------- */


void ErrMsgParameterError(void) {
	PyErr_SetString(PyExc_TypeError, "parameter error.");
}

void ErrMsgArrayLengthErr(void) {
	PyErr_SetString(PyExc_IndexError, "bytes or bytearray length error.");
}

void ErrMsgArithOverflowCalc(void) {
	PyErr_SetString(PyExc_OverflowError, "arithmetic overflow in calculation.");
}

void ErrMsgOperatorNotValidforthisFunction(void) {
	PyErr_SetString(PyExc_ValueError, "operator not valid for this function.");
}

void ErrMsgArithOverflowParam(void) {
	PyErr_SetString(PyExc_OverflowError, "arithmetic overflow in parameter.");
}

void ErrMsgOutputNotMutableParam(void) {
	PyErr_SetString(PyExc_TypeError, "output sequence must be mutable.");
}

void ErrMsgArrayLengthMismatch(void) {
	PyErr_SetString(PyExc_TypeError, "sequence length mismatch.");
}

/*--------------------------------------------------------------------------- */
