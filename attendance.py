import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Tk
from PIL import Image, ImageTk
import pyttsx3
import os

# === Import internal project modules ===
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# === Constants ===
HAAR_PATH = r"haarcascade_frontalface_default.xml"
TRAIN_IMAGE_PATH = r"TrainingImage"
TRAIN_LABEL_PATH = r"TrainingImageLabel\Trainner.yml"

# === Text to Speech ===
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# === Input Validator ===
def is_digit_input(in_str, acttyp):
    return in_str.isdigit() if acttyp == "1" else True

# === Error Dialog ===
def show_error_dialog():
    err = Tk()
    err.geometry("400x110")
    err.title("Warning!!")
    err.configure(bg="black")
    tk.Label(err, text="Enrollment & Name required!!!", fg="yellow", bg="black", font=("times", 20)).pack()
    Button(err, text="OK", command=err.destroy, fg="yellow", bg="black", font=("times", 20)).place(x=110, y=50)

# === Register Face UI ===
def open_register_ui():
    reg_win = Tk()
    reg_win.title("Register Student")
    reg_win.geometry("780x480")
    reg_win.configure(bg="black")
    reg_win.resizable(0, 0)

    def take_image():
        er_no = er_entry.get()
        name = name_entry.get()
        takeImage.TakeImage(er_no, name, HAAR_PATH, TRAIN_IMAGE_PATH, notif_label, show_error_dialog, speak)
        er_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)

    def train_image():
        trainImage.TrainImage(HAAR_PATH, TRAIN_IMAGE_PATH, TRAIN_LABEL_PATH, notif_label, speak)

    # --- UI Layout ---
    tk.Label(reg_win, text="Register Your Face", fg="green", bg="black", font=("arial", 30)).pack(pady=10)
    tk.Label(reg_win, text="Enter Details", fg="yellow", bg="black", font=("arial", 24)).pack()

    # Enrollment Field
    tk.Label(reg_win, text="Enrollment No", bg="black", fg="yellow", font=("arial", 14)).place(x=100, y=140)
    er_entry = Entry(reg_win, font=("arial", 18), validate="key", bg="black", fg="yellow")
    er_entry.place(x=270, y=140)
    er_entry["validatecommand"] = (er_entry.register(is_digit_input), "%P", "%d")

    # Name Field
    tk.Label(reg_win, text="Name", bg="black", fg="yellow", font=("arial", 14)).place(x=100, y=200)
    name_entry = Entry(reg_win, font=("arial", 18), bg="black", fg="yellow")
    name_entry.place(x=270, y=200)

    # Notification
    tk.Label(reg_win, text="Notification", bg="black", fg="yellow", font=("arial", 14)).place(x=100, y=260)
    notif_label = tk.Label(reg_win, text="", bg="black", fg="yellow", font=("arial", 14), width=30)
    notif_label.place(x=270, y=260)

    # Buttons
    Button(reg_win, text="Take Image", command=take_image, font=("arial", 16), bg="black", fg="yellow", width=12).place(x=150, y=350)
    Button(reg_win, text="Train Image", command=train_image, font=("arial", 16), bg="black", fg="yellow", width=12).place(x=380, y=350)

# === Home UI ===
def build_home():
    window = Tk()
    window.title("Face Recognition Attendance")
    window.geometry("1280x720")
    window.configure(bg="black")

    # Title and Logo
    logo = Image.open("UI_Image/0001.png").resize((50, 47))
    logo_img = ImageTk.PhotoImage(logo)
    tk.Label(window, image=logo_img, bg="black").place(x=470, y=10)
    tk.Label(window, text="CHANDIGARH UNIVERSITY", font=("CALIBRI", 27), bg="white", fg="red").place(x=525, y=12)

    tk.Label(window, text="GOOD MORNING\nWELCOME TO\nAttendance System", bg="white", fg="blue", font=("Times", 35)).pack(pady=50)

    # Icons
    def load_icon(path, x, y):
        img = ImageTk.PhotoImage(Image.open(path))
        lbl = tk.Label(window, image=img, bg="black")
        lbl.image = img
        lbl.place(x=x, y=y)

    load_icon("UI_Image/register.jpg", 100, 270)
    load_icon("UI_Image/verifyy.jpg", 600, 270)
    load_icon("UI_Image/attendance.jpg", 999, 270)

    # Buttons
    def make_button(text, cmd, x, y):
        Button(window, text=text, command=cmd, font=("times new roman", 16), bg="black", fg="yellow", width=20).place(x=x, y=y)

    make_button("Register a new student", open_register_ui, 100, 520)
    make_button("Take Attendance", lambda: automaticAttedance.subjectChoose(speak), 600, 520)
    make_button("View Attendance", lambda: show_attendance.subjectchoose(speak), 1000, 520)
    make_button("EXIT", window.quit, 600, 660)

    window.mainloop()

# === Run Main UI ===
if __name__ == "__main__":
    build_home()
