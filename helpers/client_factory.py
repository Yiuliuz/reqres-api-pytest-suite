from clients.reqres_client import ReqresClient
from config.enviroment import (
    REQRES_API_KEY,
    REQRES_MANAGE_API_KEY,
    REQRES_BASE_URL,
    REQRES_ENV,
)


def create_reqres_client():
    if not REQRES_API_KEY and not REQRES_MANAGE_API_KEY:
        raise RuntimeError(
            "No API key configured."
        )

    return ReqresClient(
        base_url=REQRES_BASE_URL,
        api_key=REQRES_API_KEY or REQRES_MANAGE_API_KEY,
        environment=REQRES_ENV,
    )


def create_reqres_manage_client():
    if not REQRES_MANAGE_API_KEY:
        raise RuntimeError(
            "REQRES_MANAGE_API_KEY is not configured."
        )

    return ReqresClient(
        base_url=REQRES_BASE_URL,
        api_key=REQRES_MANAGE_API_KEY,
        environment=REQRES_ENV,
    )