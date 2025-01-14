#!/bin/bash

# This script will do a simple user setup of bytesfunc from source. 
# Call pip directly with the appropriate options if you wish to have a
# different type of install.

# ======================================================================

fcompileresults="bf_compileresults.txt"
fcompileerrors="bf_compileerrors.txt"
pkgname="bytesfunc"

# ======================================================================

# Check if an appropriately named package is present.
if [ ! -f $pkgname*.tar.gz ]; then
	echo "Found $pkgname source package."
else
	echo "Could not find $pkgname source package."
	echo "Exiting ..."
	exit 1
fi


# ======================================================================

echo "Running $pkgname build as a local install using pip."

echo "Compiler messages are redirected to $fcompileresults."


# ======================================================================

# Insert the date in the error files.
echo `date '+%Y-%m-%d %H:%M:%S'` > $fcompileresults

echo `date '+%Y-%m-%d %H:%M:%S'` > $fcompileerrors

# ======================================================================

# Over-ride the PEP-668 externally managed option in "pip" so we can test
# without setting up a virtual environment.
# This was introduced for Ubuntu 23.04. 
export PIP_BREAK_SYSTEM_PACKAGES=1

# ======================================================================

# ======================================================================

# Find out if running on BSD. FreeBSD and OpenBSD use "pip" instead of "pip3".
# Linux uses "pip3". uname for FreeBSD and OpenBSD is their names as written here.
# Since we have to run on BSD, we can't use Bash built-ins for string comparions
# and so have to do it the hard way.
platform=$( uname )
echo "OS platform $platform detected."
echo "Installing using pip ..."
if echo "$platform" | grep -q "BSD"; then
	pip install --user --force-reinstall ./$pkgname 1>> $fcompileresults 2>> $fcompileerrors
else
	pip3 install --user --force-reinstall ./$pkgname 1>> $fcompileresults 2>> $fcompileerrors
fi

# ======================================================================

# Check for reported errors.
haserror=$( grep "finished with status 'error'" $fcompileresults | wc -l )
if [ "$haserror" -gt "0" ]; then
	echo "Compile errors were detected."
fi

# Check for reported success.
wassucess=$( grep "Successfully installed $pkgname" $fcompileresults | wc -l )
if [ "$wassucess" -gt "0" ]; then
	echo "Package successfully installed."
fi


# Check for warnings or errors.
wascomperr=$( cat $fcompileerrors | wc -l )
if [ "$wascomperr" -gt "1" ]; then
	echo "Check $fcompileerrors for warnings or errors."
fi

# Append the compile errors to the compile results file.
echo >> $fcompileresults
cat $fcompileerrors >> $fcompileresults

echo "Setup complete. Check $fcompileresults for errors."

