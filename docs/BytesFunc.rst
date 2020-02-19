=========
BytesFunc
=========

:Authors:
    Michael Griffin
    

:Version: 1.0.0 for 2020-02-19
:Copyright: 2014 - 2020
:License: This document may be distributed under the Apache License V2.0.
:Language: Python 3.5 or later


.. contents:: Table of Contents

---------------------------------------------------------------------

Introduction
============

The BytesFunc module provides high speed array processing functions for use with
Python 'bytes' and 'bytearray' objects. These functions are patterned after the
functions in the standard Python "operator" module together with some additional 
ones from other sources.

The purpose of these functions is to perform mathematical calculations on 
"bytes" and "bytearray" objects significantly faster than using native Python.

---------------------------------------------------------------------

Function Summary
================

The compare operators used for 'ball', 'bany', and 'findindex' are examples
only, and other compare operations are available. Many functions will accept
other parameter combinations of sequences and numeric parameters. See the
details for each function for what parameter combinations are valid.


Brief Description
-----------------

=========== ==================================================
  Function       Equivalent to
=========== ==================================================
      and\_  Perform a bitwise AND across the sequence.
       ball  True if all elements of the sequence meet the match criteria.
       bany  True if any elements of the sequence meet the match criteria.
       bmax  Return the maximum value in the sequence.
       bmin  Return the minimum value in the sequence.
       bsum  Return the sum of the sequence.
         eq  True if all elements of the sequence equal the compare value.
  findindex  Returns the index of the first value in an array to meet the
             specified criteria.
         ge  True if all elements of the sequence are greater than or equal to 
             the compare value.
         gt  True if all elements of the sequence are greater than the compare 
             value.
     invert  Perform a bitwise invert across the sequence.
         le  True if all elements of the sequence are less than or equal to the 
             compare value.
     lshift  Perform a bitwise left shift across the sequence.
         lt  True if all elements of the sequence are less than the compare 
             value.
         ne  True if all elements of the sequence are not equal the compare 
             value.
       or\_  Perform a bitwise OR across the sequence.
     rshift  Perform a bitwise right shift across the sequence.
        xor  Perform a bitwise XOR across the sequence.
=========== ==================================================


Python Equivalent
-----------------


=========== ==================================================
  Function       Equivalent to
=========== ==================================================
      and\_ [x & param for x in sequence1]
       ball all([(x > param) for x in array])
       bany any([(x > param) for x in array])
       bmax max(sequence)
       bmin min(sequence)
       bsum sum(sequence)
         eq all([x == param for x in sequence])
  findindex [x for x,y in enumerate(array) if y > param][0]
         ge all([x >= param for x in sequence])
         gt all([x > param for x in sequence])
     invert [~x for x in sequence1]
         le all([x <= param for x in sequence])
     lshift [x << param for x in sequence1]
         lt all([x < param for x in sequence])
         ne all([x != param for x in sequence])
       or\_ [x | param for x in sequence1]
     rshift [x >> param for x in sequence1]
        xor [x ^ param for x in sequence1]
=========== ==================================================



---------------------------------------------------------------------

Description
===========

Parameters
----------

Parameter Formats
_________________

Parameters come in several forms.

* Sequences. Sequences are either "bytes" or "bytearray" objects. Bytes 
  sequences are immutable and must not be used for output destinations. 
  Bytearray sequences are mutable, and may be used for inputs or outputs.
* Numeric parameters. Numeric input parameters are individual integers and must 
  be in the range of 0 to 255.
* Comparison operators. Comparison operators are unicode strings in the form 
  used by Python for compare operations. These must be quoted strings, and not 
  bare Python symbols. See the section below for a list of these.
* Sequence length control. Sequence length control allows only part of a 
  sequence to be used as an input. See the section below for details.
* Overflow detection disable. Overflow detection control is used for disable 
  integer overflow. See the section below for details.

Example::

  sequence = bytes([1, 2, 5, 99, 8])
  # Find the maximum value and return it. The answer should be 99.
  result = bytesfunc.bmax(sequence)

Example::

  sequence1 = bytes([1, 2, 5, 99, 8])
  sequence2 = bytearray([0, 0, 0, 0, 0])
  # Xor each element in sequence1 with '7', and write the output to
  # sequence2. Sequence2 should be bytearray(b'\x06\x05\x02d\x0f').
  bytesfunc.xor(sequence1, 7, sequence2)

