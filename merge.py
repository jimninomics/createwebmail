import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import mouse
import requests
import pyautogui as pt
import os
import subprocess
import undetected_chromedriver as uc
from faker import Faker
import string
import ssl
import random
import json
import base64
import socket
import sys
import re
from email.header import decode_header
import imaplib
import email
from typing import Optional, Dict, List, Tuple, Union
from oauth2client.service_account import ServiceAccountCredentials
import gspread
ssl._create_default_https_context = ssl._create_unverified_context
fake = Faker()
openvpn_path = r"C:\Program Files\OpenVPN\bin\openvpn.exe"
list_of_proxy = [f"vpn/{file}" for file in os.listdir('vpn') if file.endswith('.ovpn')]

auth_path = "vpn/auth.txt"
CPANEL_URL = ""  # Updated cPanel URL to match the domain
CPANEL_USERNAME = ""                   # Your cPanel username
CPANEL_PASSWORD = ""              # Replace with actual password

def is_vpn_connected():
    """Check if VPN is connected by verifying the external IP address."""
    try:
        response = requests.get("https://ifconfig.me", timeout=5)  # Use an external IP checker
        current_ip = response.text.strip()

        print(f"Current IP: {current_ip}")
        return current_ip not in ["209.209.40.119"]  # Replace with your actual ISP IP
    except requests.RequestException as e:
        print(f"Error checking VPN status: {e}")
        return False  # Assume not connected if there's an error


def connect_vpn():
    """Connect to VPN and verify connection."""
    config_path = random.choice(list_of_proxy)

    print("Connecting to VPN...")
    subprocess.Popen([openvpn_path, "--config", config_path, "--auth-user-pass", auth_path])

    time.sleep(15)  # Wait for connection to establish

def confirm_if_vpn_is_on():
    # Verify VPN connection
    while True:
        for _ in range(2):  # Retry up to 5 times
            if is_vpn_connected():
                print("VPN successfully connected.")
                return True
            print("VPN not connected, retrying...")
            time.sleep(5)

        try:
            disconnect_vpn()
        except:
            pass
        try:
            connect_vpn()
        except:
            pass



def disconnect_vpn():
    """Disconnect VPN by terminating OpenVPN process."""
    try:
        print("Disconnecting from VPN...")
        subprocess.run(["taskkill", "/F", "/IM", "openvpn.exe"], check=True)
        print("VPN disconnected.")
    except Exception as e:
        print(f"Error disconnecting VPN: {e}")


def connect_to_incognitor():
    # options = webdriver.ChromeOptions()
    # options.add_argument("--incognito")
    # driver = webdriver.Chrome(options=options)
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://admin.google.com/ac/users")
    return driver

def login_to_webmail(driver, gmail_account, gmail_password):


    #-------------------------------------------------------------------------------------------------------
    nini= 0
    while True:
        nini+=1
        try:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Email or phone"]')))
                driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Email or phone"]').clear()
                driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Email or phone"]').send_keys(gmail_account)
                click_next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
                    )
                try:
                    click_next_button.click()
                except:
                    driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                    driver.execute_script("arguments[0].click();", click_next_button)
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Enter your password"]')))
            except: 
                pass

            try:
                driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Enter your password"]').send_keys(gmail_password)
                click_next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
                    )
                try:
                    click_next_button.click()
                except:
                    driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                    driver.execute_script("arguments[0].click();", click_next_button)
            except:
                pass
            try:
                click_next_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="I understand"]'))
                    )
                try:
                    click_next_button.click()
                except:
                    driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                    driver.execute_script("arguments[0].click();", click_next_button)
            except:
                pass
            try:
                click_next_button = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, 'Do this later'))
                    )
                try:
                    click_next_button.click()
                except:
                    driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                    driver.execute_script("arguments[0].click();", click_next_button)
            except:
                pass
            try:
                try:
                    position1 = pt.locateOnScreen("images_state/chromewithout1.PNG", confidence=.7)
                    x = position1[0]
                    y = position1[1]
                    pt.moveTo(x+20,y+20)
                    pt.click()
                    time.sleep(2)
                except:
                    position1 = pt.locateOnScreen("images_state/chromewithout.PNG", confidence=.7)
                    x = position1[0]
                    y = position1[1]
                    pt.moveTo(x+20,y+20)
                    pt.click()
                    time.sleep(2)
                
            except:
                pass
            try:
                position1 = pt.locateOnScreen("images_state/chromewithout2.PNG", confidence=.7)
                x = position1[0]
                y = position1[1]
                pt.moveTo(x+20,y+20)
                pt.click()
                time.sleep(2)
            except:
                pass
            click_next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Invite new user"]'))
                )
            break
        except:
            if nini % 3 == 0:
                driver.refresh()
            elif nini % 5 == 0:
                driver.get("https://admin.google.com/ac/users")
            elif nini % 10 == 0:
                sign_out(driver, gmail_account)
            
            time.sleep(1)
    try:
        click_next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Invite new user"]'))
            )
        return True
    except:
        return False

