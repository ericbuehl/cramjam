import platform
import sys
import sysconfig

import pytest

# DEBUG ONLY: block the hypothesis patch-suggestion module so its import in
# _hypothesis_pytestplugin.pytest_runtest_makereport raises ImportError (which
# the plugin handles) instead of the SyntaxError-INTERNALERROR seen in CI,
# letting pytest print the real FAILURES section.
sys.modules["hypothesis.extra._patching"] = None


@pytest.fixture(scope="session")
def is_pypy():
    impl = platform.python_implementation()
    return impl.lower() == "pypy"

@pytest.fixture(scope="session")
def is_free_threaded():
    return bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


def pytest_configure(config):
    config.addinivalue_line("markers", "skip_pypy: skip this test on PyPy")


def pytest_runtest_setup(item):
    if "skip_pypy" in item.keywords and platform.python_implementation() == "PyPy":
        pytest.skip("skipped on PyPy")
