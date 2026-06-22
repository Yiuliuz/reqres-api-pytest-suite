import pytest

from schemas.product_schema import assert_product_contract , assert_product_schema

pytestmark = [pytest.mark.api, pytest.mark.live]


@pytest.mark.read_only
@pytest.mark.regression
@pytest.mark.contract
def test_products_match_basic_contract(reqres_client):
    #GIVEN a configured api client.

    #WHEN get list of products
    response = reqres_client.get_products()

    #THEN response status code is positive.
    assert response.status_code == 200, (
        f"GET products failed before contract validation. "
        f"Status={response.status_code}, body={response.text}")
    #AND There is products
    products = response.json()["data"]
    assert products, "The products collection should contain sample data"
    #AND product contract is correct
    for product in products:
        assert_product_contract(product)
        assert_product_schema(product)
