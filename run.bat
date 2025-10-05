@echo on
cd /d "%WORKSPACE%"
if exist venv rmdir /s /q venv

set "PY=C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" -m venv venv
call venv\Scripts\activate
python -m pip install -U pip setuptools wheel

python -m pip install --prefer-binary pytest allure-pytest selenium webdriver-manager openpyxl==3.1.5 -vvv ^
|| python -m pip install --prefer-binary --no-build-isolation pytest allure-pytest selenium webdriver-manager openpyxl==3.1.5 -vvv

set "PYTHONPATH=%CD%"
python -m pytest --alluredir=reports\allure-results
set RC=%ERRORLEVEL%

if exist reports\allure-results\*.json (
  "C:\ProgramData\Jenkins\.jenkins\tools\ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation\C_Program_Files_Allure_allure-2.35.1_bin\bin\allure.bat" ^
    generate reports\allure-results -c -o reports\allure-report
) else (
  echo [WARN] No Allure results. Skipping report generation.
)

exit /b %RC%
