import os
import csv
from datetime import datetime

ATTENDANCE_FOLDER = "Attendance"
os.makedirs(ATTENDANCE_FOLDER, exist_ok=True)

def save_attendance(enrollment, name):
    """
    Appends attendance of a student to today's attendance CSV.
    Skips if already marked present.
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    filename = f"{ATTENDANCE_FOLDER}/Attendance_{date_str}.csv"

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Enrollment'] == str(enrollment):
                    return  # Already marked

    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Enrollment', 'Name', 'Date', 'Time'])
        writer.writerow([enrollment, name, date_str, time_str])