Example::

  sequence1 = bytes([1, 2, 5, 99, 8, 101])
  # Find the first index of sequence1 which is greater than or equal to 99.
  # The answer should be 3.
  result = bytesfunc.findindex('>=', sequence, 99)


Function Documentation Details
------------------------------




and\_
_____________________________

Calculate and\_ over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [x & param for x in sequence1]
or                      [param & x for x in sequence1]
or                      [x & y for x,y in zip(sequence1, sequence2)]
======================  ==============================================

Call formats::

  and_(sequence1, param)
  and_(sequence1, param, outpsequence)
  and_(param, sequence1)
  and_(param, sequence1, outpsequence)
  and_(sequence1, sequence2)
  and_(sequence1, sequence2, outpsequence)
  and_(sequence1, param, maxlen=y)
  and_(sequence1, param, nosimd=False)

* sequence1 - The first input data bytes or bytearray sequence to be
  examined. If no output sequence is provided the results will overwrite
  the input data.
* param - A non-sequence numeric parameter.
* sequence2 - A second input data sequence. Each element in this sequence is
  applied to the corresponding element in the first sequence.
* outpsequence - The output sequence. This parameter is optional.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled. This parameter is


ball
_____________________________

Calculate ball over the values a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([(x > param) for x in array])
======================  ==============================================

Call formats::

  result = ball(opstr, sequence, param)
  result = ball(opstr, sequence, param, maxlen=y)
  result = ball(opstr, sequence, param, nosimd=False)

* opstr - The arithmetic comparison operation as a string.
          These are: '==', '>', '>=', '<', '<=', '!='.
* sequence - An input bytes or bytearray to be examined.
* param - A non-array numeric parameter.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If any comparison operations result in true,
  the return value will be true. If all of them result in false, the
  return value will be false.


bany
_____________________________

Calculate bany over the values a bytes or bytearray object.

======================  ==============================================
Equivalent to:          any([(x > param) for x in array])
======================  ==============================================

Call formats::

  result = bany(opstr, sequence, param)
  result = bany(opstr, sequence, param, maxlen=y)
  result = bany(opstr, sequence, param, nosimd=False)

* opstr - The arithmetic comparison operation as a string.
          These are: '==', '>', '>=', '<', '<=', '!='.
* sequence - An input bytes or bytearray to be examined.
* param - A non-array numeric parameter.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


bmax
_____________________________

Calculate bmax over the values in an array.

======================  ==============================================
Equivalent to:          max(sequence)
======================  ==============================================

Call formats::

  result = bmax(sequence)
  result = bmax(sequence, maxlen=y)
  result = bmax(sequence, nosimd=False)

* sequence - The input bytes or bytearray to be examined.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result = The maximum of all the values in the sequence.


bmin
_____________________________

Calculate bmin over the values in an array.

======================  ==============================================
Equivalent to:          min(sequence)
======================  ==============================================

Call formats::

  result = bmin(sequence)
  result = bmin(sequence, maxlen=y)
  result = bmin(sequence, nosimd=False)

* sequence - The input bytes or bytearray to be examined.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result = The minimum of all the values in the sequence.


bsum
_____________________________

Calculate the arithmetic sum of an bytes or bytearray sequence.

======================  ==============================================
Equivalent to:          sum(sequence)
======================  ==============================================

Call formats::

  result = bsum(sequence)
  result = bsum(sequence, maxlen=y)
  result = bsum(sequence, matherrors=False)

* sequence - An input bytes or bytearray to be examined.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* matherrors - If True, checks for numerical errors including integer
  overflow are ignored.
* result - The sum of the sequence.


eq
_____________________________

Calculate eq over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([x == param for x in sequence])
or                      all([param == x for x in sequence])
or                      all([x == y for x,y in zip(sequence1, sequence2)])
======================  ==============================================

Call formats::

  result = eq(sequence1, param)
  result = eq(param, sequence1)
  result = eq(sequence1, sequence2)
  result = eq(sequence1, param, maxlen=y)
  result = eq(sequence1, param, nosimd=False)

