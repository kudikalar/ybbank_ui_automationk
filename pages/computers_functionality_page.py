from selenium.webdriver.common.by import By
from core.base_page import BasePage

class ComputersPage(BasePage):
    COMPUTERS_MENU     = (By.LINK_TEXT, "Computers")
    DESKTOPS_MENU      = (By.LINK_TEXT, "Desktops")
    BUILD_COMPUTER     = (By.LINK_TEXT, "Build your own cheap computer")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button-72")
    SHOPPING_CART_LINK = (By.XPATH, "//*[@id='topcartlink']/a/span[1]")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_computers_menu(self):
        self.click(self.COMPUTERS_MENU)

    def open_desktops(self):
        self.click(self.DESKTOPS_MENU)

    def select_build_computer(self):
        self.click(self.BUILD_COMPUTER)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def view_shopping_cart(self):
        self.click(self.SHOPPING_CART_LINK)