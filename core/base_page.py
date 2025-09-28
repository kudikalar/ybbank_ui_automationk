# core/base_page.py
from __future__ import annotations

from pathlib import Path
from typing import Tuple, List, Optional, Union, Any
from urllib.parse import urljoin

import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from core.logger import get_logger
from core.wait import Waiter
from config.config import ENVIRONMENTS, DEFAULT_ENV

Locator = Tuple[str, str]


def _resolve_base_url(value: str) -> str:
    """Accepts full URL or env alias like 'qa' and returns a proper base URL."""
    if not value:
        return ENVIRONMENTS[DEFAULT_ENV].rstrip("/")
    v = value.strip()
    if "://" in v:
        return v.rstrip("/")
    if v in ENVIRONMENTS:
        return ENVIRONMENTS[v].rstrip("/")
    return ENVIRONMENTS[DEFAULT_ENV].rstrip("/")


class BasePage:
    logger = get_logger("BasePage")

    def __init__(self, driver: WebDriver, base_url: str = "", timeout: int = 15, poll: float = 0.3):
        self.driver = driver
        self.base_url = _resolve_base_url(base_url)
        # IMPORTANT: only use self.w (a Waiter). Do not set/override self.wait.
        self.w = Waiter(driver, timeout=timeout, poll=poll)

    # ------------------ Navigation ------------------
    def open(self, path: str = "/") -> None:
        url = urljoin(self.base_url + "/", path.lstrip("/"))
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        self.w.js_ready()

    # ------------------ Low-level finds ------------------
    def find(self, locator: Locator) -> WebElement:
        # Use the underlying WebDriverWait exposed at self.w.wait
        return self.w.wait.until(EC.presence_of_element_located(locator))

    def finds(self, locator: Locator) -> List[WebElement]:
        return self.driver.find_elements(*locator)

    def find_visible(self, locator: Locator) -> WebElement:
        return self.w.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: Locator) -> WebElement:
        return self.w.wait.until(EC.element_to_be_clickable(locator))

    # ------------------ Clicks with waits ------------------
    def click(self, locator: Locator, retry: int = 2) -> WebElement:
        step_name = f"Click {locator}"
        with allure.step(step_name):
            last_err: Optional[Exception] = None
            for attempt in range(retry + 1):
                try:
                    el = self.find_clickable(locator)
                    # Scroll + move helps with overlays
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    ActionChains(self.driver).move_to_element(el).pause(0.05).click(el).perform()
                    self.logger.info(f"Clicked: {locator}")
                    return el
                except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException) as e:
                    last_err = e
                    self.logger.warning(f"Click failed ({attempt + 1}/{retry + 1}) for {locator}: {e}")
                    # attach after failed attempt
                    self._attach_allure_snapshot(f"Click failed attempt {attempt + 1} on {locator}")
                    # ensure DOM ready before retry
                    try:
                        self.wait.js_ready()
                    except Exception:
                        pass

            # final JS fallback inside the same allure step
            try:
                el = self.find_visible(locator)
                self.driver.execute_script("arguments[0].click();", el)
                self.logger.info(f"JS-clicked: {locator}")
                allure.attach(f"Used JS fallback for {locator}", name="Click fallback",
                              attachment_type=AttachmentType.TEXT)
                return el
            except Exception as e:
                self._attach_allure_snapshot(f"JS click failed on {locator}")
                self.logger.error(f"JS click failed for {locator}: {e}", exc_info=True)
                raise last_err if last_err else e

    def js_click(self, locator: Locator, retry: int = 1) -> WebElement:
        step_name = f"JS Click {locator}"
        with allure.step(step_name):
            last_err: Optional[Exception] = None
            for attempt in range(retry + 1):
                try:
                    el = self.find_visible(locator)
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    self.driver.execute_script("arguments[0].click();", el)
                    self.logger.info(f"JS-clicked: {locator}")
                    return el
                except StaleElementReferenceException as e:
                    last_err = e
                    self.logger.warning(f"JS click stale ({attempt + 1}/{retry + 1}) for {locator}: {e}")
                    self._attach_allure_snapshot(f"JS click stale attempt {attempt + 1} on {locator}")
                    try:
                        self.wait.js_ready()
                    except Exception:
                        pass
                except Exception as e:
                    last_err = e
                    self._attach_allure_snapshot(f"JS click failed attempt {attempt + 1} on {locator}")
                    self.logger.error(f"JS click error on {locator}: {e}", exc_info=True)

            raise last_err if last_err else RuntimeError(f"Unable to JS-click {locator}")

    def type(self, locator: Locator, text: str, clear: bool = True, press_enter: bool = False) -> WebElement:
        # redact long/secret values if needed
        preview = text if (text is None or len(text) <= 80) else text[:77] + "..."
        step_name = f"Type into {locator} | value='{preview}'"
        with allure.step(step_name):
            try:
                el = self.find_visible(locator)
                if clear:
                    el.clear()
                self.logger.info(f"Typing into {locator}: '{preview}'")
                el.send_keys(text)
                if press_enter:
                    el.send_keys(Keys.ENTER)
                return el
            except Exception as e:
                self._attach_allure_snapshot(f"Type failed on {locator}")
                self.logger.error(f"Failed typing into {locator}: {e}", exc_info=True)
                raise

    def _attach_allure_snapshot(self, title: str) -> None:
        """Attach screenshot + page source to Allure (best-effort)."""
        try:
            png = self.driver.get_screenshot_as_png()
            allure.attach(png, name=f"{title} - screenshot", attachment_type=AttachmentType.PNG)
        except Exception:
            pass
        try:
            allure.attach(self.driver.page_source, name=f"{title} - page source", attachment_type=AttachmentType.HTML)
        except Exception:
            pass

    # ------------------ Reads ------------------
    def text_of(self, locator: Locator) -> str:
        return self.find_visible(locator).text

    def attr(self, locator: Locator, name: str) -> str:
        return self.find(locator).get_attribute(name)

    def css(self, locator: Locator, name: str) -> str:
        return self.find(locator).value_of_css_property(name)

    def is_visible(self, locator: Locator) -> bool:
        try:
            self.find_visible(locator)
            return True
        except TimeoutException:
            return False

    def is_present(self, locator: Locator) -> bool:
        try:
            self.find(locator)
            return True
        except TimeoutException:
            return False

    def is_clickable_now(self, locator: Locator) -> bool:
        try:
            self.find_clickable(locator)
            return True
        except TimeoutException:
            return False

    def count(self, locator: Locator) -> int:
        return len(self.finds(locator))

    # ------------------ Select (dropdown) ------------------
    def select_by_text(self, locator: Locator, text: str) -> None:
        Select(self.find_visible(locator)).select_by_visible_text(text)

    def select_by_value(self, locator: Locator, value: str) -> None:
        Select(self.find_visible(locator)).select_by_value(value)

    def select_by_index(self, locator: Locator, index: int) -> None:
        Select(self.find_visible(locator)).select_by_index(index)

    def deselect_all(self, locator: Locator) -> None:
        Select(self.find_visible(locator)).deselect_all()

    def selected_texts(self, locator: Locator) -> List[str]:
        return [o.text for o in Select(self.find(locator)).all_selected_options]

    # ------------------ Mouse actions ------------------
    def hover(self, locator: Locator) -> WebElement:
        el = self.find_visible(locator)
        ActionChains(self.driver).move_to_element(el).perform()
        return el

    def double_click(self, locator: Locator) -> WebElement:
        el = self.find_visible(locator)
        ActionChains(self.driver).double_click(el).perform()
        return el

    def right_click(self, locator: Locator) -> WebElement:
        el = self.find_visible(locator)
        ActionChains(self.driver).context_click(el).perform()
        return el

    def drag_and_drop(self, source: Locator, target: Locator) -> None:
        src = self.find_visible(source)
        dst = self.find_visible(target)
        ActionChains(self.driver).drag_and_drop(src, dst).perform()

    def drag_and_drop_by_offset(self, source: Locator, x: int, y: int) -> None:
        src = self.find_visible(source)
        ActionChains(self.driver).drag_and_drop_by_offset(src, x, y).perform()

    # ------------------ Scrolling ------------------
    def scroll_into_view(self, locator: Locator, align_to_top: bool = True) -> WebElement:
        el = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(arguments[1]);", el, align_to_top)
        return el

    def scroll_to_top(self) -> None:
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ------------------ Frames / Windows ------------------
    def switch_to_frame(self, locator_or_index: Union[Locator, int, WebElement]) -> None:
        if isinstance(locator_or_index, tuple):
            self.w.frame_and_switch(locator_or_index)
        elif isinstance(locator_or_index, int):
            self.driver.switch_to.frame(locator_or_index)
        else:
            self.driver.switch_to.frame(locator_or_index)

    def switch_to_default(self) -> None:
        self.driver.switch_to.default_content()

    def switch_to_window(self, index: int = -1) -> None:
        self.w.js_ready()
        handles = self.driver.window_handles
        target = handles[index]
        self.driver.switch_to.window(target)

    def switch_to_window_by_title(self, title_fragment: str, timeout: int = 10) -> None:
        def _by_title(_):
            for h in self.driver.window_handles:
                self.driver.switch_to.window(h)
                if title_fragment in self.driver.title:
                    return True
            return False
        Waiter(self.driver, timeout=timeout).wait.until(_by_title)

    # ------------------ Alerts ------------------
    def alert_accept(self) -> None:
        self.w.wait.until(lambda d: d.switch_to.alert).accept()

    def alert_dismiss(self) -> None:
        self.w.wait.until(lambda d: d.switch_to.alert).dismiss()

    def alert_text(self) -> str:
        return self.w.wait.until(lambda d: d.switch_to.alert).text

    def alert_type(self, text: str, accept: bool = True) -> None:
        al = self.w.wait.until(lambda d: d.switch_to.alert)
        al.send_keys(text)
        (al.accept() if accept else al.dismiss())

    # ------------------ Files / Screens ------------------
    def upload_file(self, locator: Locator, file_path: Union[str, Path]) -> WebElement:
        p = str(Path(file_path).resolve())
        return self.type(locator, p, clear=False)

    def screenshot(self, name: str = "screenshot", directory: Union[str, Path] = "screenshots") -> Path:
        Path(directory).mkdir(parents=True, exist_ok=True)
        path = Path(directory) / f"{name}.png"
        self.driver.save_screenshot(str(path))
        return path

    # ------------------ JS / Network helpers ------------------
    def execute_script(self, script: str, *args) -> Any:
        return self.driver.execute_script(script, *args)

    def execute_async_script(self, script: str, *args) -> Any:
        return self.driver.execute_async_script(script, *args)

    def page_ready(self) -> bool:
        return self.w.js_ready()

    def ajax_idle(self) -> bool:
        return self.w.ajax_complete(timeout_ok=True)

    # ------------------ Wait wrappers (convenience) ------------------
    def wait_visible(self, locator: Locator) -> WebElement:
        return self.w.visible(locator)

    def wait_clickable(self, locator: Locator) -> WebElement:
        return self.w.clickable(locator)

    def wait_invisible(self, locator: Locator) -> bool:
        return self.w.invisible(locator)

    def wait_text(self, locator: Locator, text: str) -> bool:
        return self.w.text_in(locator, text)

    def wait_url_contains(self, fragment: str) -> bool:
        return self.w.url_contains(fragment)

    def wait_title_contains(self, text: str) -> bool:
        return self.w.title_contains(text)

    # ------------------ Utilities ------------------
    def safe_get(self, locator: Locator, default: Optional[str] = None) -> Optional[str]:
        try:
            return self.text_of(locator)
        except TimeoutException:
            return default

    def exists_now(self, locator: Locator) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
