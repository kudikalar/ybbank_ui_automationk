# core/logger.py
from __future__ import annotations
import logging, sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from queue import SimpleQueue

_LOGGERS = {}
_LISTENER: QueueListener | None = None
_CONFIGURED = False

def setup_logging(
    log_dir: str | Path = "logs",
    log_file: str = "test_run.log",
    level: int = logging.INFO,
    max_bytes: int = 2 * 1024 * 1024,
    backups: int = 5,
) -> None:
    """Configure root logger once, with thread/process-safe queue + console + file."""
    global _CONFIGURED, _LISTENER
    if _CONFIGURED:
        return

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile_path = log_dir / log_file

    # Format
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(processName)s | %(threadName)s | %(name)s | %(message)s"
    )

    # Root logger uses QueueHandler (non-blocking, avoids Selenium thread contention)
    q = SimpleQueue()
    qh = QueueHandler(q)
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(qh)

    # Real handlers (console + rotating file) consume from the queue
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(level)

    fh = RotatingFileHandler(
        logfile_path, maxBytes=max_bytes, backupCount=backups, encoding="utf-8"
    )
    fh.setFormatter(fmt)
    fh.setLevel(level)

    _LISTENER = QueueListener(q, ch, fh, respect_handler_level=True)
    _LISTENER.start()

    _CONFIGURED = True


def get_logger(name: str = "framework") -> logging.Logger:
    """Return a named logger; propagates to the configured root (so no per-logger handlers)."""
    if name in _LOGGERS:
        return _LOGGERS[name]
    lg = logging.getLogger(name)
    # Important: let messages bubble to root where our handlers live
    lg.propagate = True
    _LOGGERS[name] = lg
    return lg


def shutdown_logging() -> None:
    """Flush & stop queue listener; close handlers cleanly (pytest session end)."""
    global _LISTENER, _CONFIGURED
    try:
        if _LISTENER:
            _LISTENER.stop()
            _LISTENER = None
    finally:
        logging.shutdown()
        _CONFIGURED = False
