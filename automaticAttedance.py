import tkinter as tk
from tkinter import *
import os, cv2
import pandas as pd
import datetime
import time
from save_attendance import save_attendance

# === File Paths ===
haarcasecade_path = r"haarcascade_frontalface_default.xml"
trainimagelabel_path = r"TrainingImageLabel/Trainner.yml"
studentdetail_path = r"StudentDetails.csv"

def subjectChoose(text_to_speech):
    def FillAttendance():
        subject_name = tx.get().strip()
        if not subject_name:
            text_to_speech("Please enter the subject name!")
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read(trainimagelabel_path)
        except:
            msg = "Model not found. Please train the model first."
            Notifica.configure(text=msg, bg="black", fg="yellow", font=("times", 15, "bold"))
            Notifica.place(x=20, y=250)
            text_to_speech(msg)
            return

        face_cascade = cv2.CascadeClassifier(haarcasecade_path)
        student_df = pd.read_csv(studentdetail_path)

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX

        attendance = pd.DataFrame(columns=["Enrollment", "Name"])

        start_time = time.time()
        end_time = start_time + 20  # 20 seconds

        while time.time() < end_time:
            _, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 70:
                    name = student_df.loc[student_df["Enrollment"] == Id]["Name"].values
                    name_str = str(name[0]) if len(name) > 0 else "Unknown"
                    save_attendance(Id, name_str)
                    attendance.loc[len(attendance)] = [Id, name_str]

                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 260, 0), 4)
                    cv2.putText(img, f"{Id} - {name_str}", (x + h, y), font, 1, (255, 255, 0), 4)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 25, 255), 7)
                    cv2.putText(img, "Unknown", (x + h, y), font, 1, (0, 25, 255), 4)

            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
            cv2.imshow("Filling Attendance...", img)

            if cv2.waitKey(30) & 0xFF == 27:
                break

        cam.release()
        cv2.destroyAllWindows()

        msg = f"Attendance marked successfully for subject: {subject_name}"
        Notifica.configure(text=msg, bg="black", fg="yellow", font=("times", 15, "bold"), relief=RIDGE, bd=5)
        Notifica.place(x=20, y=250)
        text_to_speech(msg)

        # Display attendance summary
        import tkinter as tk
        root = tk.Tk()
        root.title(f"Attendance Summary - {subject_name}")
        root.configure(background="black")

        tk.Label(root, text="Today's Attendance", bg="black", fg="white", font=("Times", 20, "bold")).pack(pady=10)

        for index, row in attendance.iterrows():
            tk.Label(root, text=f"{row['Enrollment']} - {row['Name']}", bg="black", fg="yellow", font=("Times", 15)).pack()

        root.mainloop()

    def Attf():
        sub = tx.get().strip()
        if not sub:
            text_to_speech("Please enter the subject name!")
        else:
            os.startfile(os.path.join(os.getcwd(), "Attendance"))

    # === GUI ===
    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    Label(subject, text="Enter the Subject Name", bg="black", fg="green", font=("arial", 25)).pack(pady=15)

    global Notifica
    Notifica = Label(subject, text="", bg="yellow", fg="black", font=("times", 15, "bold"))

    Label(subject, text="Subject:", bg="black", fg="yellow", font=("times new roman", 15)).place(x=50, y=100)
    global tx
    tx = Entry(subject, width=15, bd=5, bg="black", fg="yellow", font=("times", 25, "bold"))
    tx.place(x=190, y=100)

    Button(subject, text="Fill Attendance", command=FillAttendance, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=12).place(x=190, y=170)
    Button(subject, text="Check Sheets", command=Attf, font=("times new roman", 15), bg="black", fg="yellow", height=2, width=12).place(x=360, y=170)

    subject.mainloop()
