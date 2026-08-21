import contextlib
import platform
import sysconfig

import pytest

# Eagerly import hypothesis modules that are otherwise imported lazily in the
# middle of the test session. pytest assertion-rewrites hypothesis (it ships a
# pytest plugin), and on GitHub Actions runners the mid-run ast.parse of these
# lazy imports intermittently fails with a bogus SyntaxError, failing whichever
# test triggered the import and crashing pytest with INTERNALERROR while
# reporting. Importing them here means they are parsed once, up front.
import hypothesis.internal.conjecture.optimiser  # noqa: F401

with contextlib.suppress(ImportError):  # requires the optional libcst
    import hypothesis.extra._patching  # noqa: F401


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
