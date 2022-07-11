=========
BytesFunc
=========

:Authors:
    Michael Griffin

:Version: 3.3.0 for 2022-07-11
:Copyright: 2014 - 2022
:License: This document may be distributed under the Apache 2.0 License.
:Language: Python 3.6 or later

---------------------------------------------------------------------

Introduction
============

The BytesFunc module provides high speed array processing functions for use with
Python 'bytes' and 'bytearray' objects. These functions are patterned after the
functions in the standard Python "operator" module together with some additional 
ones from other sources.

The purpose of these functions is to perform mathematical calculations on 
"bytes" and "bytearray" objects significantly faster than using native Python.

See full documentation at: https://bytesfunc.readthedocs.io/en/latest/

If you are installing on an ARM platform such as the Raspberry Pi, see the
installation notes at the end before attempting to install from PyPI using PIP.

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

======================= ========== ====== =============== ================
OS                       Hardware   Bits   Compiler        Python Version
======================= ========== ====== =============== ================
Ubuntu 20.04 LTS         x86_64     64     GCC               3.8
Ubuntu 22.04             x86_64     64     GCC               3.10
Debian 11                i686       32     GCC               3.9
Debian 11                x86_64     64     GCC               3.9
OpenSuse 15.3            x86_64     64     GCC               3.6
Alma 9                   x86_64     64     GCC               3.9
Alpine 3.16.0            i686       32     GCC               3.10
FreeBSD 13               x86_64     64     LLVM              3.8
OpenBSD 7.1              x86_64     64     LLVM              3.9
MS Windows 10            x86_64     64     MS VS C v.1929    3.10
MS Windows 11            x86_64     64     MS VS C v.1929    3.10
Raspberry Pi 2022-04-04  RPi 3      32     GCC               3.9
Ubuntu 22.04             RPi 4      64     GCC               3.10
======================= ========== ====== =============== ================

* The Rasberry Pi 3 tests were conducted on a Raspberry Pi 3 ARM CPU running
  in 32 bit mode. 
* The Ubuntu ARM tests were conducted on a Raspberry Pi 4 ARM CPU running in
  64 bit mode.
* All others were conducted using VMs running on x86 hardware. 

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
	pip3 install bytesfunc
	# Force install from PyPI source instead of using a binary wheel.
	pip3 install --user --force-reinstall --no-binary=:all: bytesfunc
	# Install from a local copy of the source package (Linux).
	pip3 install --no-index --find-links=. bytesfunc
	# Install a local package as a user package.
	pip3 install --user --no-index --find-links=. bytesfunc
	# Windows, FreeBSD, and OpenBSD seems to use "pip" instead 
	# of "pip3" for some reason.
	pip install bytesfunc


Newer versions of OpenBSD and FreeBSD will not install this package correctly 
when running setup.py directly. Use pip to install, even for local package
installs. Testing of this package has been changed to use only pip (or pip3)
in order to provide a common testing method for all platforms. Testing using
setup.py directly is no longer done.


Recent versions of PyPI seem to be building their own binary wheels for some 
platforms using their own infrastruction. This may result in an invalid ARM 
binary on Raspberry Pi. 

If you have difficulties, then either download the tar.gz version and install 
it locally (see the above instructions for a local install). Alternatively,
see the above example for how to force a binary install instead of using a 
wheel. There is also a bash script called "setupuser.sh" which will call setup.
py directly with the appropriate parameters. 

The setup.py file has platform detection code which it uses to pass the 
correct flags to the C compiler. For ARM, this includes the CPU type. If you
are using an ARM CPU type which is not recognized then setup.py may not
compile in SIMD features. You can experiment with modifying setup.py to add
new ARM models, but be sure that anything you try is compatible with the 
existing ones.

---------------------------------------------------------------------

Release History
===============
* 3.3.0 - Major performance improvements for bsum through the use of SIMD and
          other optimizations. Used splint (GCC lint) on all C code and fixed
          warnings. Other than bsum, no changes in functionality.
* 3.2.1 - Fixed formatting error in README.rst. 
* 3.2.0 - Update to testing and support. Tested with new releases of Ubuntu 
          22.04 and OpenBSD 7.1. Changed "simdsupport" to also report the 
          architecture the binary was compiled for. "Simdsupport" is only
          used for testing and benchmarking and is not a stable part of
          the release.
* 3.1.2 - Bump to correct minor documentation error in README.rst. 
* 3.1.1 - Update to testing and support. Raspberry Pi 32 bit OS updated to
          version 2022-04-04. Update to setup.py to improve ARM version 
          detection.
* 3.1.0 - Update to testing and support. On Windows 10 the Python version is
          3.10. Centos has been replaced by AlmaLinux due to Red Hat ending 
          long term support for Centos. Ubuntu Server 21.04 replaced by 21.10.
          No actual code changes.
* 3.0.0 - Major speed improvement to lshfit and rshift on x86-64 due to adding
          SIMD support. Debian test platforms were updated to latest versions 
          (11). 
* 2.2.0 - Updated benchmarks to make each one a separate file. Centos and
          OpenSuse test platforms updated to latest versions.
* 2.1.1 - Documentation updated and version number bumped to reflect testing 
          with Ubuntu 21.04, FreeBSD 13.0, and OpenBSD 6.9. No code changes.
* 2.1.0 - Changed setup.py to detect Raspberry Pi 4 and set the compiler args
          accordingly. Added support for Pi 4. Dropped testing of 64 bit 
          mode on Pi 3. 
* 2.0.1 - Documentation updated to reflect testing with the release version
          of Ubuntu 20.04 ARM (Rasberry Pi), Ubuntu 2010 (x86-64), OpenBSD 6.8,
          and Python 3.9 on Windows. No code changes and no change in version 
          number.
* 2.0.0 - Documentation updated to reflect testing with the release version
          of Ubuntu 20.04. No code changes and no change in version number.
* 2.0.0 - Added SIMD support for ARMv8 AARCH64. This is 64 bit ARM on a
          Raspberry Pi3 when running 64 bit Ubuntu. Raspbian is 32 bit only
          and has 64 bit SIMD vectors. 64 bit ARM has 128 bit SIMD vectors
          and so offers improved performance.
* 1.0.0 - First release.