def sign_out(driver, gmail_account):

    driver.get('https://accounts.google.com/Logout')

    def sign_sign(gmail_account):
        for _ in range(10):
            try:
                try:
                    try:
                        remove_an_account = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, "//li[.//div[text()='Remove an account']]"))
                            )
                        try:
                            remove_an_account.click()
                        except:
                            driver.execute_script("arguments[0].scrollIntoView();", remove_an_account)
                            driver.execute_script("arguments[0].click();", remove_an_account)
                    except:
                        remove_an_account= driver.find_element(By.CSS_SELECTOR, 'li[jsname="fKeql"]')
                        try:
                            remove_an_account.click()
                        except:
                            driver.execute_script("arguments[0].scrollIntoView();", remove_an_account)
                            driver.execute_script("arguments[0].click();", remove_an_account)
                except:
                    pass
                try:
                    try:
                        remove_the_account = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, f'//li[.//div[@data-email="{gmail_account}"]]'))
                            )
                        try:
                            remove_the_account.click()
                        except:
                            driver.execute_script("arguments[0].scrollIntoView();", remove_the_account)
                            driver.execute_script("arguments[0].click();", remove_the_account)
                    except:
                        remove_the_account = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.TAG_NAME, f'li'))
                            )
                        try:
                            remove_the_account.click()
                        except:
                            driver.execute_script("arguments[0].scrollIntoView();", remove_the_account)
                            driver.execute_script("arguments[0].click();", remove_the_account)
                except:
                    pass
                try:
                    try:
                        yes_remove = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Yes, remove']]"))
                            )
                        try:
                            yes_remove.click()
                        except:
                            driver.execute_script("arguments[0].scrollIntoView();", yes_remove)
                            driver.execute_script("arguments[0].click();", yes_remove)
                    except:
                        yes_remove= driver.find_element(By.CSS_SELECTOR, 'button[data-mdc-dialog-action="ssJRIf"]')
                        try:
                            yes_remove.click()
                        except:
                            driver.execute_script("arguments[0].scrollIntoView();", yes_remove)
                            driver.execute_script("arguments[0].click();", yes_remove)
                except:
                    pass
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Email or phone"]')))
                break
            except:
                driver.get('https://accounts.google.com/Logout')

    try:
        english_pickr= driver.find_element(By.CSS_SELECTOR, 'li[data-value="en-US"]')
        try:
            english_pickr.click()
        except:
            driver.execute_script("arguments[0].scrollIntoView();", english_pickr)
            driver.execute_script("arguments[0].click();", english_pickr)
    except:
        pass
    sign_sign(gmail_account)
    while True:
        try:
            driver.get("https://workspace.google.com/essentials/signup/verify/emailstart?hl=en&source=gafb-essentials-hero-en&ga_region=noram&ga_country=us&ga_lang=en&")
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'ucj-1')))
            break
        except:
            sign_sign(gmail_account)
            pass
    try:
        english_pickr= driver.find_element(By.CSS_SELECTOR, 'li[data-value="en-US"]')
        try:
            english_pickr.click()
        except:
            driver.execute_script("arguments[0].scrollIntoView();", english_pickr)
            driver.execute_script("arguments[0].click();", english_pickr)
    except:
        pass

