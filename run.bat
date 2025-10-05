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

REM ===== Ensure critical plugins exist =====
python -c "import pytest, sys;print('pytest',pytest.__version__)" || pip install pytest
python -c "import allure_pytest" 2>nul || pip install allure-pytest
python -c "import selenium" 2>nul || pip install selenium
python -c "import webdriver_manager" 2>nul || pip install webdriver-manager
python -m pytest --help | findstr /I allure || (
  echo !!! Allure plugin not loaded. Check venv/site-packages and requirements.txt
  exit /b 2
)

echo === Locate tests ===
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
  echo !!! No tests folder found. Listing python files as hint:
  dir /s /b *.py
  echo !!! Create tests\ or define testpaths in pytest.ini
  exit /b 3
)
echo Using TEST_PATH=%TEST_PATH%
dir /b %TEST_PATH%

REM ===== Optional headless for your framework =====
set HEADLESS=true

REM ===== Clean previous results =====
if exist reports\allure-results rmdir /s /q reports\allure-results

REM ===== Run pytest (first pass without xdist to surface errors) =====
python -m pytest "%TEST_PATH%" -v --alluredir=reports\allure-results
set "PYTEST_EXIT=%ERRORLEVEL%"

echo === Contents of reports\allure-results ===
if exist reports\allure-results (
  dir /b reports\allure-results
) else (
  echo !!! allure-results directory not created (pytest did not run or crashed early)
)

REM ===== Fail early if no JSON produced =====
for /f %%C in ('dir /b /a:-d reports\allure-results 2^>nul ^| find /c /v ""') do set COUNT=%%C
if "%COUNT%"=="" set COUNT=0
echo Files in allure-results: %COUNT%
if %COUNT% LSS 2 (
  echo !!! Allure results look empty. Common causes:
  echo  - Test collection errors (see pytest log above)
  echo  - Plugin not loaded (ensure allure-pytest installed)
  echo  - No tests matched (check file names: test_*.py or *_test.py)
  exit /b %PYTEST_EXIT%
)

REM ===== (Optional) second run with xdist once stable =====
REM python -m pytest "%TEST_PATH%" -v -n auto --alluredir=reports\allure-results

REM ===== Generate static HTML if Allure CLI exists =====
where allure >nul 2>nul && (
  allure generate reports\allure-results -o reports\allure-report --clean
  echo HTML report at reports\allure-report
) || (
  echo (info) Allure CLI not found on PATH; Jenkins Allure plugin can render results.
)

exit /b %PYTEST_EXIT%
