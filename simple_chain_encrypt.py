import json
import os

SAVE_FILE = "saved_codes.json"

# Load existing data (if any)
def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

# Save updated data
def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Encrypt a letter using a code and a number between 1–7
def encrypt_letter(letter, code, number):
    combined = f"{letter}:{code}:{number}"
    encrypted = "".join(chr((ord(c) + number) % 256) for c in combined)
    return encrypted

# Decrypt a letter using the same code and number (in reverse order)
def decrypt_letter(encrypted, code, number):
    decrypted = "".join(chr((ord(c) - number) % 256) for c in encrypted)
    letter, stored_code, stored_number = decrypted.split(":")
    if stored_code == code and stored_number == str(number):
        return letter
    else:
        return "[Wrong code or number]"

# Main program
def main():
    data = load_data()

    print("🔐 Personal Encryption Tool")
    print("Type 'encrypt' to encrypt, 'decrypt' to decrypt, or 'exit' to quit.\n")

    while True:
        choice = input("Enter mode (encrypt/decrypt/exit): ").strip().lower()

        if choice == "encrypt":
            message_name = input("Enter a name for this encryption session: ").strip()
            if message_name not in data:
                data[message_name] = []

            while True:
                letter = input("Enter a letter (or type 'finish' to end): ").strip()
                if letter.lower() == "finish":
                    break
                code = input("Enter your secret code (letters or numbers): ").strip()
                number = int(input("Enter a number (1–7): ").strip())

                encrypted = encrypt_letter(letter, code, number)
                data[message_name].append({
                    "encrypted": encrypted,
                    "number": number
                })
                print(f"Encrypted: {encrypted}")

            save_data(data)
            print(f"Session '{message_name}' saved successfully!\n")

        elif choice == "decrypt":
            message_name = input("Enter the session name to decrypt: ").strip()
            if message_name not in data:
                print("No saved data with that name.\n")
                continue

            print(f"Decrypting session '{message_name}'...")
            decrypted_message = ""

            for item in data[message_name]:
                encrypted = item["encrypted"]
                number = item["number"]

                code = input(f"Enter the code you used for letter with number {number}: ").strip()
                decrypted = decrypt_letter(encrypted, code, number)
                decrypted_message += decrypted

            print("\n✅ Decrypted Message:", decrypted_message, "\n")

        elif choice == "exit":
            print("Goodbye! 🔒")
            break

        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()
