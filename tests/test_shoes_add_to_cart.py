import pytest
import allure
import os
from core.wait import Waiter
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.shoes_add_to_cart import Shoes_Add_To_Cart
from utils.assertions import assert_equals
from utils.data_reader import read_excel

test_data = read_excel("data/Login_test_data.xlsx")
@pytest.mark.parametrize("data", test_data)
@allure.feature("Registration")
class Test_shoes_cart:

    def test_blue_shoes(self,env,driver,data):
        hp = HomePage(driver, env)
        hp.open_home()

        lp = LoginPage(driver, env)
        lp.open_login_page()

        lp.enter_email_address(data["EmailIDLogin"])
        lp.enter_password(data["PasswordLogin"])
        lp.click_login_btn()

        sp= Shoes_Add_To_Cart(driver,env)
       # Waiter(driver).visible(sp.APPERAL_AND_SHOES)

        sp.apperal_and_shoes()
       # Waiter(driver).visible(sp.ADD_TO_CART_SHOES)

        sp.add_to_cart_shoes()
        sp.click_shopping_cart()

        sp.select_country("India")
        sp.enter_zip("500081")
        sp.select_checkbox()
        sp.select_checkout()




