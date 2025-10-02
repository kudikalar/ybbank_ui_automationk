import pytest

from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestValid:

    @pytest.mark.smoke
    def test_valid_login(self,driver, env):
        # 1) Go to home page
        hp = HomePage(driver, env)
        hp.open_home()

        # 2) Go to login page
        lp = LoginPage(driver, env)
        lp.open_login_page()

        # 3) Actually the credentials should read from Excel, but here i used hardcore
        email = "myfirsttestcase@gmail.com"
        password = "test@123"

        # 4) Perform login
        lp.enter_email(email)
        lp.enter_password(password)

        #5) Verify login
        assert lp.click_login(), "Login Successful with valid credentials"

        #6) Verify logout
        assert lp.click_logout(), "Logged out Successful"


