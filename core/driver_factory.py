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


def _sauce_host(region: str) -> str:
    r = (region or "us-west-1").lower()
    if r in ("eu", "eu-central-1"):
        return "ondemand.eu-central-1.saucelabs.com/wd/hub"
    if r.startswith("apac") or r.startswith("ap-southeast-1"):
        return "ondemand.apac-southeast-1.saucelabs.com/wd/hub"
    return "ondemand.us-west-1.saucelabs.com/wd/hub"


class DriverFactory:
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
        try: driver.maximize_window()
        except Exception: pass
        return driver

    @staticmethod
    def _edge(headless: bool):
        opts = EdgeOptions()
        if headless:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(service=EdgeService(), options=opts)
        try: driver.maximize_window()
        except Exception: pass
        return driver

    @staticmethod
    def create_driver(
        browser: str = "chrome",
        headless: bool = False,
        remote: bool = False,
        platform: str = "Windows",
        cloud: Optional[str] = None,
        grid_url: Optional[str] = None,
        *,
        platform_name: str = "Windows 11",
        browser_version: str = "latest",
        sauce_build: Optional[str] = None,
        sauce_name: Optional[str] = None,
        sauce_tags: Optional[str] = "pytest",
        sauce_region: str = "us-west-1",
        sauce_tunnel: Optional[str] = None,
    ):
        # ---- env overrides (CI/local)
        env_remote = os.getenv("REMOTE_DRIVER", "").lower()
        if env_remote in ("sauce", "grid"):
            remote = True
            cloud = "saucelabs" if env_remote == "sauce" else cloud

        browser        = os.getenv("SAUCE_BROWSER", browser).lower()
        platform_name  = os.getenv("SAUCE_PLATFORM", platform_name)
        browser_version= os.getenv("SAUCE_VERSION", browser_version)
        sauce_region   = os.getenv("SAUCE_REGION", sauce_region)
        sauce_build    = os.getenv("SAUCE_BUILD", sauce_build or "GitHub Actions Build")
        sauce_name     = os.getenv("SAUCE_NAME", sauce_name or "PyTest Run")
        sauce_tags     = os.getenv("SAUCE_TAGS", sauce_tags or "pytest")
        sauce_tunnel   = os.getenv("SAUCE_TUNNEL", sauce_tunnel)

        gh_sha    = os.getenv("GITHUB_SHA")
        gh_run_id = os.getenv("GITHUB_RUN_ID")

        # ---- local?
        if not remote:
            if browser == "chrome":  return DriverFactory._chrome(headless)
            if browser == "firefox": return DriverFactory._firefox(headless)
            if browser == "edge":    return DriverFactory._edge(headless)
            raise ValueError(f"Unsupported browser: {browser}")

        # ---- options
        if browser == "chrome":
            opts = ChromeOptions()
        elif browser == "firefox":
            opts = FirefoxOptions()
        elif browser == "edge":
            opts = EdgeOptions()
        else:
            raise ValueError(f"Unsupported remote browser: {browser}")

        if headless and cloud != "saucelabs":
            if browser == "firefox": opts.headless = True
            else: opts.add_argument("--headless=new")

        opts.set_capability("platformName", platform_name)
        opts.set_capability("browserVersion", browser_version)

        # ---- Sauce Labs
        if cloud == "saucelabs":
            user = (os.environ.get("SAUCE_USERNAME") or "").strip()
            key  = (os.environ.get("SAUCE_ACCESS_KEY") or "").strip()
            if not user or not key:
                raise RuntimeError("SAUCE_USERNAME/SAUCE_ACCESS_KEY not set (and no grid_url provided).")

            # Build hub URL WITHOUT creds; auth via sauce:options
            remote_url = grid_url if (grid_url and grid_url.startswith(("http://","https://"))) \
                         else f"https://{_sauce_host(sauce_region)}"

            tags_list = [t.strip() for t in (sauce_tags or "").split(",") if t.strip()]
            sauce_options = {
                "username": user,
                "accessKey": key,
                "build": sauce_build,
                "name": sauce_name,
                "tags": tags_list,
                "screenResolution": "1920x1080",
                "seleniumVersion": "4.25.0",
                "github": {"sha": gh_sha, "runId": gh_run_id},
            }
            if sauce_tunnel:
                sauce_options["tunnelName"] = sauce_tunnel

            opts.set_capability("sauce:options", sauce_options)

            # logs (no credential leak)
            try:
                caps = getattr(opts, "capabilities", {})
                log.info("Sauce endpoint: %s", remote_url)
                log.info("Capabilities: %s", json.dumps(caps, indent=2))
            except Exception:
                pass

            try:
                return webdriver.Remote(command_executor=remote_url, options=opts)
            except Exception:
                log.error("Remote session creation failed at %s", remote_url, exc_info=True)
                raise

        # ---- Selenium Grid / other cloud
        remote_url = grid_url or "http://localhost:4444/wd/hub"
        try:
            return webdriver.Remote(command_executor=remote_url, options=opts)
        except Exception:
            log.error("Remote session creation failed at %s", remote_url, exc_info=True)
            raise
