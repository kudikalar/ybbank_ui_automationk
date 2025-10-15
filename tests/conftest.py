import os
import pytest
from core.driver_factory import DriverFactory
from utils.config_reader import Config
from core.logger import setup_logging, shutdown_logging, get_logger
from config.config import DEFAULT_ENV

_cfg = Config()

def pytest_addoption(parser):
    parser.addoption("--browser",   action="store",  default=_cfg.browser, help="chrome|firefox|edge")
    parser.addoption("--platform",  action="store",  default=_cfg.platform)
    parser.addoption("--cloud",     action="store",  default=_cfg.cloud or "")
    parser.addoption("--grid-url",  action="store",  default=_cfg.grid_url or "")
    parser.addoption("--base-url",  action="store",  default=getattr(_cfg, "base_url", ""))
    parser.addoption("--env",       action="store",  default=DEFAULT_ENV, help="Environment alias or full URL")
    parser.addoption("--remote",    action="store_true", default=bool(getattr(_cfg, "remote", False)))
    parser.addoption("--headless",  action="store_true", default=bool(getattr(_cfg, "headless", False)))
    parser.addoption("--sauce-region", action="store",
                     choices=["us","eu","apac","us-west-1","eu-central-1","apac-southeast-1"],
                     default=os.getenv("SAUCE_REGION", "us"))

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

# SINGLE env fixture (do not duplicate)
@pytest.fixture
def env(pytestconfig):
    # Let PageObjects resolve alias/full URL.
    # Prefer --env if provided; otherwise fall back to --base-url.
    opt_env = pytestconfig.getoption("env")
    if opt_env:
        return opt_env
    return pytestconfig.getoption("base_url")

def _on_sauce(driver) -> bool:
    caps = getattr(driver, "capabilities", {}) or {}
    # When running on Sauce, capabilities usually include 'sauce:options' or 'sauce:jobName'
    return any(k.startswith("sauce:") for k in caps.keys())

@pytest.fixture(autouse=True, scope="session")
def driver(request):
    log = get_logger("driver")
    browser   = request.config.getoption("browser")
    platform  = request.config.getoption("platform")
    cloud     = (request.config.getoption("cloud") or "").strip() or None
    grid_url  = (request.config.getoption("grid_url") or "").strip() or None
    remote    = bool(request.config.getoption("remote"))
    headless  = bool(request.config.getoption("headless"))

    platform_name   = "Windows 11"
    browser_version = "latest"
    sauce_build     = "RegisterSuite-1"
    sauce_name      = request.node.name
    sauce_tags      = "pytest,demowebshop,register"
    sauce_region    = request.config.getoption("sauce_region")

    if remote and (cloud == "saucelabs") and (not grid_url):
        if not os.getenv("SAUCE_USERNAME") or not os.getenv("SAUCE_ACCESS_KEY"):
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

        # Mark job result on Sauce only
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
