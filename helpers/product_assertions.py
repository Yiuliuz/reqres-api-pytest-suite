

def assert_product_matches_payload(product, payload):
    for field, expected_value in payload.items():
        assert product[field] == expected_value, (
            f"Field '{field}' mismatch. "
            f"Expected={expected_value}, Actual={product[field]}"
        )