* sequence1 - An input bytes or bytearray to be examined.
* sequence2 - An input bytes or bytearray to be examined.
* param - A integer numeric input parameter in the range 0 - 255.
* The first and second parameters are compared to each other. If one
  parameter is a sequence and the other is an integer, the integer
  is compared to each element in the sequence. If both parameters are
  sequences, each element of one sequence is compared to the
  corresponding element of the other sequence.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


findindex
_____________________________

Calculate findindex over the values a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [x for x,y in enumerate(array) if y > param][0]
======================  ==============================================

Call formats::

  result = findindex(opstr, sequence, param)
  result = findindex(opstr, sequence, param, maxlen=y)
  result = findindex(opstr, sequence, param, nosimd=False)

* opstr - The arithmetic comparison operation as a string.
          These are: '==', '>', '>=', '<', '<=', '!='.
* sequence - An input bytes or bytearray to be examined.
* param - A non-array numeric parameter.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - The resulting index. This will be negative if no match was found.


ge
_____________________________

Calculate ge over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([x >= param for x in sequence])
or                      all([param >= x for x in sequence])
or                      all([x >= y for x,y in zip(sequence1, sequence2)])
======================  ==============================================

Call formats::

  result = ge(sequence1, param)
  result = ge(param, sequence1)
  result = ge(sequence1, sequence2)
  result = ge(sequence1, param, maxlen=y)
  result = ge(sequence1, param, nosimd=False)

* sequence1 - An input bytes or bytearray to be examined.
* sequence2 - An input bytes or bytearray to be examined.
* param - A integer numeric input parameter in the range 0 - 255.
* The first and second parameters are compared to each other. If one
  parameter is a sequence and the other is an integer, the integer
  is compared to each element in the sequence. If both parameters are
  sequences, each element of one sequence is compared to the
  corresponding element of the other sequence.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


gt
_____________________________

Calculate gt over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([x > param for x in sequence])
or                      all([param > x for x in sequence])
or                      all([x > y for x,y in zip(sequence1, sequence2)])
======================  ==============================================

Call formats::

  result = gt(sequence1, param)
  result = gt(param, sequence1)
  result = gt(sequence1, sequence2)
  result = gt(sequence1, param, maxlen=y)
  result = gt(sequence1, param, nosimd=False)

* sequence1 - An input bytes or bytearray to be examined.
* sequence2 - An input bytes or bytearray to be examined.
* param - A integer numeric input parameter in the range 0 - 255.
* The first and second parameters are compared to each other. If one
  parameter is a sequence and the other is an integer, the integer
  is compared to each element in the sequence. If both parameters are
  sequences, each element of one sequence is compared to the
  corresponding element of the other sequence.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


invert
_____________________________

Calculate invert over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [~x for x in sequence1]
======================  ==============================================

Call formats::

    invert(sequence1)
    invert(sequence1, outpseq)
    invert(sequence1, maxlen=y)
    invert(sequence1, nosimd=False)

* sequence1 - The input bytes or bytearray to be examined. If no output
  bytearray is provided the results will overwrite the input data, in which
  case it must be a bytearray.
* outpseq - The output bytearray. This parameter is optional.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled. This parameter is
  optional. The default is FALSE.


le
_____________________________

Calculate le over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([x <= param for x in sequence])
or                      all([param <= x for x in sequence])
or                      all([x <= y for x,y in zip(sequence1, sequence2)])
======================  ==============================================

Call formats::

  result = le(sequence1, param)
  result = le(param, sequence1)
  result = le(sequence1, sequence2)
  result = le(sequence1, param, maxlen=y)
  result = le(sequence1, param, nosimd=False)

* sequence1 - An input bytes or bytearray to be examined.
* sequence2 - An input bytes or bytearray to be examined.
* param - A integer numeric input parameter in the range 0 - 255.
* The first and second parameters are compared to each other. If one
  parameter is a sequence and the other is an integer, the integer
  is compared to each element in the sequence. If both parameters are
  sequences, each element of one sequence is compared to the
  corresponding element of the other sequence.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


lshift
_____________________________

Calculate lshift over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [x << param for x in sequence1]
or                      [param << x for x in sequence1]
or                      [x << y for x,y in zip(sequence1, sequence2)]
======================  ==============================================

Call formats::

  lshift(sequence1, param)
  lshift(sequence1, param, outpsequence)
  lshift(param, sequence1)
  lshift(param, sequence1, outpsequence)
  lshift(sequence1, sequence2)
  lshift(sequence1, sequence2, outpsequence)
  lshift(sequence1, param, maxlen=y)
  lshift(sequence1, param, nosimd=False)

