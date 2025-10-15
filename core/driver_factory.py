# core/driver_factory.py
import os
import json
import logging
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

log = logging.getLogger("DriverFactory")

_SAUCE_DCS = ("us-west-1", "eu-central-1", "apac-southeast-1")


def _sauce_host(region: str) -> str:
    r = (region or "us-west-1").lower()
    if r in ("eu", "eu-central-1"):
        return "ondemand.eu-central-1.saucelabs.com/wd/hub"
    if r.startswith(("apac", "ap-southeast-1", "apac-southeast-1")):
        return "ondemand.apac-southeast-1.saucelabs.com/wd/hub"
    return "ondemand.us-west-1.saucelabs.com/wd/hub"


def _norm(val, *, lower: bool = True, default=None):
    if val is None:
        return default
    s = str(val).strip()
    return s.lower() if lower else s


class DriverFactory:
    # ----------------- Local drivers -----------------

    @staticmethod
    def _chrome(headless: bool):
        opts = ChromeOptions()
        opts.add_argument("--start-maximized")
        if headless:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(service=ChromeService(), options=opts)

    @staticmethod
    def _firefox(headless: bool):
        opts = FirefoxOptions()
        opts.headless = headless
        driver = webdriver.Firefox(service=FirefoxService(), options=opts)
        try:
            driver.maximize_window()
        except Exception:
            pass
        return driver

    @staticmethod
    def _edge(headless: bool):
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(service=EdgeService(), options=opts)
        try:
            driver.maximize_window()
        except Exception:
            pass
        return driver

    # ----------------- Factory entry -----------------

    @staticmethod
    def create_driver(
        *,
        browser: str = "chrome",
        headless: bool = False,
        remote: bool = False,
        platform: str = "Windows",
        cloud: Optional[str] = None,
        grid_url: Optional[str] = None,
        platform_name: str = "Windows 11",
        browser_version: str = "latest",
        sauce_build: Optional[str] = None,
        sauce_name: Optional[str] = None,
        sauce_tags: Optional[str] = "pytest",
        sauce_region: str = "us-west-1",
        sauce_tunnel: Optional[str] = None,
    ):
        """
        Create a WebDriver. Default is local.
        Remote is ONLY enabled by the caller (--remote). Env vars do not force it.
        """

        # Normalize inputs
        browser         = _norm(os.getenv("SAUCE_BROWSER", browser), lower=True) or "chrome"
        platform_name   = _norm(os.getenv("SAUCE_PLATFORM", platform_name), lower=False) or "Windows 11"
        browser_version = _norm(os.getenv("SAUCE_VERSION", browser_version), lower=False) or "latest"
        sauce_region    = _norm(os.getenv("SAUCE_REGION", sauce_region), lower=True) or "us-west-1"
        sauce_build     = _norm(os.getenv("SAUCE_BUILD", sauce_build or "Automation Build"), lower=False)
        sauce_name      = _norm(os.getenv("SAUCE_NAME", sauce_name or "PyTest Run"), lower=False)
        sauce_tags_env  = _norm(os.getenv("SAUCE_TAGS"), lower=False)
        sauce_tags      = sauce_tags_env or sauce_tags or "pytest"
        sauce_tunnel    = _norm(os.getenv("SAUCE_TUNNEL", sauce_tunnel), lower=False)
        cloud           = _norm(cloud, lower=True)

        # Normalize browser aliases
        b = browser
        if b in ("gc", "google-chrome"):
            b = "chrome"
        elif b in ("ff",):
            b = "firefox"
        elif b in ("msedge",):
            b = "edge"

        # ---- Local (default) ----
        if not remote:
            if b == "chrome":  return DriverFactory._chrome(headless)
            if b == "firefox": return DriverFactory._firefox(headless)
            if b == "edge":    return DriverFactory._edge(headless)
            raise ValueError(f"Unsupported browser: {browser!r}")

        # ---- Remote options (Grid/Sauce) ----
        if b == "chrome":
            opts = ChromeOptions()
        elif b == "firefox":
            opts = FirefoxOptions()
        elif b == "edge":
            opts = EdgeOptions()
        else:
            raise ValueError(f"Unsupported remote browser: {browser!r}")

        # Headless for generic grids (Sauce ignores)
        if headless and cloud != "saucelabs":
            if b == "firefox":
                opts.headless = True
            else:
                opts.add_argument("--headless=new")

        # W3C caps
        opts.set_capability("platformName", platform_name)
        opts.set_capability("browserVersion", browser_version)

        # ---- Sauce Labs ----
        if cloud == "saucelabs":
            user = _norm(os.environ.get("SAUCE_USERNAME"), lower=False)
            key = _norm(os.environ.get("SAUCE_ACCESS_KEY"), lower=False)
            if not user or not key:
                raise RuntimeError("SAUCE_USERNAME/SAUCE_ACCESS_KEY not set (and no grid_url provided).")

            # region
            dc = sauce_region
            if dc in ("", "us"): dc = "us-west-1"
            if dc == "eu":       dc = "eu-central-1"
            if dc in ("apac", "ap-southeast-1"): dc = "apac-southeast-1"

            tags_list = [t.strip() for t in (sauce_tags or "").split(",") if t.strip()]
            sauce_options = {
                "username": user,
                "accessKey": key,
                "build": sauce_build,
                "name": sauce_name,
                "tags": tags_list,
                "screenResolution": "1920x1080",
                "seleniumVersion": "4.25.0",
                "github": {"sha": os.getenv("GITHUB_SHA"), "runId": os.getenv("GITHUB_RUN_ID")},
            }
            if sauce_tunnel:
                sauce_options["tunnelName"] = sauce_tunnel

            opts.set_capability("sauce:options", sauce_options)

            host_path = _sauce_host(dc)
            remote_url = f"https://{user}:{key}@{host_path}"

            # Log safe/redacted caps
            try:
                caps = getattr(opts, "capabilities", {}) or {}
                cap_redacted = json.loads(json.dumps(caps))
                if "sauce:options" in cap_redacted:
                    cap_redacted["sauce:options"]["username"] = "***"
                    cap_redacted["sauce:options"]["accessKey"] = "***"
                log.info("Creating Sauce session at https://%s", host_path)
                log.info("Capabilities: %s", json.dumps(cap_redacted, indent=2))
            except Exception:
                pass

            return webdriver.Remote(command_executor=remote_url, options=opts)

        # ---- Generic Selenium Grid ----
        if not grid_url:
            raise RuntimeError("Remote requested but neither Sauce nor --grid-url was provided.")
        return webdriver.Remote(command_executor=grid_url, options=opts)
