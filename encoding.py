import cv2
import numpy as np
import face_recognition
import os
from cryptography.fernet import Fernet
import csv

# Load the encryption key
with open(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\secret.key", 'rb') as key_file:
    key = key_file.read()

# Initialize the cipher suite with the loaded key
cipher_suite = Fernet(key)

# Function to decrypt an image
def decrypt_image(encrypted_image_path):
    with open(encrypted_image_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    nparr = np.frombuffer(decrypted_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

path = r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\photos"
images = []
classNames = []

# Reading encrypted images from the directory
myList = os.listdir(path)
for cl in myList:
    if cl.endswith('.jpg.enc'):
        decrypted_img = decrypt_image(os.path.join(path, cl))
        images.append(decrypted_img)
        classNames.append(os.path.splitext(cl)[0])  # Store roll number

# Function to find encodings for images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Encoding known faces
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Save the encodings and class names
# Save the encodings and class names IN CLASSNAME.CSV
np.save(r'C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\encodings.npy', encodeListKnown, allow_pickle=True)
with open(r'C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\classNames.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for name in classNames:  # Write each roll number on a new line
        writer.writerow([name])  # Each roll number as a single-item list

print("Encodings saved successfully.")

