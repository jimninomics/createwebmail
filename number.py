import requests
import time
import os
import argparse
from typing import Optional, Dict, List, Tuple, Union

class DaisySMS:
    BASE_URL = "https://daisysms.com/stubs/handler_api.php"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_number(self, service: str = "ds", max_price: float = 5.5,
                  areas: Optional[List[str]] = None,
                  carriers: Optional[List[str]] = None) -> Tuple[bool, Union[str, Dict]]:
        """
        Rent a phone number

        Returns:
            Tuple[bool, Union[str, Dict]]: (success, result)
                If success is True, result is a dict with 'id' and 'number'
                If success is False, result is an error message
        """
        params = {
            "api_key": self.api_key,
            "action": "getNumber",
            "service": service,
            "max_price": max_price
        }

        if areas:
            params["areas"] = ",".join(areas)

        if carriers:
            params["carriers"] = ",".join(carriers)

        response = requests.get(self.BASE_URL, params=params)
        result = response.text

        if result.startswith("ACCESS_NUMBER"):
            # Parse the response: ACCESS_NUMBER:ID:PHONE_NUMBER
            parts = result.split(":")
            return True, {"id": parts[1], "number": parts[2]}
        else:
            # Handle error cases
            return False, result

    def get_status(self, activation_id: str, get_text: bool = False) -> Tuple[bool, Union[str, Dict]]:
        """
        Check status and get SMS code if available

        Returns:
            Tuple[bool, Union[str, Dict]]: (success, result)
                If success is True, result is a dict with 'code' and optionally 'text'
                If success is False, result is an error message
        """
        params = {
            "api_key": self.api_key,
            "action": "getStatus",
            "id": activation_id
        }

        if get_text:
            params["text"] = 1

        response = requests.get(self.BASE_URL, params=params)
        result = response.text

        if result.startswith("STATUS_OK"):
            # Parse the response: STATUS_OK:CODE
            code = result.split(":")[1]
            response_data = {"code": code}

            # If text was requested, get it from headers
            if get_text and "X-Text" in response.headers:
                response_data["text"] = response.headers["X-Text"]

            return True, response_data
        else:
            return False, result

    def mark_as_done(self, activation_id: str) -> Tuple[bool, str]:
        """
        Mark a rental as done

        Returns:
            Tuple[bool, str]: (success, message)
        """
        params = {
            "api_key": self.api_key,
            "action": "setStatus",
            "id": activation_id,
            "status": 6
        }

        response = requests.get(self.BASE_URL, params=params)
        result = response.text

        if result == "ACCESS_ACTIVATION":
            return True, "Successfully marked as done"
        else:
            return False, result

    def cancel_number(self, activation_id: str) -> Tuple[bool, str]:
        """
        Cancel a number rental (no code received or user canceled)

        Returns:
            Tuple[bool, str]: (success, message)
        """
        params = {
            "api_key": self.api_key,
            "action": "setStatus",
            "id": activation_id,
            "status": 8  # Status 8 for cancellation
        }

        response = requests.get(self.BASE_URL, params=params)
        result = response.text

        if result == "ACCESS_ACTIVATION":
            return True, "Successfully canceled number"
        else:
            return False, result

    def wait_for_code(self, activation_id: str, timeout: int = 90,
                     interval: int = 5, get_text: bool = False,
                     allow_cancel: bool = False) -> Tuple[bool, Union[str, Dict]]:
        """
        Wait for SMS code to arrive with timeout

        Args:
            activation_id: The activation ID
            timeout: Maximum time to wait in seconds
            interval: Time between checks in seconds
            get_text: Whether to get the full SMS text
            allow_cancel: Whether to allow user to cancel waiting by pressing Ctrl+C

        Returns:
            Tuple[bool, Union[str, Dict]]: (success, result)
                If canceled, result will be "CANCELED"
        """
        start_time = time.time()

        if allow_cancel:
            print("Press Ctrl+C to cancel waiting for SMS code")

        try:
            while time.time() - start_time < timeout:
                success, result = self.get_status(activation_id, get_text)

                if success:
                    return True, result
                elif result == "STATUS_WAIT_CODE":
                    elapsed = int(time.time() - start_time)
                    remaining = timeout - elapsed
                    print(f"Waiting for SMS... (elapsed: {elapsed}s, remaining: {remaining}s) - Press Ctrl+C to cancel")
                    time.sleep(interval)
                else:
                    return False, result

            return False, "Timeout waiting for SMS"

        except KeyboardInterrupt:
            print("\nCanceled by user")
            return False, "CANCELED"

