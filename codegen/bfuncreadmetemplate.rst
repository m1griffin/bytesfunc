=========
BytesFunc
=========

:Authors:
    Michael Griffin

:Version:  {versionnumber} for {versiondate}
:Copyright: 2014 - {copyrightyear}
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

{bfuncdoc_ossupportdata}

* The Rasberry Pi 3 tests were conducted on a Raspberry Pi 3 ARM CPU running
  in 32 bit mode. 
* The Ubuntu ARM tests were conducted on a Raspberry Pi 4 ARM CPU running in
  64 bit mode.
* The Rasberry Pi 5 tests were conducted on a Raspberry Pi 5 ARM CPU running
  in 64 bit mode. 
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


Installing on Linux with PIP and PEP-668
----------------------------------------
PEP-668 (PEPs describe changes to Python) introduced a new feature which can
affect how packages are installed with PIP. If PIP is configured to be 
EXTERNALLY-MANAGED it will refuse to install a package outside of a virtual
environment.

The intention of this is to prevent conflicts between packages which are 
installed using the system package manager, and ones which are installed using
PIP.

Linux distros which are affeced by this include the latest versions of Debian
and Ubuntu.

As this package is a library which is intended to be used by other 
applications, there is no one right way to install it, whether inside or 
outside of a virtual environment. Review the options available with PIP to see
what is suitable for your application.

For testing purposes this package was installed by setting the environment
variable PIP_BREAK_SYSTEM_PACKAGES to "1", which effectively disables this
feature in PIP. 

example::

	export PIP_BREAK_SYSTEM_PACKAGES=1


---------------------------------------------------------------------

Release History
===============
{release_history}
