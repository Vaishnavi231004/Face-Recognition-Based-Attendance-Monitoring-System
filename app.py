import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file
import subprocess
import os
from download import download_csv  # Import function from download.py
import csv

app = Flask(__name__)



@app.route('/timetable')
def show_timetable():
    timetable = []
    with open(r'C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\timetable.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            timetable.append(row)

    return render_template('timetable.html', timetable=timetable)
# Load timetable from CSV
def load_timetable():
    df = pd.read_csv(r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\timetable.csv")
    return df.to_dict(orient="records")  # Convert to list of dictionaries

@app.route('/')
def landing():
    return render_template('landing1.html')

@app.route('/home')
def home():
    timetable = load_timetable()
    return render_template('index1.html', timetable=timetable)

@app.route('/capture_photo', methods=['GET'])
def capture_photo():
    try:
        subprocess.run(["python", r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\takephoto.py"], check=True)
        return jsonify({"message": "Photo captured successfully!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to capture photo", "details": str(e)}), 500

@app.route('/start_attendance', methods=['GET'])
def start_attendance():
    try:
        subprocess.Popen(["python", r"C:\Users\mohite\Desktop\sem6\face-recognition-main\face-recognition-main\facerec.py"])
        return jsonify({"message": "Real-Time Attendance Started!"})
    except Exception as e:
        return jsonify({"error": "Failed to start face recognition", "details": str(e)}), 500

@app.route('/download_csv', methods=['GET'])
def download_csv_file():
    month = request.args.get('month')
    if not month:
        return jsonify({"error": "month not provided"}), 400

    filename = f"Attendance_{month}.csv"

    if not os.path.exists(filename):
        return jsonify({"error": "File not found"}), 404

    try:
        return send_file(filename, as_attachment=True, mimetype="text/csv",
                         download_name=f"Attendance_{month}.csv")
    except Exception as e:
        return jsonify({"error": "Error while sending CSV file", "details": str(e)}), 500

@app.route('/download_pdf', methods=['GET'])
def download_pdf_file():
    month = request.args.get('month')
    if not month:
        return jsonify({"error": "Month not provided"}), 400

    csv_file = f"Attendance_{month}.csv"
    pdf_file = f"Attendance_{month}.pdf"

    if not os.path.exists(csv_file):
        return jsonify({"error": "CSV file not found, cannot generate PDF"}), 404

    if not os.path.exists(pdf_file):  # Only generate if not already present
        try:
            download_csv(csv_file, pdf_file, month)
        except Exception as e:
            return jsonify({"error": "Failed to generate PDF", "details": str(e)}), 500

    try:
        return send_file(pdf_file, as_attachment=True, mimetype="application/pdf",
                         download_name=f"Attendance_{month}.pdf")
    except Exception as e:
        return jsonify({"error": "Error while sending PDF file", "details": str(e)}), 500


print(app.url_map)


if __name__ == '__main__':
    app.run(debug=True)