* sequence1 - The first input data bytes or bytearray sequence to be
  examined. If no output sequence is provided the results will overwrite
  the input data.
* param - A non-sequence numeric parameter.
* sequence2 - A second input data sequence. Each element in this sequence is
  applied to the corresponding element in the first sequence.
* outpsequence - The output sequence. This parameter is optional.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled. This parameter is


lt
_____________________________

Calculate lt over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([x < param for x in sequence])
or                      all([param < x for x in sequence])
or                      all([x < y for x,y in zip(sequence1, sequence2)])
======================  ==============================================

Call formats::

  result = lt(sequence1, param)
  result = lt(param, sequence1)
  result = lt(sequence1, sequence2)
  result = lt(sequence1, param, maxlen=y)
  result = lt(sequence1, param, nosimd=False)

* sequence1 - An input bytes or bytearray to be examined.
* sequence2 - An input bytes or bytearray to be examined.
* param - A integer numeric input parameter in the range 0 - 255.
* The first and second parameters are compared to each other. If one
  parameter is a sequence and the other is an integer, the integer
  is compared to each element in the sequence. If both parameters are
  sequences, each element of one sequence is compared to the
  corresponding element of the other sequence.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


ne
_____________________________

Calculate ne over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          all([x != param for x in sequence])
or                      all([param != x for x in sequence])
or                      all([x != y for x,y in zip(sequence1, sequence2)])
======================  ==============================================

Call formats::

  result = ne(sequence1, param)
  result = ne(param, sequence1)
  result = ne(sequence1, sequence2)
  result = ne(sequence1, param, maxlen=y)
  result = ne(sequence1, param, nosimd=False)

* sequence1 - An input bytes or bytearray to be examined.
* sequence2 - An input bytes or bytearray to be examined.
* param - A integer numeric input parameter in the range 0 - 255.
* The first and second parameters are compared to each other. If one
  parameter is a sequence and the other is an integer, the integer
  is compared to each element in the sequence. If both parameters are
  sequences, each element of one sequence is compared to the
  corresponding element of the other sequence.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled if present.
  The default is False (SIMD acceleration is enabled if present).
* result - A boolean value corresponding to the result of all the
  comparison operations. If all comparison operations result in true,
  the return value will be true. If any of them result in false, the
  return value will be false.


or\_
_____________________________

Calculate or\_ over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [x | param for x in sequence1]
or                      [param | x for x in sequence1]
or                      [x | y for x,y in zip(sequence1, sequence2)]
======================  ==============================================

Call formats::

  or_(sequence1, param)
  or_(sequence1, param, outpsequence)
  or_(param, sequence1)
  or_(param, sequence1, outpsequence)
  or_(sequence1, sequence2)
  or_(sequence1, sequence2, outpsequence)
  or_(sequence1, param, maxlen=y)
  or_(sequence1, param, nosimd=False)

* sequence1 - The first input data bytes or bytearray sequence to be
  examined. If no output sequence is provided the results will overwrite
  the input data.
* param - A non-sequence numeric parameter.
* sequence2 - A second input data sequence. Each element in this sequence is
  applied to the corresponding element in the first sequence.
* outpsequence - The output sequence. This parameter is optional.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled. This parameter is


rshift
_____________________________

Calculate rshift over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [x >> param for x in sequence1]
or                      [param >> x for x in sequence1]
or                      [x >> y for x,y in zip(sequence1, sequence2)]
======================  ==============================================

Call formats::

  rshift(sequence1, param)
  rshift(sequence1, param, outpsequence)
  rshift(param, sequence1)
  rshift(param, sequence1, outpsequence)
  rshift(sequence1, sequence2)
  rshift(sequence1, sequence2, outpsequence)
  rshift(sequence1, param, maxlen=y)
  rshift(sequence1, param, nosimd=False)

* sequence1 - The first input data bytes or bytearray sequence to be
  examined. If no output sequence is provided the results will overwrite
  the input data.
* param - A non-sequence numeric parameter.
* sequence2 - A second input data sequence. Each element in this sequence is
  applied to the corresponding element in the first sequence.
* outpsequence - The output sequence. This parameter is optional.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled. This parameter is


