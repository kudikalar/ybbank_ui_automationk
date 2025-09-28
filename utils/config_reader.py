# core/config.py
from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union

from dotenv import load_dotenv


def _to_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}

def _to_int(v: Any, default: int) -> int:
    try:
        return int(str(v).strip())
    except Exception:
        return default

def _to_float(v: Any, default: float) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default

def _to_list(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x).strip() for x in v]
    # comma/space separated
    raw = str(v).replace("\n", ",").replace(";", ",")
    return [x.strip() for x in raw.split(",") if x.strip()]


class Config:
    """
    Unified config loader.
    Priority: defaults < JSON file < .env / os.environ.
    """

    def __init__(
        self,
        path: Union[str, Path] = None,
        env_file: Optional[Union[str, Path]] = ".env",
    ):
        if env_file:
            # loads from project root if present (no error if missing)
            load_dotenv(dotenv_path=env_file if Path(env_file).exists() else None)

        # allow CONFIG_PATH to override
        path = path or os.getenv("CONFIG_PATH", "config/config.json")
        self._path = Path(path)

        # ------- defaults (safe to extend) -------
        self._data: Dict[str, Any] = {
            "base_url": "",
            "browser": "chrome",          # chrome|firefox|edge
            "headless": False,
            "remote": False,
            "platform": "Windows",        # Windows|macOS|Linux
            "cloud": None,                # saucelabs|browserstack|None
            "grid_url": None,

            # timeouts / waits
            "timeout": 15,                # explicit wait seconds
            "poll": 0.3,                  # polling frequency

            # paths & logging
            "screenshots_dir": "screenshots",
            "downloads_dir": "downloads",
            "log_level": "INFO",

            # tags/filtering (if you use them)
            "markers": [],                # e.g., ["smoke","regression"]

            # Secrets (if present in env they’ll be filled below)
            "sauce": {"username": None, "access_key": None},
            "browserstack": {"username": None, "access_key": None},
        }

        # ------- JSON file (optional) -------
        if self._path.exists():
            with self._path.open("r", encoding="utf-8") as f:
                try:
                    file_data = json.load(f) or {}
                    if not isinstance(file_data, dict):
                        raise ValueError("config JSON must be an object")
                    self._data.update(file_data)
                except json.JSONDecodeError as e:
                    raise RuntimeError(f"Invalid JSON in {self._path}: {e}") from e

        # Whole-JSON override via env (optional)
        cfg_json = os.getenv("CONFIG_JSON")
        if cfg_json:
            try:
                env_data = json.loads(cfg_json)
                if isinstance(env_data, dict):
                    self._data.update(env_data)
            except Exception:
                pass  # ignore malformed CONFIG_JSON

        # ------- env overrides (type-aware) -------
        self._data["base_url"] = os.getenv("BASE_URL", self._data.get("base_url"))
        self._data["browser"] = os.getenv("BROWSER", self._data.get("browser"))
        self._data["headless"] = _to_bool(os.getenv("HEADLESS", self._data.get("headless")))
        self._data["remote"] = _to_bool(os.getenv("REMOTE", self._data.get("remote")))
        self._data["platform"] = os.getenv("PLATFORM", self._data.get("platform"))
        self._data["cloud"] = os.getenv("CLOUD", self._data.get("cloud"))
        self._data["grid_url"] = os.getenv("GRID_URL", self._data.get("grid_url"))

        self._data["timeout"] = _to_int(os.getenv("TIMEOUT", self._data.get("timeout")), self._data["timeout"])
        self._data["poll"] = _to_float(os.getenv("POLL", self._data.get("poll")), self._data["poll"])

        self._data["screenshots_dir"] = os.getenv("SCREENSHOTS_DIR", self._data.get("screenshots_dir"))
        self._data["downloads_dir"] = os.getenv("DOWNLOADS_DIR", self._data.get("downloads_dir"))
        self._data["log_level"] = os.getenv("LOG_LEVEL", self._data.get("log_level"))
        self._data["markers"] = _to_list(os.getenv("MARKERS", self._data.get("markers")))

        # secrets (picked from env if available)
        self._data["sauce"]["username"] = os.getenv("SAUCE_USERNAME", self._data["sauce"].get("username"))
        self._data["sauce"]["access_key"] = os.getenv("SAUCE_ACCESS_KEY", self._data["sauce"].get("access_key"))
        self._data["browserstack"]["username"] = os.getenv("BROWSERSTACK_USERNAME", self._data["browserstack"].get("username"))
        self._data["browserstack"]["access_key"] = os.getenv("BROWSERSTACK_ACCESS_KEY", self._data["browserstack"].get("access_key"))

        # normalize a couple values
        if self._data["cloud"]:
            self._data["cloud"] = str(self._data["cloud"]).lower()
        if self._data["browser"]:
            self._data["browser"] = str(self._data["browser"]).lower()

    # -------- public helpers --------
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def write_back(self, target: Optional[Union[str, Path]] = None) -> None:
        """Persist current config to JSON (handy after programmatic changes)."""
        out = Path(target) if target else self._path
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    # typed getters (optional sugar)
    @property
    def base_url(self) -> str: return self._data["base_url"]
    @property
    def browser(self) -> str: return self._data["browser"]
    @property
    def headless(self) -> bool: return bool(self._data["headless"])
    @property
    def remote(self) -> bool: return bool(self._data["remote"])
    @property
    def platform(self) -> str: return self._data["platform"]
    @property
    def cloud(self) -> Optional[str]: return self._data["cloud"]
    @property
    def grid_url(self) -> Optional[str]: return self._data["grid_url"]
    @property
    def timeout(self) -> int: return int(self._data["timeout"])
    @property
    def poll(self) -> float: return float(self._data["poll"])
    @property
    def sauce(self) -> Dict[str, Optional[str]]: return self._data["sauce"]
    @property
    def browserstack(self) -> Dict[str, Optional[str]]: return self._data["browserstack"]
