import os
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

def download_csv(csv_path, pdf_path, date):
    """Converts a CSV file to a PDF file."""
    print(f"📂 Checking file existence: {csv_path}")  # Debugging output
    if not os.path.exists(csv_path):
        print(f"❌ Error: File '{csv_path}' not found.")
        return

    try:
        df = pd.read_csv(csv_path)
        print(f"✅ CSV file loaded successfully! Rows: {len(df)}")  # Debugging output

        if df.empty:
            print("❌ Error: CSV file is empty.")
            return

        # Create a PDF
        c = canvas.Canvas(pdf_path, pagesize=landscape(letter))
        width, height = landscape(letter)
        c.setFont("Helvetica-Bold", 12)

        # Title
        c.drawString(200, height - 40, f"Attendance Report - {date}")

        # Draw table headers
        c.setFont("Helvetica", 10)
        x_offset = 50
        y_offset = height - 80
        row_height = 20
        col_width = (width - 2 * x_offset) / len(df.columns)  # Dynamic column width

        headers = df.columns.tolist()
        for i, header in enumerate(headers):
            c.drawString(x_offset + (i * col_width), y_offset, header)

        # Draw table rows
        for _, row in df.iterrows():
            y_offset -= row_height
            if y_offset < 50:  # Avoid overflowing pages
                c.showPage()
                c.setFont("Helvetica", 10)
                y_offset = height - 50

            for i, value in enumerate(row):
                c.drawString(x_offset + (i * col_width), y_offset, str(value))

        c.save()
        print(f"✅ PDF saved as {pdf_path}")  # Debugging output

    except pd.errors.EmptyDataError:
        print("❌ Error: No data found in CSV file.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

# Ask user for date
if __name__ == "__main__":
    date = input("Enter the date (YYYY-MM-DD): ").strip()
    csv_file = f"Attendance_{date}.csv"  # Example: "Attendance_2025-02-10.csv"
    pdf_file = f"Attendance_{date}.pdf"

    print(f"📂 Processing: {csv_file} → {pdf_file}")  # Debugging output

    # Convert CSV to PDF
    download_csv(csv_file, pdf_file, date)