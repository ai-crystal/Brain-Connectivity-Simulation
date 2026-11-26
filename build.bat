@echo off
setlocal
cd /d "%~dp0"
set "PYEXE="
set "PYARG="
where python >nul 2>nul && set "PYEXE=python"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PYEXE if exist "C:\Python312\python.exe" set "PYEXE=C:\Python312\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" set "PYEXE=%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" & set "PYARG=-3"
if not defined PYEXE (
  echo [ERROR] Python 3.10+ not found. Please install Python and retry.
  pause
  exit /b 1
)
"%PYEXE%" %PYARG% -c "import typst, pypandoc, fitz" >nul 2>nul
if errorlevel 1 (
  echo [SETUP] Installing dependencies, this may take a few minutes...
  "%PYEXE%" %PYARG% -m pip install --upgrade typst pypandoc_binary pymupdf matplotlib
  if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
  )
)

echo [BUILD] Building all books...
"%PYEXE%" %PYARG% books\build\build.py
if errorlevel 1 (
  echo [ERROR] Build failed.
  pause
  exit /b 1
)
"%PYEXE%" %PYARG% booksuild\check.py
if errorlevel 1 (
  echo [ERROR] Check failed.
  pause
  exit /b 1
)
echo [DONE] PDFs are in the output folder.
pause
