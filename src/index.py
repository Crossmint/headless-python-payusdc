from create_order import create_order
from get_order import poll_order
from utils import validate
from dotenv import load_dotenv
from rich import print as rprint
from rich.text import Text
import json
import os
import sys

# Load environment variables
load_dotenv()

# Validate required environment variables
validate(os.getenv('CROSSMINT_API_KEY'), 'CROSSMINT_API_KEY is required.')
validate(os.getenv('COLLECTION_ID'), 'COLLECTION_ID is required')
validate(os.getenv('EMAIL_ADDRESS'), 'EMAIL_ADDRESS is required')
validate(os.getenv('PAYER_ADDRESS'), 'PAYER_ADDRESS is required')

try:
    print("Creating order...")
    result = create_order()
    client_secret, order = result['clientSecret'], result['order']
    rprint(client_secret, order)
    validate(order['phase'] == "payment", f'Order is in phase [bold red]"{order["phase"]}"[/bold red]. Expected "payment".')

    payment = order['payment']
    validate(payment['status'] == "awaiting-payment", 
            f'Payment is in status "{payment["status"]}". Expected "awaiting-payment".')
    serialized_transaction = payment['preparation']['serializedTransaction']

    print(f'Copy and paste this string to the next step of the quickstart: \033[34m{serialized_transaction}\033[0m')

    completed_order = poll_order(order['orderId'], client_secret)
    rprint("Here is the final order details")
    rprint(json.dumps(completed_order, indent=2))

except Exception as error:
    rprint(f"Error: {error}", file=sys.stderr)