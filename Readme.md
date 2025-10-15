1. commands to run in saucelab
[pytest -v tests/test_register.py --remote --cloud saucelabs --browser chrome --sauce-region eu]

#run headless in saucelab
[pytest -v tests/test_register.py --remote --cloud saucelabs --browser chrome --headless --sauce-region eu]

#run headless in saucelab specific test
[pytest tests/test_register.py::TestRegister::test_verify_system_prevents_duplicate_email_registration --remote --cloud saucelabs --browser chrome --headless --sauce-region eu]

🔹 1. Run Locally (Chrome, UI mode)
[pytest -v tests/test_register.py --browser chrome]

🔹 2. Run Locally (Firefox, headless)
[pytest -v tests/test_register.py --browser firefox --headless]

🔹 3. Run on Local Selenium Grid
[pytest -v tests/test_register.py --remote --browser chrome --grid-url "http://localhost:4444/wd/hub"]

✅ Step 1: Install the Pytest Allure Plugin
Run in your virtual environment:
pip install allure-pytest

✅ Step 2: Run Tests with Allure Directory
Execute your pytest command with the --alluredir option:
pytest -v --alluredir=reports/allure-results

👉 This will generate JSON files inside reports/allure-results.

✅ Step 3: Generate Allure Report
Now create the HTML report:
*[allure generate reports/allure-results -o reports/allure-report --clean]*

Open the report:
[allure open reports/allure-report]

1️⃣ Run Specific Test on Sauce Labs (Chrome, EU region)
[pytest -v tests/test_register.py --remote --cloud saucelabs --browser chrome --sauce-region eu]

2️⃣ Run Headless Browser on Sauce Labs
[pytest -v tests/test_register.py --remote --cloud saucelabs --browser chrome --headless --sauce-region eu]

3️⃣ Run on Different Desktop Browsers
Firefox
[pytest -v tests/test_login.py --remote --cloud saucelabs --browser firefox --sauce-region eu]

Microsoft Edge
[pytest -v tests/test_add_tocart.py --remote --cloud saucelabs --browser edge --sauce-region eu]

4️⃣ Run on Mobile Devices (via Sauce Labs Emulators/Simulators)
Android Chrome (Pixel 7)
[pytest -v tests/test_login.py --remote --cloud saucelabs --browser chrome --sauce-region eu --cap "appium:platformName=Android" --cap "appium:platformVersion=13.0" --cap "appium:deviceName=Google Pixel 7" --cap "browserName=Chrome"]

iOS Safari (iPhone 14)
[pytest -v tests/test_login.py --remote --cloud saucelabs --browser safari --sauce-region eu --cap "appium:platformName=iOS" --cap "appium:platformVersion=16.0" --cap "appium:deviceName=iPhone 14 Simulator" --cap "browserName=Safari"]

5️⃣ Run With Allure Reporting Enabled
[pytest -v tests/ --remote --cloud saucelabs --browser chrome --sauce-region eu --alluredir=reports/allure-results]

Then generate and open report:
[allure generate reports/allure-results -o reports/allure-report --clean && allure open reports/allure-report]

Run with Specific Class with a Test including allure report
[pytest tests/test_register.py::TestRegister --alluredir=reports/allure-results]

Generate Allure Report as Server
[allure serve reports/allure-results]

