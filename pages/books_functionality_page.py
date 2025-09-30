from selenium.webdriver.common.by import By
from core.base_page import BasePage


class BooksPage(BasePage):
    BOOK_LINK_TEXT     = (By.LINK_TEXT, "Computing and Internet")
    ADD_TO_CART        = (By.ID, "add-to-cart-button-13")
    QTY                = (By.ID, "addtocart_13_EnteredQuantity")
    SHOPPING_CART_TEXT = (By.XPATH, "//*[@id='topcartlink']/a/span[1]")
    COUNTRY            = (By.ID, "CountryId")
    PROVINCE           = (By.ID, "StateProvinceId")
    ZIP                = (By.ID, "ZipPostalCode")
    ESTIMATE_BTN       = (By.CLASS_NAME, "estimate-shipping-button")
    CHECK_BOX          = (By.ID, "termsofservice")
    CHECKOUT           = (By.ID, "checkout")

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_books_page(self):
        self.open("/books")
        self.wait_url_contains("/books")
        self.wait_visible(self.BOOK_LINK_TEXT)

    def click_book_link(self):
        self.click(self.BOOK_LINK_TEXT)

    def set_quantity(self, value):
        self.type(self.QTY, value, clear=True)

    def click_add_to_cart(self):
        self.click(self.ADD_TO_CART)

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
