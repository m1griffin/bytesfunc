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

// No error
#define ARR_NO_ERR 0
// The operation requested is not valid for this function.
#define ARR_ERR_INVALIDOP -1
// An arithmetic overflow occurred during a calculation. 
#define ARR_ERR_OVFL -2
// The item requested was not found.
#define ARR_ERR_NOTFOUND -5

/*--------------------------------------------------------------------------- */

// The following functions are used to provide standardized error messages. 
void ErrMsgParameterError(void);
void ErrMsgArrayLengthErr(void);
void ErrMsgArithOverflowCalc(void);
void ErrMsgOperatorNotValidforthisFunction(void);
void ErrMsgArithOverflowParam(void);
void ErrMsgOutputNotMutableParam(void);
void ErrMsgArrayLengthMismatch(void);
