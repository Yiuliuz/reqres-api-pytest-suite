import pytest

from helpers.performance import assert_response_time

pytestmark = [pytest.mark.api, pytest.mark.live]


@pytest.mark.smoke
@pytest.mark.read_only
def test_list_products_response_time(reqres_client):
    #GIVEN a configured api client

    #WHEN get a list products
    response = reqres_client.get_products()

    #THEN response time is under 2 seconds
    assert_response_time(response)
