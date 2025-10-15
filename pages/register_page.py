from selenium.webdriver.common.by import By
from core.base_page import BasePage

class RegisterPage(BasePage):
    #Page Objects
    FIRSTNAME     = (By.ID, "first")
    LASTNAME      = (By.ID, "last")
    EMAIL         = (By.ID, "email")
    PASSWORD      = (By.ID, "pass")
    CONFIRM_PWD   = (By.ID, "confirm")
    REGISTER_BTN  = (By.ID, "submit")
    #Error validation
    PASSWORD_MISMATCH =(By.ID,"confirmErr")
    #SMOKE VALIDATION
    REGISTER_PAGE_TITLE =(By.XPATH,'//*[@id="h1]')
    FIRSTNAME_FIELD_TITLE =(By.XPATH,'//*[@id="form"]/div[1]/div[1]/label')
    FIRSTNAME_FIELD_WATER_MARK =(By.XPATH,'//*[@id="first"]')
    LASTNAME_FIELD_TITLE =(By.XPATH,'//*[@id="form"]/div[1]/div[2]/label')
    LASTNAME_FIELD_WATER_MARK =(By.XPATH,'//*[@id="last"]')
    EMAIL_FIELD_TITLE=(By.XPATH,'//*[@id="form"]/div[1]/div[3]/label')
    EMAIL_FIELD_WATER_MARK=(By.XPATH,'//*[@id="email"]')
    PASSWORD_FIELD_TITLE=(By.XPATH,'//*[@id="form"]/div[1]/div[4]/label')
    PASSWORD_FIELD_WATER_MARK=(By.XPATH,'//*[@id="pass"]')
    CONFIRM_PWD_FIELD_TITLE=(By.XPATH,'//*[@id="form"]/div[1]/div[5]/label')
    CONFIRM_PWD_FIELD_WATER_MARK=(By.XPATH,'//*[@id="confirm"]')
    REGISTER_BUTTON=(By.XPATH,'//*[@id="submit"]')
    SIGIN_OPTION=(By.XPATH,'//*[@id="form"]/div[2]/a')
    FOOTER_LINE=(By.XPATH,'/html/body/main/div[2]/span[1]')

    def __init__(self, driver, env):
        super().__init__(driver, env)

    def open_register_page(self):
        self.open("/register.html")
        self.wait_url_contains("/register.html")
        self.wait_visible(self.REGISTER_BTN)

    def enter_first_name(self, v):       self.type(self.FIRSTNAME, v)
    def enter_last_name(self, v):        self.type(self.LASTNAME, v)
    def enter_email_address(self, v):    self.type(self.EMAIL, v)
    def enter_password(self, v):         self.type(self.PASSWORD, v)
    def enter_confirm_password(self, v): self.type(self.CONFIRM_PWD, v)
    def click_register_button(self):     self.click(self.REGISTER_BTN)
    #def if_password_error_displayed(self):  self.is_visible(self.PASSWORD_MISMATCH)
    def password_error(self):   return self.text_of(self.PASSWORD_MISMATCH)




