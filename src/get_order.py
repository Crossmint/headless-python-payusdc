from typing import Dict, Any
from utils import base_url, validate
from rich import print
import os
import requests
import time

def get_order(order_id: str, client_secret: str) -> Dict[str, Any]:
    try:
        response = requests.get(
            f"{base_url}/orders/{order_id}",
            headers={
                'Content-Type': 'application/json',
                'x-api-key': os.environ.get('CROSSMINT_API_KEY'),
                'Authorization': client_secret
            }
        )
        
        validate(response.ok, f"Failed to get order: {response.reason}")
        return response.json()
    except Exception as error:
        raise error

def poll_order(order_id: str, client_secret: str) -> Dict[str, Any]:
    while True:
        try:
            order = get_order(order_id, client_secret)
            print(f'Current order status: [bold yellow]{order["phase"]}[/bold yellow]')

            if order['phase'] == 'completed':
                return order
            time.sleep(3)
            
        except Exception as error:
            raise error