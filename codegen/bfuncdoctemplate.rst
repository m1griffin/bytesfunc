=========
BytesFunc
=========

:Authors:
    Michael Griffin
    

:Version: 3.1.2 for 2022-04-10
:Copyright: 2014 - 2022
:License: This document may be distributed under the Apache License V2.0.
:Language: Python 3.6 or later


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

{summarytable}



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

{opdocs}


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

SIMD instructions are presently supported only on the following:

* 64 bit x86 (i.e. AMD64) using GCC.
* 32 bit ARMv7 using GCC (tested on Raspberry Pi 3).
* 64 bit ARMv8 AARCH64 using GCC (tested on Raspberry Pi 4).

Other compilers or platforms will still run the same functions and should 
produce the same results, but they will not benefit from SIMD acceleration. 

However, non-SIMD functions will still be much faster standard Python code. See
the performance benchmarks to see what the relative speed differences are. With
wider data types (e.g. double precision floating point) SIMD provides only
marginal speed ups anyway. 


Raspberry Pi 32 versus 64 bit
-----------------------------

The Raspberry Pi uses an ARM CPU. This can operate in 32 or 64 bit mode. When
in 32 bit mode, the Raspberry Pi 3 operates in ARMv7 mode. This has 64 bit ARM
NEON SIMD vectors.

When in 64 bit mode, it acts as an ARMv8, with AARCH64 128 bit ARM NEON SIMD
vectors.

The Raspbian Linux OS is 32 bit mode only. Other distros such as Ubuntu offer
64 bit versions. 

The "setup.py" file uses platform detection code to determine which ARM CPU
and mode it is running on. Due to the availability of hardware for testing,
this code is tailored to the Raspberry Pi 3 and Raspberry Pi 4 and the 
operating systems listed. This code then selects the appropriate compiler 
arguments to pass to the setup routines to tell the compiler what mode to 
compile for.

If other ARM platforms are used which have different platform signatures or
which require different compiler arguments, the "setup.py" file may need to be
modified in order to use SIMD acceleration.

However, the straight 'C' code should still compile and run, and still provide 
performance many times faster than when using native Python.



SIMD Function Support
---------------------

The following table shows which functions are supported by SIMD on which CPU
architectures.

{simdtable}



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

{pybench_x86}


ARMv7 Benchmarks
_________________

The following tests were conducted on an ARM CPU in 32 bit mode (ARMv7) on a 
Raspberry Pi 3.

{pybench_ARMv7}


ARMv8 Benchmarks
_________________

The following tests were conducted on an ARM CPU in 64 bit mode (ARMv8) on a 
Raspberry Pi 4.

{pybench_ARMv8}


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

======================= ========== ====== =============== ================
OS                       Hardware   Bits   Compiler        Python Version
======================= ========== ====== =============== ================
Ubuntu 20.04 LTS         x86_64     64     GCC               3.8
Ubuntu 21.10             x86_64     64     GCC               3.9
Debian 11                i686       32     GCC               3.9
Debian 11                x86_64     64     GCC               3.9
OpenSuse 15.3            x86_64     64     GCC               3.6
Alma 8.5                 x86_64     64     GCC               3.6
FreeBSD 13               x86_64     64     LLVM              3.8
OpenBSD 7.0              x86_64     64     LLVM              3.8
MS Windows 10            x86_64     64     MS VS C v.1929    3.10
MS Windows 11            x86_64     64     MS VS C v.1929    3.10
Raspberry Pi 2022-04-04  RPi 3      32     GCC               3.9
Ubuntu 20.04             RPi 4      64     GCC               3.8
======================= ========== ====== =============== ================

* The Rasberry Pi 3 tests were conducted on a Raspberry Pi 3 ARM CPU running
  in 32 bit mode. 
* The Ubuntu ARM tests were conducted on a Raspberry Pi 4 ARM CPU running in
  64 bit mode.
* All others were conducted using VMs running on x86 hardware. 


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