xor
_____________________________

Calculate xor over the values in a bytes or bytearray object.

======================  ==============================================
Equivalent to:          [x ^ param for x in sequence1]
or                      [param ^ x for x in sequence1]
or                      [x ^ y for x,y in zip(sequence1, sequence2)]
======================  ==============================================

Call formats::

  xor(sequence1, param)
  xor(sequence1, param, outpsequence)
  xor(param, sequence1)
  xor(param, sequence1, outpsequence)
  xor(sequence1, sequence2)
  xor(sequence1, sequence2, outpsequence)
  xor(sequence1, param, maxlen=y)
  xor(sequence1, param, nosimd=False)

* sequence1 - The first input data bytes or bytearray sequence to be
  examined. If no output sequence is provided the results will overwrite
  the input data.
* param - A non-sequence numeric parameter.
* sequence2 - A second input data sequence. Each element in this sequence is
  applied to the corresponding element in the first sequence.
* outpsequence - The output sequence. This parameter is optional.
* maxlen - Limit the length of the sequence used. This must be a valid
  positive integer. If a zero or negative length, or a value which is
  greater than the actual length of the sequence is specified, this
  parameter is ignored.
* nosimd - If True, SIMD acceleration is disabled. This parameter is


Parameter Details
-----------------

Comparison Operators
____________________

Some functions use comparison operators. These are unicode strings containing
the Python compare operators and include following:

========= ============================
Operator   Description
========= ============================
 '<'       Less than.
 '<='      Less than or equal to.
 '>'       Greater than.
 '>='      Greater than or equal to.
 '=='      Equal to.
 '!='      Not equal to.
========= ============================

All comparison operators must contain only the above characters and may not
include any leading or trailing spaces or other characters.

Numeric Parameters
__________________

"Bytes" and "bytearray" objects are sequences of 8 bit bytes with each element
being in the range of 0 to 255. When a function accepts a non-sequence numeric
parameter, this must also be in the range of 0 to 255.


Using Less than the Entire Sequence
___________________________________

If the size of the sequence is larger than the desired length of the calculation,
it may be limited to the first part of the sequence by using the 'maxlen' 
parameter. In the following example only the first 3 elements will be operated
on, with the following ones left unchanged.::

 x = bytes([20,21,22,23,24,25])
 result = bytesfunc.bmax(x, maxlen=3)


Suppressing or Ignoring Math Errors
___________________________________

Some functions can be made to ignore some mathematical errors (e.g. integer 
overflow) by setting the 'matherrors' keyword parameter to True.::

 x = bytes([20,21,22,23,24,250,250])
 result = bytesfunc.sum(x, matherrors=True)


Ignoring errors may be desirable if the side effect (e.g. the result of an 
integer overflow) is the intended effect, or for reasons of a minor performance
improvement in some cases. Benchmark your calculation before deciding if this 
is worth while.


Differences with Native Python
______________________________

In some cases 'BytesFunc' will not produce exactly the same result as Python. 
There are several reasons for this, the primary one being that BytesFunc 
operates on different underlying data types. Specifically, BytesFunc
uses the platform's native integer types while Python integers are of 
arbitrary size and can never overflow (Python simply expands the word size 
indefinitely), while BytesFunc integers will overflow the same as they would 
with programs written in C.

Think of BytesFunc as exposing C style semantics in a form convenient to use
in Python. Some convenience which Python provides (e.g. no limit to the size of 
integers) is traded off for large performance increases.


---------------------------------------------------------------------

SIMD Support
============

General
-------

SIMD (Single Instruction Multiple Data) is a set of CPU features which allow
multiple operations to take place in parallel. Some, but not all, functions may
make use of these instructions to speed up execution. 


Disabling SIMD
--------------

Those functions which do support SIMD features will automatically make use of 
them by default unless this feature is disabled. There is normally no reason
to disable SIMD, but should there be hardware related problems the function can
be forced to fall back to conventional execution mode. 

If the optional parameter "nosimd" is set to true ("nosimd=True"), SIMD 
execution will be disabled. The default is "False". 

To repeat, there is normally no reason to wish to disable SIMD. 


Platform Support
----------------

SIMD instructions are presently supported only on 64 bit x86 (i.e. AMD64) and 
ARMv7 using the GCC compiler. Other compilers or platforms will still run the 
same functions and should produce the same results, but they will not benefit 
from SIMD acceleration. 

