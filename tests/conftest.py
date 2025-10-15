import os
import pytest
from pathlib import Path
from core.driver_factory import DriverFactory
from utils.config_reader import Config
from core.logger import setup_logging, shutdown_logging, get_logger
from config.config import DEFAULT_ENV

# --- Load .env early (local runs) ---
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except Exception:
    pass

_cfg = Config()

def _region_normalize(val: str) -> str:
    v = (val or "").lower().strip()
    if v in ("us", "us-west-1", ""):
        return "us-west-1"
    if v in ("eu", "eu-central-1"):
        return "eu-central-1"
    if v in ("apac", "apac-southeast-1", "ap-southeast-1"):
        return "apac-southeast-1"
    return v

def _bool_env(name: str, fallback: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return fallback
    return str(v).strip().lower() in ("1", "true", "yes", "y", "on")

def pytest_addoption(parser):
    parser.addoption("--browser",   action="store",  default=(os.getenv("SAUCE_BROWSER") or _cfg.browser))
    parser.addoption("--platform",  action="store",  default=_cfg.platform)
    parser.addoption("--cloud",     action="store",  default=(os.getenv("CLOUD") or (_cfg.cloud or "")))
    parser.addoption("--grid-url",  action="store",  default=(os.getenv("GRID_URL") or (_cfg.grid_url or "")))
    parser.addoption("--base-url",  action="store",  default=getattr(_cfg, "base_url", ""))
    parser.addoption("--env",       action="store",  default=DEFAULT_ENV, help="Environment alias or full URL")
    parser.addoption("--remote",    action="store_true",
                     default=(str(os.getenv("REMOTE_DRIVER", "")).strip().lower() in ("sauce", "grid")
                              or bool(getattr(_cfg, "remote", False))))
    parser.addoption("--headless",  action="store_true", default=_bool_env("HEADLESS", getattr(_cfg, "headless", False)))
    parser.addoption("--sauce-region", action="store",
                     choices=["us","eu","apac","us-west-1","eu-central-1","apac-southeast-1"],
                     default=_region_normalize(os.getenv("SAUCE_REGION", "us")))

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    setup_logging(log_dir="logs", log_file="test_run.log")

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    shutdown_logging()

@pytest.fixture(autouse=True, scope="session")
def _log_banner():
    log = get_logger("pytest")
    log.info("=== Pytest session started ===")
    yield
    log.info("=== Pytest session finished ===")

@pytest.fixture
def env(pytestconfig):
    opt_env = pytestconfig.getoption("env")
    if opt_env:
        return opt_env
    return pytestconfig.getoption("base_url")

def _on_sauce(driver) -> bool:
    caps = getattr(driver, "capabilities", {}) or {}
    # presence of top-level 'sauce:options' indicates Sauce run
    return any(k.startswith("sauce:") for k in caps.keys())

@pytest.fixture
def driver(request):
    log = get_logger("driver")
    browser  = str(request.config.getoption("browser") or "").strip().lower()
    platform = str(request.config.getoption("platform") or "").strip()
    cloud    = str(request.config.getoption("cloud") or "").strip().lower() or None
    grid_url = str(request.config.getoption("grid_url") or "").strip() or None
    remote   = bool(request.config.getoption("remote"))
    headless = bool(request.config.getoption("headless"))

    # Defaults (may be overridden inside DriverFactory via env)
    platform_name   = "Windows 11"
    browser_version = "latest"
    sauce_build     = os.getenv("SAUCE_BUILD", "RegisterSuite-1")
    sauce_name      = request.node.name
    sauce_tags      = os.getenv("SAUCE_TAGS", "pytest,demowebshop,register")
    sauce_region    = _region_normalize(request.config.getoption("sauce_region"))

    # If REMOTE_DRIVER=sauce but --cloud not set, default to saucelabs
    if remote and not cloud and str(os.getenv("REMOTE_DRIVER","")).strip().lower() == "sauce":
        cloud = "saucelabs"

    if remote and (cloud == "saucelabs") and (not grid_url):
        if not (os.getenv("SAUCE_USERNAME") and os.getenv("SAUCE_ACCESS_KEY")):
            pytest.skip("SAUCE_USERNAME/SAUCE_ACCESS_KEY not set and no --grid-url provided; skipping Sauce run.")

    drv = None
    try:
        drv = DriverFactory.create_driver(
            browser=browser,
            headless=headless,
            remote=remote,
            platform=platform,
            cloud=cloud,
            grid_url=grid_url,
            platform_name=platform_name,
            browser_version=browser_version,
            sauce_build=sauce_build,
            sauce_name=sauce_name,
            sauce_tags=sauce_tags,
            sauce_region=sauce_region,
        )
        drv.implicitly_wait(0)
        yield drv

        # Mark job result on Sauce
        try:
            if _on_sauce(drv):
                outcome = "passed"
                rep = getattr(request.node, "rep_call", None)
                if rep and rep.failed:
                    outcome = "failed"
                drv.execute_script(f"sauce:job-result={outcome}")
        except Exception as e:
            log.error(f"Could not set Sauce job result: {e}", exc_info=True)
    finally:
        try:
            if drv:
                drv.quit()
        except Exception as e:
            log.error(f"driver.quit() failed: {e}", exc_info=True)

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "rep_call", rep)
