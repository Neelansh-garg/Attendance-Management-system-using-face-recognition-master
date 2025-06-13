import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def subjectchoose(text_to_speech=None):
    def open_csv():
        file_path = filedialog.askopenfilename(
            title="Select Attendance File",
            filetypes=[("CSV Files", "*.csv")],
            initialdir=os.path.join(os.getcwd(), "Attendance")  # your attendance folder
        )
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)
            display_attendance(df, file_path)
            if text_to_speech:
                text_to_speech("Attendance loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read the file:\n{e}")

    def display_attendance(dataframe, file_path):
        viewer = tk.Toplevel()
        viewer.title(f"Attendance Viewer - {os.path.basename(file_path)}")
        viewer.geometry("800x600")
        viewer.configure(bg="black")

        tk.Label(viewer, text="Attendance Records", font=("Helvetica", 16), bg="black", fg="white").pack(pady=10)

        text = tk.Text(viewer, wrap="none", font=("Courier", 12), bg="white", fg="black")
        text.pack(fill="both", expand=True)

        text.insert("end", dataframe.to_string(index=False))

    # Start selection UI
    root = tk.Toplevel()
    root.title("View Attendance")
    root.geometry("400x200")
    root.configure(bg="black")

    tk.Label(root, text="Click to Load Attendance CSV", font=("Helvetica", 14), bg="black", fg="white").pack(pady=30)

    tk.Button(root, text="Browse File", command=open_csv, font=("Helvetica", 12), bg="yellow", fg="black").pack()

    if text_to_speech:
        text_to_speech("Please select an attendance file to view.")