However, non-SIMD functions will still be much faster standard Python code. See
the performance benchmarks to see what the relative speed differences are. 


Raspberry Pi 3 versus 4
-----------------------

The Raspberry Pi uses an ARM CPU. The Raspberry Pi 3 has an ARMv7 CPU, which
supports NEON SIMD with 64 bit vectors. The Raspberry Pi 4 has an ARMv8 CPU,
which supports NEON SIMD with 128 bit vectors.

This means that the SIMD instructions for the RPi 3 are different from those
of the RPi 4 (64 bit versus 128 bit). Due to hardware availability for testing,
SIMD support for ARMv8 is not currently available in this library. 

However, the straight 'C' code should still compile and run, and still provide 
performance many times faster than when using native Python.


SIMD Function Support
---------------------

The following table shows which functions are supported by SIMD on which CPU
architectures.


=========== ===== =======
  Function   x86   ARMv7 
=========== ===== =======
 and\_        X      X  
 ball         X      X  
 bany         X      X  
 bmax         X      X  
 bmin         X      X  
 bsum                   
 eq           X      X  
 findindex    X      X  
 ge           X      X  
 gt           X      X  
 invert       X      X  
 le           X      X  
 lshift              X  
 lt           X      X  
 ne           X      X  
 or\_         X      X  
 rshift              X  
 xor          X      X  
=========== ===== =======



SIMD Support Attributes
-----------------------

There is an attribute which can be tested to detect if BytesFunc is compiled 
with SIMD support and if the current hardware supports the required SIMD level.

bytesfunc.simdsupport.hassimd

The attribute "hassimd" will be True if the module supports SIMD.

example::

	import bytesfunc
	bytesfunc.simdsupport.hassimd
	==> True


---------------------------------------------------------------------

Performance
===========

Variables affecting Performance
-------------------------------

The purpose of the BytesFunc module is to execute common operations faster than
native Python. The relative speed will depend upon a number of factors:

* The function.
* Function options. Turning checking off will result in faster performance.
* The data in the sequence and the parameters. 
* The size of the sequence.
* The platform, including CPU type (e.g. x86 or ARM), operating system, 
  and compiler.

The speeds listed below should be used as rough guidelines only. More exact
results will require application specific testing. The numbers shown are the
execution time of each function relative to native Python. For example, a value 
of '50' means that the corresponding BytesFunc operation ran 50 times faster 
than the closest native Python equivalent. 

Both relative performance (the speed-up as compared to Python) and absolute
performance (the actual execution speed of Python and BytesFunc) will vary
significantly depending upon the compiler (which is OS platform dependent) and 
whether compiled to 32 or 64 bit. If your precise actual benchmark performance 
results matter, be sure to conduct your testing using the actual OS and compiler 
your final program will be deployed on. The values listed below were measured on 
x86-64 Linux compiled with GCC. 


Note: Some more complex BytesFunc functions do not work exactly the same way as 
the native Python equivalents. This means that the benchmark results should be 
taken as general guidelines rather than precise comparisons. 


Typical Performance Readings
----------------------------

In this set of tests, all error checking was turned on and SIMD 
acceleration was enabled where this did not conflict with the preceding
(the defaults in each case). 

The Bytesfunc versus Python factor of 100.0 means the bytesfunc version ran
100 times faster than in native Python on that platform. Benchmarks for 
different hardware and platforms cannot be compared via this benchmark in terms
of absolute performance as these are relative, not absolute numbers. 

An SIMD versus non-SIMD factor of 10.0 means the SIMD version was 10 times 
faster than the non-SIMD version. An SIMD versus non-SIMD factor of 0.0 means
the function did not support SIMD on the tested platform. 


x86-64 Benchmarks
_________________

The following tests were conducted on an x86-64 CPU.

Relative Performance - Python Time / Bytesfunc Time.

============ ===================== ======================================
  function    Bytesfunc vs Python   SIMD vs non-SIMD
