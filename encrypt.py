from cryptography.fernet import Fernet
import os

# Generate and store the key securely (do this only once)
# key = Fernet.generate_key()
# with open('secret.key', 'wb') as key_file:
#     key_file.write(key)

# Load the key from a secure location
with open(r'C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\secret.key', 'rb') as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

path = 'images'
encrypted_path = 'photos'

# Function to encrypt images
def encrypt_images(path):
    if not os.path.exists(encrypted_path):
        os.makedirs(encrypted_path)

    for image_name in os.listdir(path):
        if image_name.endswith(".jpg") or image_name.endswith(".png"):
            image_path = os.path.join(path, image_name)
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            encrypted_data = cipher_suite.encrypt(image_data)

            # Save encrypted file
            with open(os.path.join(encrypted_path, image_name + '.enc'), 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

# Encrypt images (run once)
encrypt_images(path)
