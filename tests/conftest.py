import os

import pytest

from clients.reqres_client import ReqresClient


def pytest_collection_modifyitems(config, items):
    if os.getenv("REQRES_API_KEY"):
        return

    skip_live = pytest.mark.skip(
        reason="REQRES_API_KEY is not configured; live Reqres tests are skipped"
    )

    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("REQRES_BASE_URL", "https://reqres.in")


@pytest.fixture(scope="session")
def reqres_environment():
    return os.getenv("REQRES_ENV", "prod")


@pytest.fixture(scope="session")
def api_key():
    return os.getenv("REQRES_API_KEY")


@pytest.fixture(scope="session")
def reqres_client(base_url, api_key, reqres_environment):
    if not api_key:
        pytest.skip("REQRES_API_KEY is not configured")

    return ReqresClient(
        base_url=base_url,
        api_key=api_key,
        environment=reqres_environment,
    )


@pytest.fixture
def valid_product_payload():
    return {
        "name": "QA Practice Product",
        "price": 9.99,
    }
