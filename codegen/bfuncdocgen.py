#!/usr/bin/env python3
##############################################################################
# Project:  bytesfunc
# Purpose:  Generate the documentation for the bytesfunc functions.
# Language: Python 3.4
# Date:     08-Feb-2020
#
###############################################################################
#
#   Copyright 2018 - 2020    Michael Griffin    <m12.griffin@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
##############################################################################


# ==============================================================================

import glob
import os
import itertools


# ==============================================================================

# ==============================================================================

def GetCSourceFiles(filepath):
	'''Get the list of C source files.
	'''
	# The list of files actually present.
	filelist=glob.glob(filepath)
	filelist.sort()
	return filelist


# ==============================================================================

# Read the C function names from the source files.
def GetFuncNames(filepath):
	"""Get the names of the functions. This works by reading the C source 
		code file names and looking for the string 'PyDoc_STRVAR', which
		is the indicator that this is a file which has a documentation
		string. 
	Returns: (list) a list of function names.
	"""
	# Get a list of all of the 'C' files.
	filelist = glob.glob(filepath)
	filelist.sort()

	filedata = []


	for fname in filelist:
		with open(fname, 'r') as f:
			# Search to see if the desired string is in the file.
			if 'PyDoc_STRVAR' in f.read():
				# Split the file name from the rest of the path, and then
				# split the file prefix from the file extension ('.c') to
				# get the function name.
				funcname = os.path.split(os.path.basename(fname))[1].split('.')[0]
				# We exclude 'simdsupport', as we document it separately.
				if funcname != 'simdsupport':
					filedata.append(funcname)

	return filedata

# ==============================================================================

def sanitizer(x):
	'''Sanitizier function. This escapes trailing underscore characters
	for the sake of ReST format where this is a formatting character.
	'''
	# Don't change anything if it is in the form of the function call.
	if ('and_(' in x) or ('or_(' in x):
		return x

	if 'and_' in x:
		return x.replace('and_', 'and\_')
	elif 'or_' in x:
		return x.replace('or_', 'or\_')
	else:
		return x

def FindFuncDocs(filelist, funcnames, filepath):
	'''Get the function documentation directly from the C source code. 
	The list of functions is based on the function configuraiton spreadsheet.
	Parameters:
		filelist (list) = A list of the C file names present.
		funcnames (list) = A list of the function names.
		filepath (string) = The path to th files.
	'''
	funcsdocs = {}

	# Get the documentation directly from the C source file.
	for func in funcnames:
		with open(filepath + func + '.c') as f:
			funcdata = f.readlines()
			# The documentation starts with PyDoc_STRVAR and ends with the closing function bracket.
			docdata = itertools.takewhile(lambda x: '");' not in x, itertools.dropwhile(lambda x: 'PyDoc_STRVAR' not in x, funcdata))
			# Sanitize the data by removing the C language string literal control characters, plus end of line blanks.
			docdatastripped = [x.replace('\\n\\', '').rstrip() for x in list(docdata)[1:]]
			# Sanitize some more. There will be a quote character which will be at the start of the function.
			docdatastripped[0] = docdatastripped[0].replace('"', '')
			# Some function names need the trailing '_' character escaped as this is a
			# formatting character for ReST documents.
			docsantizied = [sanitizer(x) for x in docdatastripped]
			# Add some formatting to the display of call formats. To do this we need to
			# add another colon character.
			callformats = [x.replace('Call formats:', 'Call formats::') for x in docsantizied]
				
		funcsdocs[func] = ['\n\n',] + callformats

	return funcsdocs

# ==============================================================================

# Format the function documentation.
def FormatFuncsDocs(funcsdocs):
	'''Format the function documentation.
	'''
	funcnames = list(funcsdocs.keys())
	funcnames.sort()

	docs = ['\n'.join(funcsdocs[x]) for x in funcnames]

	return ''.join(docs)

# ==============================================================================


# Read the C function names from the source files.
def GetSourceFileSIMD(filepath, simdname):
	"""Get the names of functions which have SIMD acceleration. This
		works by reading the C source code file names and looking for
		the corresponding SIMD functions. This assumes that the 
		function name follows a specific convention.
		Since there is only one data type we don't have to worry about
		which data types are supported.
		It also searches to see which platforms (CPU types) are 
		supported, again by making assumptions about the function name.
		The C source code files must be in a specific position relative
		to this script.
	Parameters: filepath (string): Get the path defining the source files.
		simdname (string): The string pattern to match to find the
			functions with SIMD support.
		Returns: (list) a list of function names with SIMD support.
	"""
	# Get a list of the SIMD related header files.
	filelist = glob.glob(filepath)
	filelist.sort()

	filedata = []


	for fname in filelist:
		with open(fname, 'r') as f:
			# Search to see if the desired SIMD function is in the file.
			if simdname in f.read():
				# Split the file name from the rest of the path, and then
				# split the file prefix from the file extension ('.c') to
				# get the function name.
				funcname = os.path.split(os.path.basename(fname))[1].split('.')[0]
				filedata.append(funcname)

	return filedata



# ==============================================================================

