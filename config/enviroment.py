import os

REQRES_API_KEY = os.getenv("REQRES_API_KEY")
REQRES_MANAGE_API_KEY = os.getenv("REQRES_MANAGE_API_KEY")
REQRES_ENV = os.getenv(
    "REQRES_ENV",
    "prod")
REQRES_BASE_URL = os.getenv(
    "REQRES_BASE_URL",
    "https://reqres.in"
)


def can_run_live_tests():
    return bool(REQRES_API_KEY or REQRES_MANAGE_API_KEY)


def can_run_write_tests():
    return bool(REQRES_MANAGE_API_KEY)