def generate_name():
    """Generate a random first and last name"""
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name

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

def create_webmail_from_cpanel(email_user, email_password, email_domain):

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
        email_user,
        email_domain,
        email_password
    )

    # Print the result
    if result["success"]:
        print("Email account created successfully!")
        return True
    else:
        print("failed to create email account")
        return False

def generate_name():
    """Generate a random first and last name with username and strong password"""
    first_name = fake.first_name()
    last_name = fake.last_name()

    # Generate username options
    username1 = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
    username2 = f"{first_name.lower()}_{last_name.lower()}{random.randint(1, 99)}"
    username3 = f"{first_name[0].lower()}{last_name.lower()}{random.randint(10, 999)}"

    # Randomly select one username style
    username = random.choice([username1, username2, username3])

    # Generate a strong password
    lowercase = random.sample(string.ascii_lowercase, 4)
    uppercase = random.sample(string.ascii_uppercase, 3)
    digits = random.sample(string.digits, 3)
    special = random.sample("!@#$%^&*()-_=+", 2)

    # Combine all character types and shuffle
    all_chars = lowercase + uppercase + digits + special
    random.shuffle(all_chars)
    password = ''.join(all_chars)

    return first_name, last_name, username, password


def google_interface(driver, password):
    for _ in range(5):
        try:
            try:
                click_next_button = WebDriverWait(driver, 40).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
                    )
                try:
                    click_next_button.click()
                except:
                    driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                    driver.execute_script("arguments[0].click();", click_next_button)
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Enter your password"]')))
                driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Enter your password"]').clear()
                driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Enter your password"]').send_keys(password)
                click_next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
                    )
                try:
                    click_next_button.click()
                except:
                    driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                    driver.execute_script("arguments[0].click();", click_next_button)
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Enter your password"]')))
            except:
                break
        except:
            pass
    try:
        click_next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="I understand"]'))
            )
        try:
            click_next_button.click()
        except:
            driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
            driver.execute_script("arguments[0].click();", click_next_button)
        
        status= True
        status_id= 'on it'
        driver.close()
        return status, status_id
    except:
        pass
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'phoneNumberId')))
        phone_number, activation_id, client= rent_number()
        driver.find_element(By.ID, 'phoneNumberId').clear()
        driver.find_element(By.ID, 'phoneNumberId').send_keys(phone_number)
        click_next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
            )
        try:
            click_next_button.click()
        except:
            driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
            driver.execute_script("arguments[0].click();", click_next_button)

        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Enter code"]')))
        code = get_code_dev(phone_number, activation_id, client, timeout=90, interval=5)
        if code == False:
            status= True
            status_id= 'add number'
            driver.back()
            return status, status_id
        
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Enter code"]').send_keys(code)
        click_next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]"))
            )
        try:
            click_next_button.click()
        except:
            driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
            driver.execute_script("arguments[0].click();", click_next_button)
        try:
            click_next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="I understand"]'))
                )
            try:
                click_next_button.click()
            except:
                driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
                driver.execute_script("arguments[0].click();", click_next_button)
            
            status= True
            status_id= 'on it'
            driver.close()
            return status, status_id
        except:
            status= True
            status_id= 'on it'
            driver.close()
            return status, status_id
        
    except:
        pass
    status= True
    status_id= 'on it'
    return status, status_id

