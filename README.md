Generate Account Numbers Sequentially: Use a tool like seq in Linux or Python to generate numbers in the required 16-digit format.

Test Against Mullvad's API: Use curl or a similar tool to send HTTP requests to the Mullvad endpoint to check if an account number is valid.

Save Valid Accounts: If the API response indicates the account is valid, save the number to a file.

validgen is the final poc
