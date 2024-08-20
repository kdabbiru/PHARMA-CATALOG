import hashlib
import time
import json
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

# Initialize smart contract conditions (simulated)
smart_contracts = {
    "manufacture": {"condition": "drug_name != ''"},
    "package": {"condition": "drug_batch_number != ''"},
    "ship": {"condition": "receiver_id != ''"},
    "receive": {"condition": "shipment_id != ''"},
    "dispense": {"condition": "drug_id != ''"}
}

# Function to simulate blockchain (same as before)
blockchain = []

# AES encryption setup
encryption_key = b'Sixteen byte key'

def encrypt_data(data):
    cipher = AES.new(encryption_key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_data(encrypted_data):
    decoded = b64decode(encrypted_data.encode('utf-8'))
    nonce = decoded[:16]
    ciphertext = decoded[16:]
    cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')

# Example function to check smart contract conditions
def check_smart_contract(contract_name, **kwargs):
    condition = smart_contracts[contract_name]["condition"]
    for key, value in kwargs.items():
        condition = condition.replace(key, f"'{value}'")
    return eval(condition)

# Functions for managing the supply chain (enhanced)
def manufacture_drug():
    print("\n--- Manufacture Drug ---")
    drug_name = input("Enter drug name: ")
    if check_smart_contract("manufacture", drug_name=drug_name):
        batch_number = str(hashlib.sha256(drug_name.encode()).hexdigest()[:10])
        encrypted_batch_number = encrypt_data(batch_number)
        blockchain.append({"action": "Manufactured", "drug_name": drug_name, "batch_number": encrypted_batch_number, "timestamp": time.time()})
        print(f"Drug '{drug_name}' has been manufactured with batch number {batch_number}.")
    else:
        print("Smart contract condition not met. Manufacture failed.")

def package_drug():
    print("\n--- Package Drug ---")
    for idx, block in enumerate(blockchain):
        if block["action"] == "Manufactured":
            print(f"{idx+1}. {block['drug_name']} - Batch: {decrypt_data(block['batch_number'])}")
    selection = int(input("Select drug to package: ")) - 1
    selected_block = blockchain[selection]
    if check_smart_contract("package", drug_batch_number=selected_block['batch_number']):
        blockchain.append({"action": "Packaged", "drug_name": selected_block['drug_name'], "batch_number": selected_block['batch_number'], "timestamp": time.time()})
        print(f"Drug '{selected_block['drug_name']}' has been packaged.")
    else:
        print("Smart contract condition not met. Packaging failed.")

def ship_drug():
    print("\n--- Ship Drug ---")
    for idx, block in enumerate(blockchain):
        if block["action"] == "Packaged":
            print(f"{idx+1}. {block['drug_name']} - Batch: {decrypt_data(block['batch_number'])}")
    selection = int(input("Select drug to ship: ")) - 1
    selected_block = blockchain[selection]
    receiver_id = input("Enter receiver ID: ")
    if check_smart_contract("ship", receiver_id=receiver_id):
        blockchain.append({"action": "Shipped", "drug_name": selected_block['drug_name'], "batch_number": selected_block['batch_number'], "receiver_id": receiver_id, "timestamp": time.time()})
        print(f"Drug '{selected_block['drug_name']}' has been shipped to receiver ID {receiver_id}.")
    else:
        print("Smart contract condition not met. Shipping failed.")

def receive_drug():
    print("\n--- Receive Drug ---")
    for idx, block in enumerate(blockchain):
        if block["action"] == "Shipped":
            print(f"{idx+1}. {block['drug_name']} - Batch: {decrypt_data(block['batch_number'])} - Receiver ID: {block['receiver_id']}")
    selection = int(input("Select drug to receive: ")) - 1
    selected_block = blockchain[selection]
    shipment_id = input("Enter shipment ID: ")
    if check_smart_contract("receive", shipment_id=shipment_id):
        blockchain.append({"action": "Received", "drug_name": selected_block['drug_name'], "batch_number": selected_block['batch_number'], "shipment_id": shipment_id, "timestamp": time.time()})
        print(f"Drug '{selected_block['drug_name']}' has been received with shipment ID {shipment_id}.")
    else:
        print("Smart contract condition not met. Receiving failed.")

def dispense_drug():
    print("\n--- Dispense Drug ---")
    for idx, block in enumerate(blockchain):
        if block["action"] == "Received":
            print(f"{idx+1}. {block['drug_name']} - Batch: {decrypt_data(block['batch_number'])}")
    selection = int(input("Select drug to dispense: ")) - 1
    selected_block = blockchain[selection]
    drug_id = input("Enter drug ID: ")
    if check_smart_contract("dispense", drug_id=drug_id):
        blockchain.append({"action": "Dispensed", "drug_name": selected_block['drug_name'], "batch_number": selected_block['batch_number'], "drug_id": drug_id, "timestamp": time.time()})
        print(f"Drug '{selected_block['drug_name']}' has been dispensed.")
    else:
        print("Smart contract condition not met. Dispensing failed.")

def audit_supply_chain():
    print("\n--- Audit Supply Chain ---")
    print(f"{'Action':<12} | {'Drug Name':<15} | {'Batch Number':<25} | {'Timestamp':<20} | {'Extra Info'}")
    print("="*85)
    for block in blockchain:
        extra_info = block.get("receiver_id", "") or block.get("shipment_id", "") or block.get("drug_id", "")
        print(f"{block['action']:<12} | {block['drug_name']:<15} | {decrypt_data(block['batch_number']):<25} | {time.ctime(block['timestamp']):<20} | {extra_info}")

def pharma_supply_chain_system():
    while True:
        print("\nPharma Supply Chain Management System")
        print("1. Manufacture Drug")
        print("2. Package Drug")
        print("3. Ship Drug")
        print("4. Receive Drug")
        print("5. Dispense Drug")
        print("6. Audit Supply Chain")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            manufacture_drug()
        elif choice == '2':
            package_drug()
        elif choice == '3':
            ship_drug()
        elif choice == '4':
            receive_drug()
        elif choice == '5':
            dispense_drug()
        elif choice == '6':
            audit_supply_chain()
        elif choice == '7':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the system
pharma_supply_chain_system()
