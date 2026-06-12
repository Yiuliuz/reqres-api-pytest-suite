class ReqresClient:
    def __init__(self, base_url, api_key, environment="prod", timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = {
            "x-api-key": api_key,
            "X-Reqres-Env": environment,
            "User-Agent": "qa-pytest-practice/1.0",
        }

    def get_product(self,id,project_id):
        return self._request("GET", f"/api/collections/products/records/{id}?project_id={project_id}")
    
    def get_products(self):
        return self._request("GET", "/api/collections/products/records")

    def create_product(self, name, price, category, in_stock):
        payload = {
            "data": {
                "name": name,
                "price": price,
                "category":category,
                "in_stock":in_stock
            }
        }

        return self._request(
            "POST",
            "/api/collections/products/records",
            json=payload,
        )

    def _request(self, method, path, **kwargs):
        import requests

        headers = kwargs.pop("headers", {})
        merged_headers = {**self.default_headers, **headers}

        return requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=merged_headers,
            timeout=self.timeout,
            **kwargs,
        )
