import csv
from signalwire.rest import Client as SignalWireClient

# 🔧 Configure your SignalWire credentials
PROJECT_ID = '3509ead4-4fb4-4e10-89e0-20a67ba1a9e4'
API_TOKEN = 'PT8bd4f3a80e4557b7c3fd3ca96061917ecb27ca99a119e499'
SPACE_URL = 'oneill1906.signalwire.com'

client = SignalWireClient(PROJECT_ID, API_TOKEN, signalwire_space_url=SPACE_URL)

# 📄 Load phone numbers and names from CSV
CSV_FILE = 'phone_numbers.csv'

with open(CSV_FILE, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            phone_number = row[0].strip()
            new_name = row[1].strip()
        except:
            continue

        try:
            # 🔄 Update the phone number's friendly name
            number = client.incoming_phone_numbers \
                .list(phone_number=phone_number, limit=1)

            if not number:
                print(f"Phone number {phone_number} not found.")
                continue

            updated = client.incoming_phone_numbers(number[0].sid) \
                .update(friendly_name=new_name)

            print(f"Updated {phone_number} to '{new_name}'")
        except Exception as e:
            print(f"Failed to update {phone_number}: {e}")