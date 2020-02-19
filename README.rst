=========
BytesFunc
=========

:Authors:
    Michael Griffin

:Version: 1.0.0 for 2020-02-19
:Copyright: 2014 - 2020
:License: This document may be distributed under the Apache 2.0 License.
:Language: Python 3.5 or later

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

Supported Sequence Types
========================

BytesFunc supports Python native "bytes" and "bytearray" objects.


---------------------------------------------------------------------

Performance
===========

Average performance increase on x86_64 Ubuntu with GCC is 600 times faster 
than native Python. Performance will vary depending on the function,  
with the performance increase ranging from 7 times to 1500 times. 

Other platforms show similar improvements.

Detailed performance figures are listed in the full documentation.


---------------------------------------------------------------------

Platform support
================

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

The Raspbian (RPi 3) tests were conducted on a Raspberry Pi ARM CPU. All others
were conducted using VMs running on x86 hardware. 


---------------------------------------------------------------------

Installation
============

Please note that this is a Python 3 package. To install using Pip, you will 
need (with Debian package in brackets):

* The appropriate C compiler and header files (gcc and build-essential).
* The Python3 development headers (python3-dev).
* Pip3 together with the corresponding Setuptools (python3-pip).

example::

	# Install from PyPI.
	pip3 install arrayfunc
	# Install from a local copy of the source package (Linux).
	pip3 install --no-index --find-links=. arrayfunc
	# Windows seems to use "pip" instead of "pip3" for some reason.
	pip install arrayfunc


---------------------------------------------------------------------

Release History
===============

* 1.0.0 - First release.