def MakeSummaryTable(funcsdocs):
	'''Extract the function documentation and order them in the correct
	categories in the form of a one line summary based on the equivalent
	Python operation.
	Parameters: funcsdocs = The function documentation.
	Returns: The function summary as a block of text.
	'''
	funcnames = list(funcsdocs.keys())
	funcnames.sort()
	functitlesize = max([len(x) for x in funcnames])
	functitlepad = max(functitlesize, len('Function')) + 2

	summdocs = []
	tablesep = '=' * functitlepad + ' ' + '=' * 50

	tablehead = tablesep + '\n' + 'Function'.center(functitlepad) + '      Equivalent to' + '\n' + tablesep

	summdocs.append('\n' + tablehead)


	# Gather all the documentation.
	for func in funcnames:
		# Extract just the equivalent operation. 
		equiv = ''.join([x for x in funcsdocs[func] if 'Equivalent to' in x])
		equivtext = equiv.partition(':')[2].lstrip().rstrip()

		# Escape the function name in the event it contains underscores.
		# This is required for RST when converting to PDF or HTML. 
		funcrst = sanitizer(func)
		# Format the line.
		summdocs.append(funcrst.rjust(functitlepad) + ' ' + equivtext)

	summdocs.append(tablesep)


	return '\n'.join(summdocs)


# ==============================================================================

def MakeSIMDTable(funcsdocs, x86, armv7):
	'''Make a table showing which functions have SIMD support, and for which architecture.
	'''
	funcnames = list(funcsdocs.keys())
	funcnames.sort()
	functitlesize = max([len(x) for x in funcnames])
	functitlepad = max(functitlesize, len('Function')) + 2

	summdocs = []
	tablesep = '=' * functitlepad + ' ===== ======='

	tablehead = tablesep + '\n' + 'Function'.center(functitlepad) + '  x86   ARMv7 \n' + tablesep
	summdocs.append('\n' + tablehead)

	flinetemplate = '   %s     %s    %s '
	for func in funcnames:
		hasx86 = '  X   ' if func in x86 else '      '
		hasarmv7 = '   X  ' if func in armv7 else '      '

		# Escape the function name in the event it contains underscores.
		# This is required for RST when converting to PDF or HTML. 
		funcrst = sanitizer(func)
		summdocs.append(' ' + funcrst.ljust(functitlepad) + hasx86 + hasarmv7)
		#summdocs.append(' %s               %s    %s \n' % (funcrst, hasx86, hasarmv7))

	summdocs.append(tablesep)

	return '\n'.join(summdocs)


# ==============================================================================

# Create the data.

filepath = '../src/*.c'
filedirpath = '../src/'

# The list of C source files.
filelist = GetCSourceFiles(filepath)
# Get just the function names from the C source files.
funcnames = GetFuncNames(filepath)
# Extract the function documentation from the C source files.
funcsdocs = FindFuncDocs(filelist, funcnames, filedirpath)

# Find all the functions with x86 SIMD support.
SIMD_data_x86 = GetSourceFileSIMD(filepath, '_x86_simd')
# Find all the functions with ARMv7 SIMD support.
SIMD_data_arm = GetSourceFileSIMD(filepath, '_armv7_simd')


# Format the main function documentation.
opdocs = FormatFuncsDocs(funcsdocs)

# Format the function summary table.
summtable = MakeSummaryTable(funcsdocs)

simdtable = MakeSIMDTable(funcsdocs, SIMD_data_x86, SIMD_data_arm)

# ==============================================================================

# Import the benchmark data.

def GetBenchmarkData(benchfile):
	'''Read the benchmark data and extract the benchmarks.
	'''
	# These are the benchmark table headings. These are used to find
	# the start and stop of the benchmark table.
	pytitle = 'Relative Performance - Python Time / Bytesfunc Time'
	pyabsolute = 'Time per test iteration in microseconds'

	with open(benchfile) as f:
		benchdata = f.readlines()

	# Get the first table.
	pybench = ''.join(itertools.takewhile(lambda x: pyabsolute not in x, itertools.dropwhile(lambda x: pytitle not in x, benchdata)))

	return pybench


pybench_x86 = GetBenchmarkData('../benchmarks/bf_benchmarkdata.txt')

pybench_ARMv7 = GetBenchmarkData('../benchmarks/RPi332_bf_benchmarkdata.txt')

pybench_ARMv8 = GetBenchmarkData('../benchmarks/RPi364_bf_benchmarkdata.txt')

# ==============================================================================

# Insert the data into the documentation template.
def WriteDocs(summtable, opdocs, simdtable, pybench_x86, pybench_ARMv7, pybench_ARMv8):
	'''Write out the documentation based on the template.
	'''
	# Read in the entire template file.
	with open('bfuncdoctemplate.rst', 'r') as f:
		doctmpl = f.read()

	# Write out the completed documentation file complete with data.
	with open('BytesFunc.rst', 'w') as f:
		f.write(doctmpl.format(summarytable = summtable, opdocs = opdocs, 
			simdtable = simdtable, 
			pybench_x86 = pybench_x86,
			pybench_ARMv7 = pybench_ARMv7,
			pybench_ARMv8 = pybench_ARMv8,
			))

# Write out the documentation file.
WriteDocs(summtable, opdocs, simdtable, pybench_x86, pybench_ARMv7, pybench_ARMv8)

# ==============================================================================
