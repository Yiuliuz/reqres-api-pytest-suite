

def print_request_history(client,test_name):

    print("\n" + "=" * 70)
    print(f" FAILED TEST: {test_name}")
    print("=" * 70)

    for i, entry in enumerate(client.request_history, start=1):

        response = entry["response"]

        print(f"\n→ REQUEST → #{i}")
        print("-" * 70)
        print(f"{entry['method']} {entry['url']}")
        print(f"Headers: {entry['request_headers']}")
        print(f"Body: {entry['request_body']}")

        print(f"\n← RESPONSE ← #{i}")
        print("-" * 70)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Body: {response.text[:1000]}")