def get_verification_code(
    api_key="1FnYUz38JilRDCbFcoxIRsYvuWCGH1",
    service="go",  # go for Google/Gmail/YouTube
    max_price=0.19,
    areas=None,
    carriers=None,
    timeout=90,
    interval=5,
    get_text=False,
    allow_cancel=True
):
    """
    Get a phone number and wait for verification code

    Args:
        api_key: Your DaisySMS API key
        service: Service code (go for Google/Gmail/YouTube)
        max_price: Maximum price
        areas: List of area codes or comma-separated string
        carriers: List of carriers or comma-separated string
        timeout: Maximum time to wait for SMS in seconds
        interval: Time between status checks in seconds
        get_text: Whether to get the full SMS text
        allow_cancel: Whether to allow cancellation if no code is received

    Returns:
        dict: Result with keys:
            - success (bool): Whether the operation was successful
            - code (str, optional): The verification code if successful
            - text (str, optional): The full SMS text if requested and available
            - phone_number (str, optional): The phone number used
            - error (str, optional): Error message if not successful
            - canceled (bool, optional): Whether the operation was canceled by the user
    """
    # Process areas and carriers if they're strings
    if isinstance(areas, str):
        areas = [a.strip() for a in areas.split(",")] if areas else None
    if isinstance(carriers, str):
        carriers = [c.strip() for c in carriers.split(",")] if carriers else None

    client = DaisySMS(api_key)

    # Get a number
    print("Requesting a phone number...")
    success, result = client.get_number(
        service=service,
        max_price=max_price,
        areas=areas,
        carriers=carriers
    )

    if not success:
        print(f"Error: {result}")
        return {"success": False, "error": result}

    activation_id = result["id"]
    phone_number = result["number"]
    print(f"Got number: {phone_number} (ID: {activation_id})")

    # Wait for SMS code
    print(f"Waiting for SMS code (timeout: {timeout}s, checking every {interval}s)...")
    success, result = client.wait_for_code(
        activation_id=activation_id,
        timeout=timeout,
        interval=interval,
        get_text=get_text,
        allow_cancel=allow_cancel
    )

    if success:
        response = {
            "success": True,
            "code": result["code"],
            "phone_number": phone_number
        }

        print(f"Got code: {result['code']}")
        if get_text and 'text' in result:
            response["text"] = result["text"]
            print(f"Message text: {result['text']}")

        # Mark as done
        print("Marking rental as done...")
        success, message = client.mark_as_done(activation_id)
        if success:
            print(message)
        else:
            print(f"Error marking as done: {message}")

        return response
    else:
        # Check if the operation was canceled by the user
        if result == "CANCELED":
            print("Operation canceled by user. Canceling number rental...")
            success, message = client.cancel_number(activation_id)
            if success:
                print(message)
            else:
                print(f"Error canceling number: {message}")

            return {
                "success": False,
                "canceled": True,
                "error": "Operation canceled by user",
                "phone_number": phone_number
            }
        else:
            print(f"Failed to get code: {result}")

            # Ask user if they want to cancel the number
            if allow_cancel:
                try:
                    choice = input("No code received. Do you want to cancel this number? (y/n): ").strip().lower()
                    if choice == 'y' or choice == 'yes':
                        print("Canceling number rental...")
                        success, message = client.cancel_number(activation_id)
                        if success:
                            print(message)
                        else:
                            print(f"Error canceling number: {message}")

                        return {
                            "success": False,
                            "canceled": True,
                            "error": "Number canceled by user",
                            "phone_number": phone_number
                        }
                except KeyboardInterrupt:
                    print("\nCanceling number rental...")
                    success, message = client.cancel_number(activation_id)
                    if success:
                        print(message)
                    else:
                        print(f"Error canceling number: {message}")

                    return {
                        "success": False,
                        "canceled": True,
                        "error": "Operation canceled by user",
                        "phone_number": phone_number
                    }

            return {"success": False, "error": result, "phone_number": phone_number}

def main():
    parser = argparse.ArgumentParser(description="DaisySMS API Client")
    parser.add_argument("--api-key", help="Your DaisySMS API key", default="1FnYUz38JilRDCbFcoxIRsYvuWCGH1")
    parser.add_argument("--service", help="Service code", default="go")  # go for Google/Gmail/YouTube
    parser.add_argument("--max-price", help="Maximum price", type=float, default=0.21)
    parser.add_argument("--areas", help="Comma-separated area codes", default="")
    parser.add_argument("--carriers", help="Comma-separated carriers", default="")
    parser.add_argument("--timeout", help="Timeout for waiting for SMS", type=int, default=90)
    parser.add_argument("--interval", help="Interval between status checks", type=int, default=5)
    parser.add_argument("--get-text", help="Get full SMS text", action="store_true")
    parser.add_argument("--no-cancel", help="Disable cancellation option", action="store_true")

    args = parser.parse_args()

    # Call the function with parsed arguments
    get_verification_code(
        api_key=args.api_key,
        service=args.service,
        max_price=args.max_price,
        areas=args.areas,
        carriers=args.carriers,
        timeout=args.timeout,
        interval=args.interval,
        get_text=args.get_text,
        allow_cancel=not args.no_cancel
    )

    # Result is already printed in the function, no need to print again

if __name__ == "__main__":
    main()