def register_on_google_workspace(driver, webmail, password, first_name, last_name, email_domain):
    status=''
    status_id=''
    click_next_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Invite new user"]'))
    )
    try:
        click_next_button.click()
    except:
        driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
        driver.execute_script("arguments[0].click();", click_next_button)
    input_email = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '''input[aria-label="Invitee's email address"]'''))
    )
    input_email.send_keys(webmail)
    click_next_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-id="ssJRIf"]'))
    )
    try:
        click_next_button.click()
    except:
        driver.execute_script("arguments[0].scrollIntoView();", click_next_button)
        driver.execute_script("arguments[0].click();", click_next_button)
    time.sleep(10)
    invite_link = fetch_emails_and_extract_link(webmail, password, limit=20)
    if invite_link:
        pass
    else:
        return False, "no link"
    driver.execute_script("window.open('');")
    time.sleep(2)
    parent_handle= driver.current_window_handle
    all_handles = driver.window_handles
    for handle in all_handles:
        if handle != parent_handle:
            driver.switch_to.window(handle) 
            driver.get(invite_link)
            ii=0
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Input for six digit verification code sent to your email."]')))
            except:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Input for six-digit verification code sent to your email."]')))
            conf= False
            time.sleep(5)
            for _ in range(10):
                try:
                    code = fetch_emails_and_extract_code(webmail, password, email_domain)
                    if code:
                        print(f"\nVerification code: {code}")
                        conf= True
                        break
                    else:
                        print("Code not found, retrying...")
                        time.sleep(5)
                except:
                    time.sleep(5)
            if conf== True:
                try:
                    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Input for six digit verification code sent to your email."]').clear()
                    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Input for six digit verification code sent to your email."]').send_keys(code)
                except:
                    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Input for six-digit verification code sent to your email."]').clear()
                    driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Input for six-digit verification code sent to your email."]').send_keys(code)
            else:
                status= False
                status_id= 'no code'
                driver.close()
                break
            continue_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Verify"]')
            try:
                continue_button.click()
            except:
                # If normal click fails, try scrolling to it and using JavaScript to click
                driver.execute_script("arguments[0].scrollIntoView();", continue_button)
                driver.execute_script("arguments[0].click();", continue_button)
            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ucc-0')))
                    pass
                except:
                    break
                try:
                    driver.find_element(By.ID, 'ucc-0').clear()
                    driver.find_element(By.ID, 'ucc-0').send_keys(first_name)
                    driver.find_element(By.ID, 'ucc-1').clear()
                    driver.find_element(By.ID, 'ucc-1').send_keys(last_name)
                    driver.find_element(By.ID, 'ucc-2').clear()
                    driver.find_element(By.ID, 'ucc-2').send_keys(password)
                    continue_button = driver.find_element(By.CLASS_NAME, 'UywwFc-LgbsSe')
                    try:
                        continue_button.click()
                    except:
                        # If normal click fails, try scrolling to it and using JavaScript to click
                        driver.execute_script("arguments[0].scrollIntoView();", continue_button)
                        driver.execute_script("arguments[0].click();", continue_button)
                    
                    break
                except:
                    pass
            try:
                continue_button = driver.find_element(By.CLASS_NAME, 'UywwFc-LgbsSe')
                try:
                    continue_button.click()
                except:
                    # If normal click fails, try scrolling to it and using JavaScript to click
                    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
                    driver.execute_script("arguments[0].click();", continue_button)
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'UywwFc-LgbsSe')))
                continue_button = driver.find_element(By.CLASS_NAME, 'UywwFc-LgbsSe')
                try:
                    continue_button.click()
                except:
                    # If normal click fails, try scrolling to it and using JavaScript to click
                    driver.execute_script("arguments[0].scrollIntoView();", continue_button)
                    driver.execute_script("arguments[0].click();", continue_button)
            except:
                pass
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), \"Sorry, we can't complete your signup\")]")))
                status= False
                status_id= 'vpnerror'
                driver.close()
                break
            except:
                pass
            
            try:
                WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Email or phone"]')))
                status= True
                status_id= 'on it'
                driver.close()
                
            except:
                status= True
                status_id= 'quit'
                
            # for _ in range(4):
            #     status, status_id= google_interface(driver, password)
            #     if status_id== 'add number':
            #         continue
            #     else:
            #         break

            
    driver.switch_to.window(parent_handle)
    try:
        try:
            position1 = pt.locateOnScreen("images_state/chromewithout1.PNG", confidence=.7)
            x = position1[0]
            y = position1[1]
            pt.moveTo(x+20,y+20)
            pt.click()
            time.sleep(2)
        except:
            position1 = pt.locateOnScreen("images_state/chromewithout.PNG", confidence=.7)
            x = position1[0]
            y = position1[1]
            pt.moveTo(x+20,y+20)
            pt.click()
            time.sleep(2)
        
    except:
        pass
    try:
        position1 = pt.locateOnScreen("images_state/chromewithout2.PNG", confidence=.7)
        x = position1[0]
        y = position1[1]
        pt.moveTo(x+20,y+20)
        pt.click()
        time.sleep(2)
    except:
        pass
    return status, status_id


