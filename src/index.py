from create_order import create_order
from get_order import poll_order
from utils import validate
from dotenv import load_dotenv
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
    print(client_secret, order)
    validate(order['phase'] == "payment", f'Order is in phase "{order["phase"]}". Expected "payment".')

    payment = order['payment']
    validate(payment['status'] == "awaiting-payment", 
            f'Payment is in status "{payment["status"]}". Expected "awaiting-payment".')
    serialized_transaction = payment['preparation']['serializedTransaction']

    print(f'Copy and paste this string to the next step of the quickstart: {serialized_transaction}')

    completed_order = poll_order(order['orderId'], client_secret)
    print("Here is the final order details")
    print(json.dumps(completed_order, indent=2))

except Exception as error:
    print(f"Error: {error}", file=sys.stderr)