import pytest
from time import sleep

from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestValid:

    @pytest.mark.smoke
    def test_valid_login(self,driver, env):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()

        email = "myfirsttestcase@gmail.com"
        password = "test@123"

        lp.enter_email(email)
        lp.enter_password(password)

        lp.click_login()
        lp.click_logout()


