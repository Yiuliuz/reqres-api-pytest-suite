import pytest

from schemas.product_schema import assert_product_contract


pytestmark = [pytest.mark.api, pytest.mark.live]


@pytest.mark.read_only
@pytest.mark.smoke
@pytest.mark.contract
def test_list_products_returns_200_and_records_list(reqres_client):
    response = reqres_client.get_products()

    assert response.status_code == 200, (
        f"GET products should return 200. "
        f"Status={response.status_code}, body={response.text}"
    )

    body = response.json()

    assert "data" in body, f"Response should include 'data'. Body={body}"
    assert isinstance(body["data"], list), (
        f"The data field should be a list. Body={body}"
    )


@pytest.mark.read_only
@pytest.mark.regression
@pytest.mark.contract
def test_products_match_basic_contract(reqres_client):
    response = reqres_client.get_products()

    assert response.status_code == 200, (
        f"GET products failed before contract validation. "
        f"Status={response.status_code}, body={response.text}"
    )

    products = response.json()["data"]

    assert products, "The products collection should contain sample data"

    for product in products:
        assert_product_contract(product)


@pytest.mark.regression
@pytest.mark.write
@pytest.mark.destructive
def test_create_product_returns_success_status(
    reqres_manage_client,
    valid_product_payload,
):
    response = reqres_manage_client.create_product(**valid_product_payload)

    assert response.status_code in {200, 201}, (
        f"Create product should return 200 or 201. "
        f"Status={response.status_code}, body={response.text}"
    )

    body = response.json()["data"]

    assert "data" in body, f"Response should include data. Body={body}"
    assert body["data"]["name"] == valid_product_payload["name"], (
        f"Created name does not match. Expected={valid_product_payload['name']}, "
        f"actual={body}"
    )
