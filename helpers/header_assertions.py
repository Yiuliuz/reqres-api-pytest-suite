

def assert_json_content_type(response):
    assert "Content-Type" in response.headers,(
        "Missing Content Type header"
    )
    assert "application/json" in response.headers["Content-Type"], (
    "Incorrect Content-Type header. "
    f"Expected a JSON response, got: "
    f"{response.headers['Content-Type']}"
    )

def assert_rate_limit_headers(response):
    headers = response.headers

    assert "X-Ratelimit-Limit" in headers,("Missing X-Ratelimit-Limit header")
    assert "X-Ratelimit-Remaining" in headers,("Missing X-Ratelimit-Remaining header")
    assert "X-Ratelimit-Reset" in headers,("Missing X-Ratelimit-Reset header")

def assert_request_trace_headers(response):
    assert "X-Request-Id" in response.headers,("Missing X-Request-Id header")

def assert_common_headers(response):
    assert_json_content_type(response)
    assert_rate_limit_headers(response)
    assert_request_trace_headers(response)