def fetch_emails_and_extract_code(username, password, email_domain, limit=5):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(f'mail.{email_domain}', 993)
    verification_code = None

    try:
        # Login to the account
        mail.login(username, password)
        print(f"Successfully logged in as {username}")

        # Select the inbox
        mail.select('INBOX')

        # Search for all emails
        status, messages = mail.search(None, 'ALL')
        message_ids = messages[0].split()

        # Get the latest emails (limited by the 'limit' parameter)
        email_count = min(limit, len(message_ids))
        latest_emails = message_ids[-email_count:]

        print(f"Fetching {email_count} latest emails...")

        # Process each email
        for mail_id in reversed(latest_emails):
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            raw_email = msg_data[0][1]

            # Parse the raw email
            msg = email.message_from_bytes(raw_email)

            # Get email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')

            # Get sender
            from_, encoding = decode_header(msg.get("From"))[0]
            if isinstance(from_, bytes):
                from_ = from_.decode(encoding or 'utf-8')

            # Get date
            date_ = msg.get("Date")

            print(f"\n{'='*50}")
            print(f"ID: {mail_id.decode()}")
            print(f"From: {from_}")
            print(f"Subject: {subject}")
            print(f"Date: {date_}")

            # Check if this is a Google Workspace verification email
            is_google_workspace = False
            if "Google Workspace" in from_ or "googleworkspace" in from_.lower():
                if "Verify your email" in subject or "Verify your email address" in subject:
                    is_google_workspace = True
                    print("*** Found Google Workspace verification email ***")

            # Get email body
            body_text = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    # Skip attachments
                    if "attachment" in content_disposition:
                        continue

                    # Get the email body
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True)
                        if body:
                            body_text = body.decode()
                            print("\nBody:")
                            print(body_text)
                            break
            else:
                # If the email is not multipart
                body = msg.get_payload(decode=True)
                if body:
                    body_text = body.decode()
                    print("\nBody:")
                    print(body_text)

            # Extract verification code if this is a Google Workspace email
            if is_google_workspace and body_text:
                # Look for verification code pattern
                match = re.search(r'verification code:\s*(\d{6})', body_text, re.IGNORECASE)
                if not match:
                    # Try alternative pattern that might appear in the email
                    match = re.search(r'enter this\s*\n*\s*verification code:\s*\n*\s*(\d{6})', body_text, re.IGNORECASE | re.MULTILINE)
                if not match:
                    # Try even simpler pattern - just look for 6 digits that might be a code
                    match = re.search(r'\n\s*(\d{6})\s*\n', body_text)

                if match:
                    verification_code = match.group(1)
                    print(f"\n*** VERIFICATION CODE FOUND: {verification_code} ***")
                    # Save the verification code to a file
                    with open('verification_code.txt', 'w') as f:
                        f.write(verification_code)
                    print(f"Verification code saved to verification_code.txt")
                    break  # Stop processing emails once we find the code

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the connection
        mail.logout()

    return verification_code

