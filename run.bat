@echo on
echo === WORKSPACE ===
cd
dir /b

REM ===== Clean venv (optional) =====
if exist venv rmdir /s /q venv

REM ===== Locate Python =====
set "PY=C:\Python312\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" --version || (echo Python missing & exit /b 1)

REM ===== Venv =====
"%PY%" -m venv venv
call venv\Scripts\activate

REM ===== Pip bootstrap =====
python -m pip install -U pip setuptools wheel

REM ===== Deps =====
pip install -r requirements.txt --prefer-binary || (
  echo Primary install failed, retrying legacy...
  pip install -r requirements.txt --prefer-binary --no-build-isolation
)

REM ===== Sanity: pytest present? =====
python -c "import pytest, sys; print('pytest', pytest.__version__)" || pip install pytest
python -c "import selenium" 2>nul || pip install selenium
python -c "import webdriver_manager" 2>nul || pip install webdriver-manager

echo === Search for tests directory ===
set "TEST_PATH="
if exist tests\ (set "TEST_PATH=tests")
if not defined TEST_PATH (
  for /f "delims=" %%D in ('dir /s /b /ad ^| findstr /r /i "\\tests$"') do (
    set "TEST_PATH=%%D"
    goto :found_tests
  )
)
:found_tests

if not defined TEST_PATH (
  echo !!! Could not find a tests folder. Listing python files for hint:
  dir /s /b *.py
  echo !!! Set TEST_PATH manually or add pytest.ini with testpaths.
  exit /b 2
)

echo Using TEST_PATH=%TEST_PATH%
dir /b %TEST_PATH%

REM ===== Optional headless flag for your framework =====
set HEADLESS=true

REM ===== Run pytest explicitly on the found path =====
python -m pytest "%TEST_PATH%" -v -n auto --alluredir=reports\allure-results
set "PYTEST_EXIT=%ERRORLEVEL%"

REM ===== Try to generate static HTML only if allure CLI exists =====
where allure >nul 2>nul && (
  allure generate reports\allure-results -o reports\allure-report --clean
) || (
  echo (info) Allure CLI not found on PATH; Jenkins plugin will render results.
)

exit /b %PYTEST_EXIT%
