REQUIRED_PRODUCT_FIELDS = {"id", "data"}
REQUIRED_PRODUCT_DATA_FIELDS = {"name", "price"}
OPTIONAL_PRODUCT_FIELDS = {"createdAt", "updatedAt"}


def assert_product_contract(product):
    # GIVEN a product response payload

    # THEN the response should contain all required top-level fields
    missing_fields = REQUIRED_PRODUCT_FIELDS - set(product)

    #THEN there is missing fields
    assert not missing_fields, (
        f"Product does not match the expected contract. "
        f"Missing fields: {sorted(missing_fields)}. Product={product}"
    )
    # AND the data field should be a JSON object
    assert isinstance(product["data"], dict), (
        f"The data field should be a JSON object. Product={product}"
    )
    # AND the data object should contain all required product fields
    missing_data_fields = REQUIRED_PRODUCT_DATA_FIELDS - set(product["data"])

    assert not missing_data_fields, (
        f"Product data does not match the expected contract. "
        f"Missing fields: {sorted(missing_data_fields)}. Product={product}"
    )
    #AND optional timestamp fields should be strings when present
    unexpected_optional_types = [
        field
        for field in OPTIONAL_PRODUCT_FIELDS
        if field in product and not isinstance(product[field], str)
    ]

    assert not unexpected_optional_types, (
        f"Optional timestamp fields should be strings when present. "
        f"Invalid fields: {unexpected_optional_types}. Product={product}"
    )
