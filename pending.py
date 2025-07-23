import requests

# Replace with your correct API user credentials
username = "rahmonidris04@gmail.com"  # Must be an admin user
password = "aloomaid123@$"
client_secret = "f558ba166258089b2ef322c340554c"

url = "https://apicfa.convirza.com/oauth/token"
payload = {
    "grant_type": "password",
    "client_id":"system",
    "username": username,
    "password": password,
    "client_secret": client_secret
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
response = requests.post(url, data=payload, headers=headers)


print("Status Code:", response.status_code)
print("Response:", response.text)

# Response: {"access_token":"86bb9237-9ae4-4398-8076-a0028442cfff","refresh_token":"6b35b4ea-dc1e-4d44-a33f-6128d9860c09","expires_in":3600,"status":"success","token_type":"Bearer"}