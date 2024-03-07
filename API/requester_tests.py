import requests
import datetime

# Define the URL
url = 'http://localhost:5000/TEST'  # Replace with your actual URL

# Define the data
data = {
    'price_at_buy': 100.0,
    'purchase_date': datetime.date.today().isoformat(),
    'fee_ratio_at_buy': 0.02,
    'fee_ratio_at_sell': 0.02,
    'capital_gains_tax_ratio': 0.15,
    'target_profit_ratio': 0.1
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response
print(response.json())