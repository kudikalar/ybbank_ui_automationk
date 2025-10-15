# core/driver_factory.py
import os
import json
import base64
import logging
from typing import Optional
from urllib import request as _urlreq
from urllib.error import HTTPError, URLError

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

log = logging.getLogger("DriverFactory")


# --- Sauce helpers ------------------------------------------------------------

_SAUCE_DCS = ("us-west-1", "eu-central-1", "apac-southeast-1")

def _sauce_host(region: str) -> str:
    r = (region or "us-west-1").lower()
    if r in ("eu", "eu-central-1"):
        return "ondemand.eu-central-1.saucelabs.com/wd/hub"
    if r.startswith(("apac", "ap-southeast-1", "apac-southeast-1")):
        return "ondemand.apac-southeast-1.saucelabs.com/wd/hub"
    return "ondemand.us-west-1.saucelabs.com/wd/hub"


def _norm(val, *, lower=True, default=None):
    if val is None:
        return default
    s = str(val).strip()
    return s.lower() if lower else s

def _probe_sauce_dc(dc: str, user: str, key: str, timeout: int = 5) -> int:
    """
    Returns HTTP status from Sauce REST API for the given DC.
    200 -> creds valid in this DC; 401/403 -> invalid (or wrong DC); 0 -> network error.
    """
    url = f"https://api.{dc}.saucelabs.com/v1/users/{user}"
    req = _urlreq.Request(url)
    token = base64.b64encode(f"{user}:{key}".encode("utf-8")).decode("utf-8")
    req.add_header("Authorization", f"Basic {token}")
    try:
        with _urlreq.urlopen(req, timeout=timeout) as resp:
            return getattr(resp, "status", 200)
    except HTTPError as e:
        return e.code
    except URLError:
        return 0
    except Exception:
        return 0


def _pick_sauce_region(preferred: str, user: str, key: str) -> str:
    """
    Try preferred first; if not 200, fall back across known DCs.
    """
    order = []
    p = (preferred or "").strip().lower()
    if p:
        # normalize short aliases
        if p in ("us", ""):
            p = "us-west-1"
        elif p == "eu":
            p = "eu-central-1"
        elif p == "apac" or p == "ap-southeast-1":
            p = "apac-southeast-1"
        order.append(p)
    # add remaining DCs to try
    for dc in _SAUCE_DCS:
        if dc not in order:
            order.append(dc)

    for dc in order:
        code = _probe_sauce_dc(dc, user, key)
        log.info("Sauce DC probe %s -> HTTP %s", dc, code)
        if code == 200:
            return dc

    # if all else fails, keep preferred (or US West) and let session error surface
    return p or "us-west-1"


