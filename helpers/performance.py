

def assert_response_time(response, max_seconds=2):
    elapsed = response.elapsed.total_seconds()

    assert elapsed <= max_seconds, (
        f"Response time exceeded: {elapsed:.3f}s > {max_seconds}s"
    )