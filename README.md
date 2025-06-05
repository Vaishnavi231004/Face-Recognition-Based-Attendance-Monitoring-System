Face Recognition-Based Attendance Monitoring System
---------------------------------------------------------------------------------------------
A machine learning-based smart attendance system that integrates real-time facial 
recognition, AES data encryption, and a fully functional web-based analytics dashboard.
Designed to automate attendance marking, secure data handling, and provide an intuitive 
interface .
----------------------------------------------------------------------------------------------
Features
•	Real-time face detection and recognition using OpenCV
•	AES-encrypted data storage and transmission
•	Faculty login and authentication system
•	Interactive dashboards for attendance visualization
•	CSV report generation
•	Optimized for varying lighting and facial orientations
•	Modular Flask-based backend and dynamic frontend
---------------------------------------------------------------------------------------------
Tech Stack
•	Python, OpenCV, Flask
•	AES Encryption
•	HTML, CSS, JavaScript
•	Matplotlib, Plotly (for data visualization)
--------------------------------------------------------------------------------------------
Project Structure
face-attendance-system/
├── static/ # CSS, JS, Images
├── templates/ # HTML 
├── photos/ # Stored face images
├── Attendance_2025-04.csv # Logged attendance data monthly in csv form
├── Attendance_2025-04.pdf # Logged attendance data monthly in pdf form
├── app.py # Flask main server file
├── takephoto.py #take new photo of user
├── train_model.py # Encode known faces
├── encryption.py # AES encryption module
├──update1.py # visualization 
├── Attendance_2025-04.csv # Logged attendance data monthly in csv form
├── README.md
├── requirements.txt
├── outputScreenshot #contains output photo of project features
---------------------------------------------------------------------------------------------
Follow these steps to run the project locally on your machine:
1.	Clone the Repository
2.	Install Dependencies
3.	Set Up Directory Structure
4.	Run Streamlit Dashboard: streamlit run update1.py
5.	Run the Flask App: python app.py
----------------------------------------------------------------------------------------------

       

