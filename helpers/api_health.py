

def ensure_api_available(client):
    response = client.get_products()

    if response.status_code == 429:
        raise RuntimeError(
            "ReqRes API daily request limit exceeded."
        )
    
    response.raise_for_status()