import pytest

from config.enviroment import REQRES_BASE_URL, REQRES_ENV

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_base_url_is_configured():
    assert REQRES_BASE_URL.startswith("https://"), (
        f"base_url should use HTTPS for external tests. base_url={REQRES_BASE_URL}"
    )


def test_reqres_environment_is_valid():
    assert REQRES_ENV in {"prod", "dev"}, (
        f"REQRES_ENV must be 'prod' or 'dev'. Current value={REQRES_ENV}"
    )
