#!/usr/bin/env python3

# Setup file for bytesfunc. As part of the setup process this script will
# attempt to detect if the current system is x86-64 or ARMv7 with GCC,
# and if so will enable SIMD extensions. If the current system is any 
# other architecture or compiler they will be disabled.


import platform
from setuptools import setup, Extension


# This is a list of the files and all the dependencies.
extensions = [
	('eq', ['src/eq.c', 'src/bytesparams_comp.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('ge', ['src/ge.c', 'src/bytesparams_comp.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('gt', ['src/gt.c', 'src/bytesparams_comp.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('le', ['src/le.c', 'src/bytesparams_comp.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('lt', ['src/lt.c', 'src/bytesparams_comp.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('ne', ['src/ne.c', 'src/bytesparams_comp.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),

	('bmax', ['src/bmax.c', 'src/bytesparams_valoutsimd.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('bmin', ['src/bmin.c', 'src/bytesparams_valoutsimd.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('bsum', ['src/bsum.c', 'src/bytesparams_bsum.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),

	('ball', ['src/ball.c', 'src/bytesparams_allany.c', 'src/bytesparams_base.c', 'src/arrayops.c', 'src/byteserrs.c']),
	('bany', ['src/bany.c', 'src/bytesparams_allany.c', 'src/bytesparams_base.c', 'src/arrayops.c', 'src/byteserrs.c']),
	('findindex', ['src/findindex.c', 'src/bytesparams_allany.c', 'src/bytesparams_base.c', 'src/arrayops.c', 'src/byteserrs.c']),

	('and_', ['src/and_.c', 'src/bytesparams_two.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('or_', ['src/or_.c', 'src/bytesparams_two.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('xor', ['src/xor.c', 'src/bytesparams_two.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('lshift', ['src/lshift.c', 'src/bytesparams_two.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),
	('rshift', ['src/rshift.c', 'src/bytesparams_two.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),

	('invert', ['src/invert.c', 'src/bytesparams_invert.c', 'src/bytesparams_base.c', 'src/byteserrs.c']),

	('simdsupport', ['src/simdsupport.c']),

]


# Used for Raspberry Pi CPU version detection. 
def GetRaspCPUType():
	'''Use only for Raspberry Pi CPU detection. 
	This makes the following assumptions.
	 - it is running on an ARM CPU.
	 - it is running on 64 bit Linux.
	 - it can read '/proc/cpuinfo' to get the CPU part data.

	If found, it will return the CPU part string. If not, then it will
	return an empty string.
	e.g. 'CPU part: 0xd08'
	'''

	# These reads the CPU Info directly from the Linux kernel.
	# This seems to be the only way to access detailed information
	# about the CPU type. 
	with open('/proc/cpuinfo') as cpuf:
		cpuinfo = cpuf.read()

	# Now check that this is a Raspberry Pi. We don't know what to look
	# for with other ARM boards, so we don't try to handle them.
	if "Raspberry Pi" in cpuinfo:
		# Find the infor for the CPU part type. This is repeated once for
		# each core, so we also remove duplicates.
		cpupartsall = list(set([x for x in cpuinfo.split('\n') if "CPU part" in x]))

		# If we found any, then get the info from the first core. If they
		# are all the same there will only be one record anyway. We should
		# end up with something that looks like 'CPU part: 0xd08'.
		if len(cpupartsall) > 0:
			cpupart = cpupartsall[0]
			return cpupart

	return ''



# Detect the compiler used for Python. We will assume that this same compiler is
# being used to compile our own modules (since the two are supposed to match).
# We are looking specifically for GCC.
# The names used by MSVC for the SIMD instructions are not compatible with
# other compilers. LLVM Clang does not have full compiler intrinsics SIMD 
# support yet. Hence, we can only use SIMD with GCC at this time. We suppress
# the command line option for unsupported compilers to avoid compiler warnings.
# GCC is expected to return a string which looks something like the 
# following: 'GCC 5.4.0 20160609'
# LLVM Clang returned something like: 'GCC 4.2.1 Compatible Clang <etc.>'
# MSVC Returns something like 'MSC <version> <chip architecture>'
# Because LLVM Clang masquerades as GCC, we must take extra effort to ensure that
# we're actually dealing with GCC. If this changes in future, we can change the 
# following to enable the option. There are however also #define statements in
# the C source which must also be changed.
# First however, we must check to make sure this is an x86 CPU, otherwise the
# SIMD flags are completely different.
PyCompilerType = platform.python_compiler()
if ('x86' in platform.machine()) and ('GCC' in PyCompilerType) and ('Clang' not in PyCompilerType):
	Compile_Args = ['-msse4.1']
# For ARMv7 32 bit. 
elif ('GCC' in PyCompilerType) and ('armv7l' in platform.machine()):
	Compile_Args = ['-mcpu=cortex-a7', '-mfpu=neon-vfpv4']
# For ARM AARCH 64 bit. 
elif ('GCC' in PyCompilerType) and ('aarch64' in platform.machine()):
	# Get the CPU part string from the kernel.
	cpupart = GetRaspCPUType()
	# For Raspberry Pi 3 in 64 bit mode.
	if '0xD03' in cpupart.upper():
		Compile_Args = ['-mcpu=cortex-a53']
	# For Raspberry Pi 4 in 64 bit mode.
	elif '0xD08' in cpupart.upper():
		Compile_Args = ['cortex-a72']
	else:
		Compile_Args = []
else:
	Compile_Args = []


with open('README.rst') as longdescdata:
    long_description = longdescdata.read()


setup(name = 'bytesfunc', 
	version = '3.1.0',
	description = 'Fast bytes and bytearray processing functions',
	long_description = long_description,
	url = 'https://github.com/m1griffin/bytesfunc',
	author = 'M Griffin',
	author_email = 'm12.griffin@gmail.com',
	license = 'Apache License V2.0',
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Scientific/Engineering :: Mathematics',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 3.6',
		],
	keywords = 'bytes and bytearray functions',
	ext_package='bytesfunc',
	ext_modules = [Extension(x, y, extra_compile_args=Compile_Args) for x,y in extensions],
	packages=['bytesfunc']
	)

