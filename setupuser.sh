#!/bin/sh
# This script will do a simple user local setup of bytesfunc. 
# Call setup.py directly with the appropriate options if you wish to have a
# different type of install.

echo Running BytesFunc build as a local install. 
echo Compiler messages are redirected to bf_compile_results.txt

echo `date` > bf_compile_results.txt
echo `date` > bf_compile_errors.txt
python3 -m build  1>> bf_compile_results.txt 2>> bf_compile_errors.txt

compcount=$( grep "$adding 'bytesfunc.*so" bf_compile_results.txt | wc -l )
echo A total of $compcount modules compiled.
echo Setup complete. Check bf_compile_results.txt for errors.
