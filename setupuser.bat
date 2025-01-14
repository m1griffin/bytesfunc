REM MS Windows version.
REM This script will do a simple user local setup of arrayfunc or bytesfunc. 
REM Call pip directly with the appropriate options if you wish to have a
REM different type of install.

REM This requires the python Windows launcher to be present.

echo off


REM ###################################################################

REM Set the variables used to define the package type. 
fcompileresults="bf_compileresults.txt"
fcompileerrors="bf_compileerrors.txt"
fpkgversion="bf_version.txt"
pkgname="bytesfunc"

REM ###################################################################


echo
echo "Installing package for %pkgname%"
echo "Compile results will be in %fcompileresults%"
echo "Error results will be in %fcompileerrors%"
echo "Version results will be in %fpkgversion%"
echo 

REM ###################################################################

REM This tells distutils that Visual Studio isn't installed, just the compiler.
SET DISTUTILS_USE_SDK=1

REM Set the environment variables.
REM This version was used with the regular MSVC compiler.
REM call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build"\vcvarsall.bat amd64
REM This version was used with the "Community" version.
REM call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build"\vcvars64.bat amd64
REM This version is for the community edition of Visual Studio 2022 on Windows 11. 
REM call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build"\vcvars64.bat amd64
REM version is for the community edition of Visual Studio 2022 on Windows 11.  
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build"\vcvars64.bat amd64

ECHO ON

ECHO Setting path next.

REM This adds the paths to the required compiler components.
REM This version was used with the regular MSVC compiler.
REM SET PATH=C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.10.25017\bin\HostX64\x64;C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.10.25017\lib\x64;C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.10.25017\include;C:\Program Files (x86)\Windows Kits\10\Include\10.0.15063.0\ucrt;%PATH%
REM This version was used with the "Community" version. Note that there is a numerical version number in the
REM path which will change from time to time and need to be updated.
REM SET PATH=c:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.15.26726\bin\Hostx64\x64;c:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.15.26726\lib\x64;c:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.15.26726\include;C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\SDK\ScopeCppSDK\SDK\include\ucrt;%PATH%
REM For VC 2022 on Windows 11.
REM SET PATH=c:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.41.34120\bin\Hostx64\x64;c:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.41.34120\lib\x64;c:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.41.34120\include;%PATH%
REM for VC 2022 on Windows 11, with later version of Visual Studio.
SET PATH=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.42.34433\bin\Hostx64\x64;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.42.34433\lib\x64;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.42.34433\include;C:\Program Files (x86)\Windows Kits\10\Include\10.0.22621.0\ucrt;%PATH%


REM =================================================================

echo Running %pkgname% build as a local install. 
echo Compiler messages are redirected to %fcompileresults%


REM =================================================================

ECHO Installing using pip ...

REM Installing from local package.
echo "Running %pkgname% build as a local install using pip."
pip install --user --force-reinstall %pkgname% 1>> %fcompileresults% 2>> %fcompileerrors%


REM =================================================================

REM Append the compile errors to the compile results file.
echo. >> %fcompileresults%
type %fcompileerrors% >> %fcompileresults%

echo Setup complete. Check %fcompileresults% for errors.

echo Saving package version results to file.
pip show %pkgname% > %fpkgversion%


