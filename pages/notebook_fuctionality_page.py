from selenium.webdriver.common.by import By
from core.base_page import BasePage

class NotebookPage(BasePage):
    COMPUTERS_MENU = (By.LINK_TEXT, "Computers")
    NOTEBOOKS_MENU = (By.LINK_TEXT, "Notebooks")
    SELECT_NOTEBOOK = (By.LINK_TEXT, "14.1-inch Laptop")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-button-31")
    SHOPPING_CART_LINK = (By.XPATH, "//*[@id='topcartlink']/a/span[1]")

    CART_TABLE = (By.CSS_SELECTOR, ".cart")
    COUNTRY_SELECT = (By.ID, "CountryId")
    ZIP_INPUT = (By.ID, "ZipPostalCode")
    TERMS_CHECKBOX = (By.ID, "termsofservice")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_computers_menu(self):
        self.click(self.COMPUTERS_MENU)

    def open_notebooks(self):
        self.click(self.NOTEBOOKS_MENU)

    def select_notebook(self):
        self.click(self.SELECT_NOTEBOOK)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def view_shopping_cart(self):
        self.click(self.SHOPPING_CART_LINK)

    def check_cart_items_present(self):
        return self.is_visible(self.CART_TABLE)

    def select_country(self, country_name):
        self.select_by_text(self.COUNTRY_SELECT, country_name)

    def enter_zip_postal_code(self, zip_code):
        self.type(self.ZIP_INPUT, zip_code)

    def agree_terms(self):
        self.click(self.TERMS_CHECKBOX)

    def proceed_checkout(self):
        self.click(self.CHECKOUT_BUTTON)