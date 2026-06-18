import os

import pytest

from clients.reqres_client import ReqresClient

from helpers.client_factory import create_reqres_client,create_reqres_manage_client
from helpers.api_health import ensure_api_available

from config.enviroment import (
    can_run_live_tests,
    can_run_write_tests,
)

from pytest import StashKey

REQRES_REQUIRES_API = StashKey[bool]()


def pytest_collection_modifyitems(config, items):

    requires_api = any(
    (
        ("live" in item.keywords and can_run_live_tests())
        or (
        ("write" in item.keywords or "destructive" in item.keywords)
        and can_run_write_tests()
        )
    )
    for item in items
)

    config.stash[REQRES_REQUIRES_API] = requires_api

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


def pytest_runtestloop(session):
    requires_api = session.config.stash.get(
        REQRES_REQUIRES_API,
        False,
    )

    if not requires_api:
        return

    client = create_reqres_client()

    try:
        ensure_api_available(client)
    except RuntimeError as e:
        pytest.exit(
            f"\nAPI precondition failed.\n{e}",
            returncode=1,
        )

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