============ ===================== ======================================
 bmax                   79.6                   4.2
 bmin                   79.5                   4.2
 bsum                    7.4                   0.0
 ball                  619.4                  15.2
 bany                  477.0                  11.8
 findindex             680.7                  10.9
 eq                    668.1                  12.2
 ge                    671.2                  11.3
 gt                    794.8                   8.7
 le                    630.9                  11.1
 lt                    492.2                   7.5
 ne                    801.0                  11.9
 and\_                1511.2                   8.7
 or\_                 1119.4                   9.9
 xor                  1001.7                  10.1
 lshift                131.1                   0.0
 rshift                 97.6                   0.0
 invert                987.6                   8.7
============ ===================== ======================================

=========== ========
Stat         Value
=========== ========
Average:    602.8
Maximum:    1511.2
Minimum:    7.4
Array size: 100000
=========== ========






ARMv7 Benchmarks
_________________

The following tests were conducted on an ARMv7 CPU on a Raspberry Pi 3.

Relative Performance - Python Time / Bytesfunc Time.

============ ==================== ======================================
  function    Bytefunc vs Python   SIMD vs non-SIMD
============ ==================== ======================================
 bmax                  222.6                   4.4
 bmin                  225.5                   4.4
 bsum                   10.3                   0.0
 ball                  343.1                   2.6
 bany                  391.4                   2.9
 findindex             523.8                   3.6
 eq                    344.2                   2.6
 ge                    358.7                   2.6
 gt                    358.8                   2.6
 le                    359.8                   2.6
 lt                    359.9                   2.6
 ne                    390.6                   2.9
 and\_                1040.1                   3.8
 or\_                 1072.1                   3.8
 xor                  1066.3                   3.8
 lshift               1289.6                   4.5
 rshift                933.1                   4.4
 invert                846.2                   3.8
============ ==================== ======================================

=========== ========
Stat         Value
=========== ========
Average:    563.1
Maximum:    1289.6
Minimum:    10.3
Array size: 100000
=========== ========






Platform Effects
----------------

The platform, including CPU, OS, compiler, and compiler version can 
affect performance, and this influence can change significantly for 
different functions. 

If your application requires exact performance data, then benchmark
your application in the specific platform (hardware, OS, and compiler) 
that you will be using.


---------------------------------------------------------------------

Platform support
================

List of tested Operation Systems, Compilers, and CPU Architectures
------------------------------------------------------------------

BytesFunc is written in 'C' and uses the standard C libraries to implement the 
underlying math functions. BytesFunc has been tested on the following platforms.

================= ========  ========================== =========================
OS                   Bits      Compiler                  Python Version Tested
================= ========  ========================== =========================
Ubuntu 18.04 LTS   64 bit    GCC                         3.6
Ubuntu 19.10       64 bit    GCC                         3.7
Ubuntu 20.04 beta  64 bit    GCC                         3.8
Debian 10          32 bit    GCC                         3.7
Debian 10          64 bit    GCC                         3.7
OpenSuse 15        64 bit    GCC                         3.6
Centos 8           64 bit    GCC                         3.6
FreeBSD 12         64 bit    LLVM                        3.7
OpenBSD 6.5        64 bit    LLVM                        3.6
MS Windows 10      64 bit    MS Visual Studio C 2015     3.8
Raspbian (RPi 3)   32 bit    GCC                         3.7
================= ========  ========================== =========================

The Raspbian (RPi 3) tests were conducted on a Raspberry Pi 3 ARMV7 CPU. All 
others were conducted using VMs running on x86 hardware. 


Platform Oddities
-----------------

As most operators are implemented using native behaviour, details of some 
operations may depend on the CPU architecture.

Lshift and rshift will exhibit a behaviour that depends on the CPU type 
whether it is 32 or 64 bit, and array size. 

For 32 bit x86 systems, if the array word size is 32 bits or less, the shift 
is masked to 5 bits. That is, shift amounts greater than 32 will "roll over",
repeating smaller shifts.

On 64 bit systems, this behaviour will vary depending on whether SIMD is used
or not. Arrays which are not even multiples of SIMD register sizes may
exibit different behaviour at different array indexes (depending on whether 
SIMD or non-SIMD instructions were used for those parts of the array).

ARM does not display this roll-over behaviour, and so may give different
results than x86. However, negative shift values may result in the shift
operation being conducted in the opposite direction (e.g. right shift instead
of left shift).

The conclusion is that bit shift operations which use a shift amount which is
not in the range of 0 to "maximum number" may produce undefined results.
So valid bit shift amounts should be 0 to 7.

