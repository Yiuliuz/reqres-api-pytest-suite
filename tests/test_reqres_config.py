import pytest


pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_base_url_is_configured(base_url):
    assert base_url.startswith("https://"), (
        f"base_url should use HTTPS for external tests. base_url={base_url}"
    )


def test_reqres_environment_is_valid(reqres_environment):
    assert reqres_environment in {"prod", "dev"}, (
        f"REQRES_ENV must be 'prod' or 'dev'. Current value={reqres_environment}"
    )
