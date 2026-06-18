"""
Run from project root:

python -m scripts.check_api_health
"""

from helpers.client_factory import create_reqres_client
from helpers.api_health import ensure_api_available

def main():
    client = create_reqres_client()
    ensure_api_available(client)
    print("API available")

if __name__=="__main__":
    main()