# --- Driver factory -----------------------------------------------------------

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
        env_remote = _norm(os.getenv("REMOTE_DRIVER"), lower=True, default="")
        if env_remote in ("sauce", "grid"):
            remote = True
            if env_remote == "sauce":
                cloud = "saucelabs"

        browser         = _norm(os.getenv("SAUCE_BROWSER", browser), lower=True) or "chrome"
        platform_name   = _norm(os.getenv("SAUCE_PLATFORM", platform_name), lower=False) or "Windows 11"
        browser_version = _norm(os.getenv("SAUCE_VERSION", browser_version), lower=False) or "latest"
        sauce_region    = _norm(os.getenv("SAUCE_REGION", sauce_region), lower=True) or "us-west-1"
        sauce_build     = _norm(os.getenv("SAUCE_BUILD", sauce_build or "GitHub Actions Build"), lower=False)
        sauce_name      = _norm(os.getenv("SAUCE_NAME", sauce_name or "PyTest Run"), lower=False)
        sauce_tags      = _norm(os.getenv("SAUCE_TAGS", sauce_tags or "pytest"), lower=False)
        sauce_tunnel    = _norm(os.getenv("SAUCE_TUNNEL", sauce_tunnel), lower=False)
        cloud           = _norm(cloud, lower=True)

        if not remote and cloud == "saucelabs":
            remote = True

        # Normalize browser aliases
        b = browser
        if b in ("gc", "google-chrome"):
            b = "chrome"
        elif b in ("ff",):
            b = "firefox"
        elif b in ("msedge",):
            b = "edge"

        # ---- local
        if not remote:
            if b == "chrome":  return DriverFactory._chrome(headless)
            if b == "firefox": return DriverFactory._firefox(headless)
            if b == "edge":    return DriverFactory._edge(headless)
            raise ValueError(f"Unsupported browser: {browser!r}")

        # ---- remote options
        if b == "chrome":
            opts = ChromeOptions()
        elif b == "firefox":
            opts = FirefoxOptions()
        elif b == "edge":
            opts = EdgeOptions()
        else:
            raise ValueError(f"Unsupported remote browser: {browser!r}")

        # Headless is ignored by Sauce but kept for generic grids
        if headless and cloud != "saucelabs":
            if b == "firefox":
                opts.headless = True
            else:
                opts.add_argument("--headless=new")

        # W3C caps
        opts.set_capability("platformName", platform_name)
        opts.set_capability("browserVersion", browser_version)

        # ---- Sauce Labs

        if cloud == "saucelabs":
            user = _norm(os.environ.get("SAUCE_USERNAME"), lower=False)
            key = _norm(os.environ.get("SAUCE_ACCESS_KEY"), lower=False)
            if not user or not key:
                raise RuntimeError("SAUCE_USERNAME/SAUCE_ACCESS_KEY not set (and no grid_url provided).")

            # normalize incoming hint; we’ll still try others on 401
            def _norm_dc(x: str) -> str:
                x = (x or "").strip().lower()
                if x in ("", "us", "us-west-1"): return "us-west-1"
                if x in ("eu", "eu-central-1"):  return "eu-central-1"
                if x in ("apac", "ap-southeast-1", "apac-southeast-1"): return "apac-southeast-1"
                return x

            dc_hint = _norm_dc(sauce_region)
            dc_order = [dc_hint] + [dc for dc in ("us-west-1", "eu-central-1", "apac-southeast-1") if dc != dc_hint]

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

            last_err = None
            for dc in dc_order:
                # Build both forms of endpoint. We’ll prefer the one with Basic auth in URL.
                host_path = _sauce_host(dc)  # e.g. ondemand.eu-central-1.saucelabs.com/wd/hub
                remote_url_auth = f"https://{user}:{key}@{host_path}"
                remote_url_naked = f"https://{host_path}"

                # Don’t leak secrets in logs
                log.info("Trying Sauce data center: %s", dc)
                try:
                    # Use the auth-in-URL endpoint first to avoid 401s caused by ignored sauce:options
                    log.info("Sauce endpoint: https://%s", host_path)
                    # Optional: print capabilities without secrets
                    try:
                        caps = getattr(opts, "capabilities", {}) or {}
                        cap_redacted = json.loads(json.dumps(caps))
                        if "sauce:options" in cap_redacted:
                            cap_redacted["sauce:options"]["username"] = "***"
                            cap_redacted["sauce:options"]["accessKey"] = "***"
                        log.info("Capabilities: %s", json.dumps(cap_redacted, indent=2))
                    except Exception:
                        pass

                    return webdriver.Remote(command_executor=remote_url_auth, options=opts)
                except Exception as e:
                    # If the failure smells like auth (401), try the next DC; otherwise save and break
                    msg = str(e)
                    last_err = e
                    if "Authorization Required" in msg or "401" in msg:
                        log.warning("Auth failed on %s, will try next DC if available.", dc)
                        continue
                    else:
                        log.error("Remote session creation failed at https://%s", host_path, exc_info=True)
                        break

            # If we’re here, all DC attempts failed
            raise last_err or RuntimeError("Could not create Sauce session in any data center.")
        return None