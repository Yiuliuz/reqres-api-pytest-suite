

def cleanup_product_if_created(client, response):
    if response.status_code != 201:
        return

    body = response.json()["data"]

    try:
        client.delete_product(body["id"])
    except Exception:
        pass