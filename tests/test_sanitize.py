from docharvester.utils import safe_filename


def test_safe_filename_strips_windows_forbidden_chars() -> None:
    assert safe_filename('a<b>c:"d/e\\\\f|g?*') == "a-b-c-d-e-f-g"


def test_safe_filename_collapses_whitespace_and_trims() -> None:
    assert safe_filename("  Hello   world  ") == "Hello world"


def test_safe_filename_has_fallback() -> None:
    assert safe_filename("   ") == "output"

