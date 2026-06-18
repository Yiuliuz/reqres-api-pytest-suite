import os

import pytest

from clients.reqres_client import ReqresClient

from helpers.client_factory import create_reqres_client,create_reqres_manage_client

from config.enviroment import (
    can_run_live_tests,
    can_run_write_tests,
)


def pytest_collection_modifyitems(config, items):

    skip_live = pytest.mark.skip(
        reason="REQRES_API_KEY is not configured; live Reqres tests are skipped"
    )
    skip_write = pytest.mark.skip(
        reason="REQRES_MANAGE_API_KEY is not configured; write Reqres tests are skipped"
    )

    for item in items:
        if "live" in item.keywords and not can_run_live_tests():
            item.add_marker(skip_live)
        if (
            "write" in item.keywords or "destructive" in item.keywords
        ) and not can_run_write_tests():
            item.add_marker(skip_write)


@pytest.fixture(scope="session")
def reqres_client():
    return create_reqres_client()


@pytest.fixture(scope="session")
def reqres_manage_client():
    return create_reqres_manage_client()


@pytest.fixture
def valid_product_payload():
    return {
        "name": "QA Practice Product",
        "price": 9.99,
        "category":"Testing",
        "in_stock":True,
    }
