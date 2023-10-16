import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the API URL
api_url = "https://api.monobank.ua/bank/currency"
google_sheets_keyfile = "C:\\Users\\Vadym\\Downloads\\mythic-display-331614-748fd073f08b.json"

# Authenticate with Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_sheets_keyfile, scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet by title or URL
# Replace 'Your Spreadsheet' with the title or URL of your Google Sheet
sheet = gc.open('task1').sheet1

try:
    # Send an HTTP GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Create an empty DataFrame to store the exchange rate data
        exchange_rates_df = pd.DataFrame(columns=['CurrencyPair', 'RateBuy', 'RateSell'])

        # Iterate through the data and extract exchange rate information
        for currency in data:
            currency_pair = f"{currency['currencyCodeA']} to {currency['currencyCodeB']}"
            rate_buy = currency['rateBuy']
            rate_sell = currency['rateSell']
            exchange_rates_df = exchange_rates_df.append({
                'CurrencyPair': currency_pair,
                'RateBuy': rate_buy,
                'RateSell': rate_sell
            }, ignore_index=True)

        # Clear the existing data in the Google Sheet
        sheet.clear()

        # Update the Google Sheet with the exchange rate data
        sheet.update([exchange_rates_df.columns.values.tolist()] + exchange_rates_df.values.tolist())

        print("Exchange rate data saved to the Google Sheet.")

    else:
        print(f"Request to {api_url} failed with status code {response.status_code}")

except requests.RequestException as e:
    print(f"An error occurred while making the request: {str(e)}")