def fetch_emails_and_extract_link(username, password, limit=5):
    """
    Fetches the latest emails and extracts the first Google Workspace invite link found.
    Returns the invite link as a string, or None if not found.
    """
    mail = imaplib.IMAP4_SSL('mail.financedon.online', 993)
    invite_link = None

    try:
        mail.login(username, password)
        mail.select('INBOX')
        status, messages = mail.search(None, 'ALL')
        message_ids = messages[0].split()
        email_count = min(limit, len(message_ids))
        latest_emails = message_ids[-email_count:]

        for mail_id in reversed(latest_emails):
            status, msg_data = mail.fetch(mail_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')
            from_, encoding = decode_header(msg.get("From"))[0]
            if isinstance(from_, bytes):
                from_ = from_.decode(encoding or 'utf-8')
            body_text = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if "attachment" in content_disposition:
                        continue
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True)
                        if body:
                            body_text = body.decode(errors='ignore')
                            break
            else:
                body = msg.get_payload(decode=True)
                if body:
                    body_text = body.decode(errors='ignore')
            # Extract invite link
            invite_match = re.search(r'(https://workspace\.google\.com/essentials/jointeam\?[^\s)]+)', body_text)
            if invite_match:
                invite_link = invite_match.group(1)
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mail.logout()
    return invite_link

class DaisySMS:
    BASE_URL = "https://daisysms.com/stubs/handler_api.php"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_number(self, service: str = "ds", max_price: float = 0.2,
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

    def wait_for_code(self, activation_id: str, timeout: int = 300,
                     interval: int = 5, get_text: bool = False) -> Tuple[bool, Union[str, Dict]]:
        """
        Wait for SMS code to arrive with timeout

        Args:
            activation_id: The activation ID
            timeout: Maximum time to wait in seconds
            interval: Time between checks in seconds
            get_text: Whether to get the full SMS text

        Returns:
            Tuple[bool, Union[str, Dict]]: (success, result)
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            success, result = self.get_status(activation_id, get_text)

            if success:
                return True, result
            elif result == "STATUS_WAIT_CODE":
                print(f"Waiting for SMS... (elapsed: {int(time.time() - start_time)}s)")
                time.sleep(interval)
            else:
                return False, result

        return False, "Timeout waiting for SMS"

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


def rent_number(api_key="1FnYUz38JilRDCbFcoxIRsYvuWCGH1", service="go", max_price=0.2, areas=None, carriers=None):
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

    return phone_number, activation_id, client



def get_code_dev(phone_number, activation_id, client, timeout=90, interval=5, get_text=False):
    print(f"Waiting for SMS code (timeout: {timeout}s, checking every {interval}s)...")
    try:
        success, result = client.wait_for_code(
            activation_id=activation_id,
            timeout=timeout,
            interval=interval,
            get_text=get_text
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

            return result['code']
        else:
            print("No code received. Canceling number rental...")
            success, message = client.cancel_number(activation_id)
            if success:
                print(message)
            else:
                print(f"Error canceling number: {message}")

            return False
    except KeyboardInterrupt:
        print("\nOperation canceled by user. Canceling number rental...")
        success, message = client.cancel_number(activation_id)
        if success:
            print(message)
        else:
            print(f"Error canceling number: {message}")

        return False

def update_sheet(webmail, password, data):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creden = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Program Files\seventh-capsule-370110-0fe38e91ed21.json', scopes=scopes)

    file = gspread.authorize(creden)

    # Open the desired workbook
    work_book = file.open('New listing process')

    # Choose the desired sheet within the workbook
    sheet = work_book.worksheet('Sheet1')

    # Update the cells in the selected sheet
    sheet.append_row([webmail, password, data])

def main():
    driver = connect_to_incognitor()
    email_domain= ''
    login_webmail= f''
    login_password= ''
    status_data= login_to_webmail(driver, login_webmail, login_password)
    if status_data==True:
        index=0
        while True:
            index +=1
            print(f"Processing Row {index}_________________________")
            first_name, last_name, username, password= generate_name()
            webmail= f"{username}@{email_domain}"
            for _ in range(3):
                try:
                    status= create_webmail_from_cpanel(username, password, email_domain)
                    if status:
                        break
                except:
                    pass
            if status == False:
                break
            status2, data= register_on_google_workspace(driver, webmail, password, first_name, last_name, email_domain)
            if data== 'quit':
                break
            update_sheet(webmail, password, data)
            time.sleep(15)
            index+=1
            if index % 10 == 0:
                driver.quit()
                
                driver= connect_to_incognitor()
                status_data= login_to_webmail(driver, login_webmail, login_password)

        


    input('aloo')

if __name__ == '__main__':
    main()
