from typing import Tuple, Optional
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
)


class Waiter:
    """
    Handy explicit waits for Selenium.
    `locator` is a tuple like: (By.ID, "username")
    """

    def __init__(self, driver: WebDriver, timeout: int = 15, poll: float = 0.3):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            timeout=timeout,
            poll_frequency=poll,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        )

    # --- Common element waits ---
    def visible(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def present(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible_all(self, locator: Tuple[str, str]):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def present_all(self, locator: Tuple[str, str]):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def invisible(self, locator: Tuple[str, str]) -> bool:
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def staleness(self, element: WebElement) -> bool:
        return self.wait.until(EC.staleness_of(element))

    # --- Text / attribute waits ---
    def text_in(self, locator: Tuple[str, str], text: str) -> bool:
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def value_not_empty(self, locator: Tuple[str, str]) -> WebElement:
        def _non_empty_value(_driver):
            el = _driver.find_element(*locator)
            return el if (el.get_attribute("value") or "").strip() != "" else False

        return self.wait.until(_non_empty_value)

    def attr_contains(self, locator: Tuple[str, str], attr: str, substring: str) -> WebElement:
        def _attr_has(_driver):
            el = _driver.find_element(*locator)
            val = el.get_attribute(attr) or ""
            return el if substring in val else False

        return self.wait.until(_attr_has)

    # --- Navigation / context waits ---
    def url_contains(self, fragment: str) -> bool:
        return self.wait.until(EC.url_contains(fragment))

    def title_is(self, title: str) -> bool:
        return self.wait.until(EC.title_is(title))

    def title_contains(self, text: str) -> bool:
        return self.wait.until(EC.title_contains(text))

    def frame_and_switch(self, locator: Tuple[str, str]) -> bool:
        return self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    # --- Page readiness / network helpers ---
    def js_ready(self) -> bool:
        """Document readyState == 'complete'."""
        return self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    def ajax_complete(self, timeout_ok: bool = True) -> bool:
        """
        Wait until jQuery AJAX is idle (if jQuery exists). If no jQuery on page:
        - returns True immediately.
        If timeout_ok is True and it times out, returns False instead of raising.
        """
        try:
            return self.wait.until(
                lambda d: d.execute_script(
                    "return !!window.jQuery ? (jQuery.active === 0) : true;"
                )
            )
        except TimeoutException:
            if timeout_ok:
                return False
            raise

    # --- Small action helpers using waits ---
    def wait_and_click(self, locator: Tuple[str, str]) -> WebElement:
        el = self.clickable(locator)
        try:
            el.click()
        except ElementClickInterceptedException:
            self.js_ready()
            el.click()
        return el

    def wait_and_type(self, locator: Tuple[str, str], text: str, clear: bool = True) -> WebElement:
        el = self.visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)
        return el

# core/wait.py  (inside class Waiter)
def until(self, condition):
    return self.wait.until(condition)
