REQUIRED_PRODUCT_FIELDS = {"id", "data", "createdAt", "updatedAt"}
REQUIRED_PRODUCT_DATA_FIELDS = {"name", "price"}


def assert_product_contract(product):
    missing_fields = REQUIRED_PRODUCT_FIELDS - set(product)

    assert not missing_fields, (
        f"Product does not match the expected contract. "
        f"Missing fields: {sorted(missing_fields)}. Product={product}"
    )

    assert isinstance(product["data"], dict), (
        f"The data field should be a JSON object. Product={product}"
    )

    missing_data_fields = REQUIRED_PRODUCT_DATA_FIELDS - set(product["data"])

    assert not missing_data_fields, (
        f"Product data does not match the expected contract. "
        f"Missing fields: {sorted(missing_data_fields)}. Product={product}"
    )
