import pytest

from schemas.product_schema import assert_product_contract


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
    #AND there is data in the body
    body = response.json()
    assert "data" in body, f"Response should include 'data'. Body={body}"
    #AND data is in list type
    assert isinstance(body["data"], list), (
        f"The data field should be a list. Body={body}"
    )


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


@pytest.mark.regression
@pytest.mark.write
@pytest.mark.destructive
def test_create_product_returns_success_status(
    reqres_manage_client,
    valid_product_payload,
):
    #GIVEN a configured manage api client.
    #AND a valid product payload

    #WHEN manage api client creates a valid product
    response = reqres_manage_client.create_product(**valid_product_payload)

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


@pytest.mark.write
@pytest.mark.contract
@pytest.mark.parametrize(
    "field, value",
    [
        pytest.param("name","",id="empty name"),
        pytest.param("price","",id="empty price"),
        pytest.param("category","",id="empty category"),
        pytest.param("in_stock","",id="empty in_stock")
    ],
)
def test_create_product_with_empty_field_returns_error_status(
    reqres_manage_client,
    valid_product_payload,
    field,
    value
):
    # GIVEN a configured manage api client
    # AND a valid product payload
    # AND parametrized new field and value
    # AND a new configured payload
    payload=valid_product_payload.copy()
    payload[field]=value 
    
    # WHEN creates a product with new payload
    response = reqres_manage_client.create_product(**payload)

    #THEN response status code is negative
    assert response.status_code == 400, (
        f"Create product with empty value in {field} field should return 400, it returns {response.status_code} "
    )


@pytest.mark.write
@pytest.mark.contract
@pytest.mark.parametrize(
    "field , type_try",
    [
        pytest.param("name",123,id="int type name"),
        pytest.param("name",True,id="list type name"),
        pytest.param("name",[],id="set type name"),
        pytest.param("name",{},id="dict type name"),
        
        pytest.param("price","abc",id="str type price"),
        pytest.param("price",True,id="list type price"),
        pytest.param("price",[],id="set type price"),
        pytest.param("price",{},id="dict type price")
    ],
)
def test_create_product_with_invalid_type_field_returns_error_status(
    reqres_manage_client,
    valid_product_payload,
    field,
    type_try
):
    # GIVEN a configured manage api client
    # AND a valid product payload
    # AND parametrized new field and type
    # AND a new configured payload
    payload=valid_product_payload.copy()
    payload[field]=type_try
    
    # WHEN create a product with new payload
    response = reqres_manage_client.create_product(**payload)
    
    #THEN response status code is negative
    assert response.status_code == 400, (
        f"Create product {type(type_try)} {field} should return 400, it returns {response.status_code}"
    )


@pytest.mark.write
@pytest.mark.contract
@pytest.mark.parametrize(
    "field",
    [
        pytest.param("name"),
        pytest.param("price"),
        pytest.param("category"),
        pytest.param("in_stock")
    ]
)
def test_create_product_with_missing_field_returns_error_status(
    reqres_manage_client,
    valid_product_payload,
    field
):
    # GIVEN a configured manage api client
    # AND a valid product payload
    # AND parametrized new field
    # AND a new configured payload
    payload=valid_product_payload.copy()
    payload.pop(field)

    # WHEN create a product with new payload
    response = reqres_manage_client.create_product(**payload)

    #THEN response status code is negative
    assert response.status_code == 400, (
        f"Create product with missing {field} should return 400, it returns {response.status_code}"
    )