from utils import base_url, validate
import os
import requests

def create_order():
    order_data = {
        "recipient": {
            "email": os.environ.get("EMAIL_ADDRESS")
        },
        "locale": "en-US",
        "payment": {
            "method": "ethereum-sepolia",
            "currency": "usdc",
            "payerAddress": os.environ.get("PAYER_ADDRESS")
        },
        "lineItems": {
            "collectionLocator": f"crossmint:{os.environ.get('COLLECTION_ID')}"
        }
    }

    try:
        response = requests.post(
            f"{base_url}/orders",
            headers={
                "Content-Type": "application/json",
                "x-api-key": os.environ.get("CROSSMINT_API_KEY")
            },
            json=order_data
        )

        validate(response.ok, f"Failed to create order: {response.reason}")
        json_response = response.json()
        return {"clientSecret": json_response["clientSecret"], "order": json_response["order"]}
    except Exception as error:
        raise error