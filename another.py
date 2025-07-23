import requests
import json
import base64
import socket
import sys

def create_cpanel_email(cpanel_url, username, password, email_user, email_domain, email_password, quota=0):
    """Create a new email account on cPanel"""
    try:
        # API endpoint for email account creation
        endpoint = f"{cpanel_url}/execute/Email/add_pop"

        # Create Basic Auth header (properly encoded)
        auth_str = f"{username}:{password}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

        # Request headers
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json'
        }

        # Request data
        data = {
            'domain': email_domain,
            'email': email_user,
            'password': email_password,
            'quota': quota
        }

        print(f"Connecting to {cpanel_url}...")

        # Make the API request with a timeout
        response = requests.post(endpoint, headers=headers, json=data, timeout=10)

        return {
            "success": True,
            "data": response.json()
        }

    except requests.exceptions.ConnectionError as e:
        # Handle connection errors (DNS resolution, connection refused, etc.)
        error_msg = str(e)
        if "getaddrinfo failed" in error_msg:
            return {
                "success": False,
                "error": f"DNS resolution failed for {cpanel_url}. Please check if the domain is correct and accessible."
            }
        elif "Connection refused" in error_msg:
            return {
                "success": False,
                "error": f"Connection refused to {cpanel_url}. Please check if the server is running and the port is open."
            }
        else:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": f"Connection to {cpanel_url} timed out. The server might be down or unreachable."
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request error: {str(e)}"
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Failed to parse server response as JSON."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

def verify_domain_exists(domain):
    """Check if a domain exists by attempting to resolve its DNS"""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

if __name__ == "__main__":
    # Configuration
    CPANEL_URL = "https://cpanel.financedon.online:2083"  # Updated cPanel URL to match the domain
    CPANEL_USERNAME = "fleaycpy"                   # Your cPanel username
    CPANEL_PASSWORD = "aloomaID123@$"              # Replace with actual password

    # Email account details
    EMAIL_USER = "lbrewer750"                          # Email username (before @)
    EMAIL_DOMAIN = "financedon.online"             # Your domain
    EMAIL_PASSWORD = "6qK50yoj#R$T"               # Password for new email

    # First verify the domain exists
    domain = CPANEL_URL.split("://")[1].split(":")[0]
    if not verify_domain_exists(domain):
        print(f"Error: Cannot resolve domain '{domain}'. Please check if the domain is correct.")
        print("Possible solutions:")
        print("1. Make sure the domain is registered and DNS is properly configured")
        print("2. Try using the server's IP address instead of the domain name")
        print("3. Check if your internet connection is working properly")
        sys.exit(1)

    # Create the email account
    result = create_cpanel_email(
        CPANEL_URL,
        CPANEL_USERNAME,
        CPANEL_PASSWORD,
        EMAIL_USER,
        EMAIL_DOMAIN,
        EMAIL_PASSWORD
    )

    # Print the result
    if result["success"]:
        print("Email account created successfully!")
        print(json.dumps(result["data"], indent=4))
    else:
        print(f"Error: {result['error']}")