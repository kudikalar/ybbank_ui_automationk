# core/assertions.py
from __future__ import annotations

import re
from typing import Any, Iterable, Mapping, Sequence, Tuple, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# If you placed Waiter at core/wait.py (as in our earlier messages)
try:
    from core.wait import Waiter
except Exception:  # fallback if Waiter is elsewhere
    Waiter = None  # type: ignore

Locator = Tuple[str, str]


# ------------- Basic value assertions -------------

def assert_equals(actual: Any, expected: Any, msg: str = "") -> None:
    assert actual == expected, msg or f"Expected {expected!r}, got {actual!r}"

def assert_not_equals(a: Any, b: Any, msg: str = "") -> None:
    assert a != b, msg or f"Did not expect {b!r}, but both are equal"

def assert_true(expr: Any, msg: str = "") -> None:
    assert bool(expr) is True, msg or "Expected True, got False"

def assert_false(expr: Any, msg: str = "") -> None:
    assert bool(expr) is False, msg or "Expected False, got True"

def assert_is_none(v: Any, msg: str = "") -> None:
    assert v is None, msg or f"Expected None, got {v!r}"

def assert_is_not_none(v: Any, msg: str = "") -> None:
    assert v is not None, msg or "Expected value to be not None"

def assert_almost_equal(a: float, b: float, rel: float = 1e-6, abs_: float = 1e-9, msg: str = "") -> None:
    ok = abs(a - b) <= max(rel * max(abs(a), abs(b)), abs_)
    assert ok, msg or f"{a} !~= {b} (rel={rel}, abs={abs_})"

def assert_greater(a: Any, b: Any, msg: str = "") -> None:
    assert a > b, msg or f"Expected {a!r} > {b!r}"

def assert_greater_equal(a: Any, b: Any, msg: str = "") -> None:
    assert a >= b, msg or f"Expected {a!r} >= {b!r}"

def assert_less(a: Any, b: Any, msg: str = "") -> None:
    assert a < b, msg or f"Expected {a!r} < {b!r}"

def assert_less_equal(a: Any, b: Any, msg: str = "") -> None:
    assert a <= b, msg or f"Expected {a!r} <= {b!r}"

def assert_between(a: Any, low: Any, high: Any, inclusive: bool = True, msg: str = "") -> None:
    ok = (low <= a <= high) if inclusive else (low < a < high)
    br = "≤" if inclusive else "<"
    assert ok, msg or f"Expected {low} {br} {a} {br} {high}"

# ------------- Sequence / mapping assertions -------------

def assert_in(member: Any, container: Iterable, msg: str = "") -> None:
    assert member in container, msg or f"{member!r} not found in {container!r}"

def assert_not_in(member: Any, container: Iterable, msg: str = "") -> None:
    assert member not in container, msg or f"{member!r} unexpectedly found in {container!r}"

def assert_len(obj: Sized | Sequence | Mapping, expected: int, msg: str = "") -> None:  # type: ignore[name-defined]
    actual = len(obj)  # type: ignore[arg-type]
    assert actual == expected, msg or f"Expected len {expected}, got {actual}"

def assert_empty(obj: Iterable, msg: str = "") -> None:
    assert len(list(obj)) == 0, msg or f"Expected empty iterable, got items"

def assert_not_empty(obj: Iterable, msg: str = "") -> None:
    assert len(list(obj)) > 0, msg or "Expected non-empty iterable"

def assert_unique(seq: Sequence, msg: str = "") -> None:
    assert len(seq) == len(set(seq)), msg or "Expected all items unique"

def assert_sorted(seq: Sequence, reverse: bool = False, msg: str = "") -> None:
    assert list(seq) == sorted(seq, reverse=reverse), msg or f"Sequence not sorted (reverse={reverse})"

def assert_sets_equal(a: Iterable, b: Iterable, msg: str = "") -> None:
    sa, sb = set(a), set(b)
    assert sa == sb, msg or f"Sets differ. Missing: {sa - sb}, Extra: {sb - sa}"

def assert_list_equal_unordered(a: Sequence, b: Sequence, msg: str = "") -> None:
    from collections import Counter
    ca, cb = Counter(a), Counter(b)
    assert ca == cb, msg or f"Lists differ (multiset compare). Diff: {ca - cb} vs {cb - ca}"

def assert_dict_contains(d: Mapping, expected: Mapping, msg: str = "") -> None:
    missing = {k: v for k, v in expected.items() if k not in d or d[k] != v}
    assert not missing, msg or f"Dict missing/unequal entries: {missing}"

