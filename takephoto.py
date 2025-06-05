import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import numpy as np



# Path to save the encrypted image
save_path = r'C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\photos'

# Load the encryption key
with open(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\secret.key", 'rb') as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)


# Function to encrypt an image
def encrypt_image(image):
    # Convert the image to a byte array
    is_success, buffer = cv2.imencode(".jpg", image)
    if not is_success:
        raise ValueError("Failed to encode image to byte array")
    
    image_bytes = buffer.tobytes()
    
    # Encrypt the byte array
    encrypted_bytes = cipher_suite.encrypt(image_bytes)
    
    return encrypted_bytes

# Initialize the webcam
cap = cv2.VideoCapture(0)
print("Webcam initialized")

# Load the face detector (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # If a face is detected, break the loop and capture the image
    if len(faces) > 0:
        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Show the frame with the detected face(s)
        cv2.imshow('Face Detected', frame)
        cv2.waitKey(5000)  # Wait for 1 second to show the detected face

        # Release the camera and close any open windows
        cap.release()
        cv2.destroyAllWindows()

        # Create a pop-up window to enter the roll number of the person
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        person_roll = simpledialog.askinteger("Input", "Enter the roll number of the person:", parent=root)

        # Check if the user provided a roll number
        if person_roll is not None:
            # Create the complete file path
            file_path = os.path.join(save_path, f"{person_roll}.jpg.enc")

            # Check if a file with the same name already exists
            if os.path.exists(file_path):
                messagebox.showerror("Error", f"A person with roll number {person_roll} already exists.")
            else:
                # Encrypt the image
                encrypted_image = encrypt_image(frame)
                # Save the encrypted image
                with open(file_path, 'wb') as file:
                    file.write(encrypted_image)
                
                messagebox.showinfo("Success", f"Image saved and encrypted as {file_path}")

        break

# Release the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
