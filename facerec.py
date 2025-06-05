import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\yolov8n-face-lindevs.pt")

# Load known face encodings
encodeListKnown = np.load(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\encodings.npy", allow_pickle=True)
with open(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\classNames.csv", mode="r") as file:
    classNames = file.read().splitlines()

# Load timetable
def load_timetable(filename):
    timetable = {}
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            day = row["Day"].strip()
            time_slot = row["TimeSlot"].strip().replace(" ", "")
            subject = row["Subject"].strip()
            if day not in timetable:
                timetable[day] = {}
            timetable[day][time_slot] = subject
    return timetable

timetable = load_timetable(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\timetable.csv")
present_students_per_subject = {}
face_timers = {}

# Get current lecture
def get_current_subject():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")

    if current_day in timetable:
        for time_slot, subject in timetable[current_day].items():
            start_time, end_time = time_slot.split("-")
            if start_time <= current_time < end_time:
                return subject
    return None

# Function to log attendance
def log_attendance(name):
    global present_students_per_subject

    subject = get_current_subject()
    if subject is None:
        print("❌ No active lecture at this time.")
        return

    if subject not in present_students_per_subject:
        present_students_per_subject[subject] = set()

    if name not in present_students_per_subject[subject]:
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")
        year_month = datetime.now().strftime("%Y-%m")
        filename = f"Attendance_{year_month}.csv"

        file_exists = os.path.isfile(filename)

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Time", "Student_ID", "Subject"])

            writer.writerow([date, time, name, subject])

        present_students_per_subject[subject].add(name)
        print(f"✅ Attendance logged for {name} in {subject}")
    else:
        print(f"⚠️ {name} is already marked present for {subject} today.")

# Generate Monthly Report
def generate_monthly_report():
    year_month = datetime.now().strftime("%Y-%m")
    report_file = f"Attendance_{year_month}.csv"
    attendance_records = []

    if not os.path.isfile(report_file):
        print("📌 No attendance data found for this month.")
        return

    with open(report_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            attendance_records.append(row)

    with open(report_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Student_ID", "Subject"])
        writer.writerows(attendance_records)

    print(f"📊 Monthly attendance report updated: {report_file}")

# Start real-time detection
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    results = model(img, verbose=False)

    facesCurFrame = []
    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box[:4])
            facesCurFrame.append((y1, x2, y2, x1))

    encodesCurFrame = face_recognition.face_encodings(img, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            roll_number = os.path.splitext(classNames[matchIndex])[0]
            current_time = datetime.now()

            if roll_number not in face_timers:
                face_timers[roll_number] = current_time
            else:
                elapsed_time = (current_time - face_timers[roll_number]).total_seconds()
                if elapsed_time >= 4:
                    log_attendance(roll_number)
                    del face_timers[roll_number]

            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, roll_number, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    detected_rolls = {os.path.splitext(classNames[np.argmin(face_recognition.face_distance(encodeListKnown, encode))])[0] for encode in encodesCurFrame}
    face_timers = {roll: time for roll, time in face_timers.items() if roll in detected_rolls}

    cv2.imshow("YOLOv8 Face Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        generate_monthly_report()
        break

cap.release()
cv2.destroyAllWindows()