def assert_keys_subset(d: Mapping, keys: Iterable, msg: str = "") -> None:
    ks = set(keys)
    assert ks.issubset(d.keys()), msg or f"Missing keys: {ks - set(d.keys())}"

# ------------- String assertions -------------

def assert_startswith(s: str, prefix: str, msg: str = "") -> None:
    assert s.startswith(prefix), msg or f"Expected {s!r} to start with {prefix!r}"

def assert_endswith(s: str, suffix: str, msg: str = "") -> None:
    assert s.endswith(suffix), msg or f"Expected {s!r} to end with {suffix!r}"

def assert_contains_ci(s: str, needle: str, msg: str = "") -> None:
    assert needle.lower() in s.lower(), msg or f"'{needle}' (ci) not found in '{s}'"

def assert_regex_match(pattern: str, s: str, msg: str = "") -> None:
    assert re.fullmatch(pattern, s) is not None, msg or f"String '{s}' does not fully match /{pattern}/"

def assert_regex_search(pattern: str, s: str, msg: str = "") -> None:
    assert re.search(pattern, s) is not None, msg or f"Pattern /{pattern}/ not found in '{s}'"

# ------------- HTTP-ish helpers (if you assert on APIs) -------------

def assert_status_code(actual: int, expected: int = 200, msg: str = "") -> None:
    assert actual == expected, msg or f"Expected HTTP {expected}, got {actual}"

def assert_between_status(actual: int, low: int, high: int, msg: str = "") -> None:
    assert low <= actual <= high, msg or f"Expected {low}≤code≤{high}, got {actual}"

# ------------- Selenium/UI assertions (use Waiter if available) -------------

def assert_title_contains(driver: WebDriver, text: str, timeout: int = 10, msg: str = "") -> None:
    if Waiter:
        ok = Waiter(driver, timeout=timeout).title_contains(text)
        assert ok, msg or f"Title does not contain '{text}'. Actual: '{driver.title}'"
    else:
        assert text in driver.title, msg or f"Title does not contain '{text}'. Actual: '{driver.title}'"

def assert_url_contains(driver: WebDriver, fragment: str, timeout: int = 10, msg: str = "") -> None:
    if Waiter:
        ok = Waiter(driver, timeout=timeout).url_contains(fragment)
        assert ok, msg or f"URL does not contain '{fragment}'. Actual: '{driver.current_url}'"
    else:
        assert fragment in driver.current_url, msg or f"URL does not contain '{fragment}'. Actual: '{driver.current_url}'"

def assert_element_visible(driver: WebDriver, locator: Locator, timeout: int = 10, msg: str = "") -> WebElement:
    if not Waiter:
        raise RuntimeError("Waiter class not available for visibility wait")
    try:
        return Waiter(driver, timeout=timeout).visible(locator)
    except TimeoutException as e:
        raise AssertionError(msg or f"Element not visible: {locator}") from e

def assert_element_text(
    driver: WebDriver,
    locator: Locator,
    expected: str,
    timeout: int = 10,
    contains: bool = False,
    ignore_case: bool = True,
    strip: bool = True,
    msg: str = "",
) -> None:
    if not Waiter:
        raise RuntimeError("Waiter class not available for text wait")
    el = Waiter(driver, timeout=timeout).visible(locator)
    actual = el.text
    if strip:
        actual, expected = actual.strip(), expected.strip()
    if ignore_case:
        actual_cmp, expected_cmp = actual.lower(), expected.lower()
    else:
        actual_cmp, expected_cmp = actual, expected
    if contains:
        assert expected_cmp in actual_cmp, msg or f"Expected text to contain '{expected}', got '{actual}'"
    else:
        assert actual_cmp == expected_cmp, msg or f"Expected text '{expected}', got '{actual}'"

def assert_attribute_equals(
    driver: WebDriver,
    locator: Locator,
    attr: str,
    expected: str,
    timeout: int = 10,
    msg: str = "",
) -> None:
    if not Waiter:
        raise RuntimeError("Waiter class not available for attribute wait")
    el = Waiter(driver, timeout=timeout).present(locator)
    actual = (el.get_attribute(attr) or "").strip()
    assert actual == expected, msg or f"Expected @{attr}='{expected}', got '{actual}'"

def assert_elements_count(driver: WebDriver, locator: Locator, expected: int, timeout: int = 10, msg: str = "") -> None:
    if not Waiter:
        raise RuntimeError("Waiter class not available for count wait")
    els = Waiter(driver, timeout=timeout).present_all(locator)
    actual = len(els)
    assert actual == expected, msg or f"Expected {expected} elements for {locator}, found {actual}"
