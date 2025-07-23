import imaplib
import email
import os
import re
from email.header import decode_header

def fetch_emails_and_extract_code(username, password, limit=5):
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('mail.financedon.online', 993)
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

if __name__ == "__main__":
    username = "michelle_arnold60@ventfluefix.store"  # Your email address
    password = 'hKB0q!r5l1*I'  # Your password

    code = fetch_emails_and_extract_code(username, password, limit=20)
    if code:
        print(f"\nVerification code: {code}")
        
        
    else:
        print("Code not found, retrying...")
        
    # Fetch the latest email and extract Google Workspace invite link
    # invite_link = fetch_emails_and_extract_link(username, password, limit=20)
    # if invite_link:
    #     print(invite_link)
    # else:
    #     print("\nNo Google Workspace invite link found in the latest emails.")
