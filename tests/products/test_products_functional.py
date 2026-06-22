import pytest

from helpers.header_assertions import assert_common_headers
from helpers.cleanup_helpers import cleanup_product_if_created
from helpers.product_assertions import assert_product_matches_payload

pytestmark = [pytest.mark.api, pytest.mark.live]


@pytest.mark.read_only
@pytest.mark.smoke
@pytest.mark.contract
def test_list_products_returns_200_and_records_list(reqres_client):
    #GIVEN a configured api client.
    
    #WHEN get a list of products
    response = reqres_client.get_products()

    #THEN response status code is positive
    assert response.status_code == 200, (
        f"GET products should return 200. "
        f"Status={response.status_code}, body={response.text}")
    #AND common HTTP headers are present
    assert_common_headers(response)
    #AND there is data in the body
    body = response.json()
    assert "data" in body, f"Response should include 'data'. Body={body}"
    #AND data is in list type
    assert isinstance(body["data"], list), (
        f"The data field should be a list. Body={body}"
    )


@pytest.mark.regression
@pytest.mark.destructive
def test_create_product_returns_success_status(
    reqres_manage_client,
    valid_product_payload,
):
    #GIVEN a configured manage api client.
    #AND a valid product payload

    #WHEN manage api client creates a valid product
    response = reqres_manage_client.create_product(valid_product_payload)

    try:
        #THEN response status code is positive
        assert response.status_code in {200, 201}, (
            f"Create product should return 200 or 201. "
            f"Status={response.status_code}, body={response.text}")
        #AND response includes data
        body = response.json()["data"]
        assert "data" in body, f"Response should include data. Body={body}"
        #AND product name match
        assert body["data"]["name"] == valid_product_payload["name"], (
            f"Created name does not match. Expected={valid_product_payload['name']}, "
            f"actual={body}"
        )
    finally:
        cleanup_product_if_created(reqres_manage_client,response)



@pytest.mark.regression
@pytest.mark.destructive
def test_update_product_returns_success_and_persists_changes(
        reqres_manage_client,
        valid_product_payload,
):
    #GIVEN a configured manage api client
    #AND a valid product payload

    # WHEN manage api client creates a product
    create_response = reqres_manage_client.create_product(
        valid_product_payload
    )
    try:
        # THEN product is created
        assert create_response.status_code in {200, 201}, (
            f"Create product should return 200 or 201. "
            f"Status={create_response.status_code}, "
            f"Body={create_response.text}"
        )
        # AND the created product has a valid id
        product_id = create_response.json()["data"]["id"]
        # AND configure a new product payload
        payload=valid_product_payload.copy()
        payload["name"]="New Testing Name"
        payload["price"]=20
        payload["category"]="New Testing Category"
        payload["in_stock"]=False

        # WHEN update product by id
        put_response=reqres_manage_client.update_product(product_id,payload)

        #THEN response status code is positive
        assert put_response.status_code == 200, (
            f"Update product should return 200"
            f"Status={put_response.status_code}"
            f"Body={put_response.text}"
        )
        #AND the changes persits
        get_response=reqres_manage_client.get_product(product_id)
        get_body=get_response.json()["data"]["data"]
        assert_product_matches_payload(get_body,payload)
    finally:
        cleanup_product_if_created(reqres_manage_client, create_response)



@pytest.mark.regression
@pytest.mark.destructive
def test_delete_product_returns_204_and_removes_product(
    reqres_manage_client,
    valid_product_payload,
):
    # GIVEN a configured manage api client
    # AND a valid product payload

    # WHEN manage api client creates a product
    create_response = reqres_manage_client.create_product(
        valid_product_payload
    )

    # THEN product is created
    assert create_response.status_code in {200, 201}, (
        f"Create product should return 200 or 201. "
        f"Status={create_response.status_code}, "
        f"Body={create_response.text}"
    )

    # AND the created product has a valid id
    product_id = create_response.json()["data"]["id"]

    # WHEN the product is deleted
    delete_response = reqres_manage_client.delete_product(
        product_id
    )

    # THEN response status code is positive
    assert delete_response.status_code == 204, (
        f"Delete product should return 204. "
        f"Status={delete_response.status_code}"
    )

    # AND the product no longer exists
    get_response = reqres_manage_client.get_product(
        product_id
    )

    assert get_response.status_code == 404, (
        f"Deleted product should not be found. "
        f"Status={get_response.status_code}"
    )
