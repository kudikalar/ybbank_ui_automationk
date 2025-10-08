from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base_page import BasePage

class Shoes_Add_To_Cart(BasePage):
    APPERAL_AND_SHOES= (By.XPATH,"/html/body/div[4]/div[1]/div[2]/ul[1]/li[4]/a")
    ADD_TO_CART_SHOES=(By.XPATH,"/html/body/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[3]/div[2]/div/div[2]/div[3]/div[2]/input")
    SHOPPING_CART_TEXT = (By.XPATH, "//*[@id='topcartlink']/a/span[1]")
    COUNTRY = (By.ID, "CountryId")
    PROVINCE = (By.ID, "StateProvinceId")
    ZIP = (By.ID, "ZipPostalCode")
    ESTIMATE_BTN = (By.CLASS_NAME, "estimate-shipping-button")
    CHECK_BOX = (By.ID, "termsofservice")
    CHECKOUT = (By.ID, "checkout")

    def apperal_and_shoes(self):
        self.click(self.APPERAL_AND_SHOES)

    def add_to_cart_shoes(self):
        self.click(self.ADD_TO_CART_SHOES)

    def click_shopping_cart(self):
        self.click(self.SHOPPING_CART_TEXT)

    def select_country(self, name):
        self.select_by_text(self.COUNTRY, name)

    def select_province(self, name):
        self.select_by_text(self.PROVINCE, name)

    def enter_zip(self, value):
        self.type(self.ZIP, value)

    def select_checkbox(self):
        self.click(self.CHECK_BOX)

    def select_checkout(self):
        self.click(self.CHECKOUT)
