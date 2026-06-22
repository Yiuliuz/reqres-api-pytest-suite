import pytest

from helpers.cleanup_helpers import cleanup_product_if_created

pytestmark = [pytest.mark.api, pytest.mark.live]


@pytest.mark.contract
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.known_issue
@pytest.mark.xfail(
    reason="Known API issue: Allows to create a product with empty required field",
    strict=True
)
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
    response = reqres_manage_client.create_product(payload)

    try:
        #THEN response status code is negative
        assert response.status_code == 400, (
            f"Create product with empty value in {field} field should return 400, it returns {response.status_code} "
        )
    finally:
        cleanup_product_if_created(reqres_manage_client, response)


@pytest.mark.contract
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.known_issue
@pytest.mark.xfail(
    reason="Known API issue: Allows to create a product with invalyd data type",
    strict=True
)
@pytest.mark.parametrize(
    "field , type_try",
    [
        pytest.param("name",123,id="int type name"),
        pytest.param("name",True,id="bool type name"),
        pytest.param("name",[],id="list type name"),
        pytest.param("name",{},id="dict type name"),
        
        pytest.param("price","abc",id="str type price"),
        pytest.param("price",True,id="bool type price"),
        pytest.param("price",[],id="list type price"),
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
    response = reqres_manage_client.create_product(payload)
    
    try:
        #THEN response status code is negative
        assert response.status_code == 400, (
            f"Create product {type(type_try)} {field} should return 400, it returns {response.status_code}"
        )
    finally:
        cleanup_product_if_created(reqres_manage_client, response)


@pytest.mark.contract
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.known_issue
@pytest.mark.xfail(
    reason="Known API issue: Allows to create a product with missing required field",
    strict=True
)
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
    response = reqres_manage_client.create_product(payload)

    try:
        #THEN response status code is negative
        assert response.status_code == 400, (
            f"Create product with missing {field} should return 400, it returns {response.status_code}"
        )
    finally:
        cleanup_product_if_created(reqres_manage_client, response)


@pytest.mark.read_only
@pytest.mark.negative
def test_get_nonexist_product_returns_404(reqres_client):
    #GIVEN a configured api client

    #WHEN requests a product by inexistent id
    response=reqres_client.get_product("INVALID ID")

    #THEN response status code is negative
    assert response.status_code==404, (
        f"Request a product by invalid id should return 404, it returns {response.status_code}",
        f"Text= {response.text}"
    )