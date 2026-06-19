class ReqresClient:
    def __init__(self, base_url, api_key, environment="prod", timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = {
            "x-api-key": api_key,
            "X-Reqres-Env": environment,
            "User-Agent": "qa-pytest-practice/1.0",
        }
        self.request_history = []

    def get_product(self,id):
        return self._request("GET", f"/api/collections/products/records/{id}")
    
    def get_products(self):
        return self._request("GET", "/api/collections/products/records")
    
    def delete_product(self,id):
        return self._request("DELETE", f"/api/collections/products/records/{id}")

    def create_product(self, body: dict):
        payload = {
            "data": body
        }

        return self._request(
            "POST",
            "/api/collections/products/records",
            json=payload,
        )

    def update_product(self,id,body:dict):
        payload = {
            "data" : body
        } 
        
        return self._request(
            "PUT",
            f"/api/collections/products/records/{id}",
            json=payload,
        )

    def _request(self, method, path, **kwargs):
        import requests

        headers = kwargs.pop("headers", {})
        merged_headers = {**self.default_headers, **headers}

        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=merged_headers,
            timeout=self.timeout,
            **kwargs,
        )

        self.request_history.append(
            {
                "method": method,
                "url": f"{self.base_url}{path}",
                "request_headers": merged_headers,
                "request_body": kwargs.get("json"),
                "response": response,
            }
        )

        return response
