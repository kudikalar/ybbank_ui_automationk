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

class DriverFactory:
    """Create local or remote WebDriver instances (local, Selenium Grid, Sauce Labs)."""

    # ---------- Local (Selenium Manager resolves drivers) ----------
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
        driver.maximize_window()
        return driver

    @staticmethod
    def _edge(headless: bool):
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(service=EdgeService(), options=opts)
        driver.maximize_window()
        return driver

    # ---------- Remote ----------
    @staticmethod
    def create_driver(
        browser: str = "chrome",
        headless: bool = False,
        remote: bool = False,
        platform: str = "Windows",           # kept for legacy/local code paths
        cloud: Optional[str] = None,         # "saucelabs" | None
        grid_url: Optional[str] = None,
        *,
        # W3C caps (used for Sauce)
        platform_name: str = "Windows 11",
        browser_version: str = "latest",
        sauce_build: Optional[str] = "RegisterSuite",
        sauce_name: Optional[str] = None,
        sauce_tags: Optional[str] = "pytest,demowebshop,register",
        sauce_region: str = "us",
    ):
        b = (browser or "chrome").lower()

        # ---- Local path
        if not remote:
            if b == "chrome":  return DriverFactory._chrome(headless)
            if b == "firefox": return DriverFactory._firefox(headless)
            if b == "edge":    return DriverFactory._edge(headless)
            raise ValueError(f"Unsupported browser: {browser}")

        # ---- Build base options
        if b == "chrome":
            opts = ChromeOptions()
        elif b == "firefox":
            opts = FirefoxOptions()
        elif b == "edge":
            opts = EdgeOptions()
        else:
            raise ValueError(f"Unsupported remote browser: {browser}")

        if headless:
            if b == "firefox":
                opts.headless = True
            else:
                opts.add_argument("--headless=new")

        # Always set W3C core caps
        opts.set_capability("platformName",  platform_name)
        opts.set_capability("browserVersion", browser_version)

        # ---- Sauce Labs
        if cloud == "saucelabs":
            # If a full Sauce URL is provided, use it directly (recommended)
            if grid_url and grid_url.startswith(("http://", "https://")):
                remote_url = grid_url
            else:
                user = os.getenv("SAUCE_USERNAME")
                key  = os.getenv("SAUCE_ACCESS_KEY")
                if not user or not key:
                    raise RuntimeError(
                        "No --grid-url provided and SAUCE_USERNAME/SAUCE_ACCESS_KEY not set."
                    )

                if sauce_region in ("eu", "eu-central-1"):
                    host = "ondemand.eu-central-1.saucelabs.com:443/wd/hub"
                elif sauce_region.startswith("apac"):
                    host = "ondemand.apac-southeast-1.saucelabs.com:443/wd/hub"
                else:
                    host = "ondemand.us-west-1.saucelabs.com:443/wd/hub"

                remote_url = f"https://{user}:{key}@{host}"

            sauce_options = {
                "build": sauce_build or "Local-Build",
                "name":  sauce_name or "Pytest Run",
                "tags":  [t.strip() for t in (sauce_tags or "").split(",") if t.strip()],
                "screenResolution": "1920x1080",
                "seleniumVersion": "4.21.0",
            }
            opts.set_capability("sauce:options", sauce_options)

            # Diagnostics (no credential leak)
            try:
                caps = getattr(opts, "capabilities", {})
                log.info("Sauce endpoint: %s", remote_url.split("@")[-1])
                log.info("Capabilities: %s", json.dumps(caps, indent=2))
            except Exception:
                pass

        else:
            # Selenium Grid or unknown cloud
            remote_url = grid_url or "http://localhost:4444/wd/hub"

        # ---- Create session
        try:
            return webdriver.Remote(command_executor=remote_url, options=opts)
        except Exception as e:
            log.error("Remote session creation failed at %s", remote_url, exc_info=True)
            raise
