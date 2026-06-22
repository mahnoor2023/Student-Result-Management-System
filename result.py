from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3


class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("900x500+150+150")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====Variables=====
        self.var_roll    = StringVar()
        self.var_name    = StringVar()
        self.var_course  = StringVar()
        self.var_obtained = StringVar()
        self.var_full    = StringVar()

        # ====Title Bar=====
        Label(
            self.root,
            text="Add Student Result",
            font=("Goudy Old Style", 22, "bold"),
            bg="#f5a623", fg="white"
        ).place(x=0, y=0, relwidth=1, height=45)

        # ====Left Form=====
        Label(self.root, text="Select Student",
              font=("Goudy Old Style", 14, "bold"), bg="white").place(x=40, y=80)
        self.roll_combo = ttk.Combobox(self.root, textvariable=self.var_roll,
              font=("Goudy Old Style", 12), state="readonly")
        self.roll_combo.place(x=220, y=80, width=140, height=28)

        Button(self.root, text="Search",
               font=("Goudy Old Style", 12, "bold"),
               bg="#2196f3", fg="white", cursor="hand2",
               command=self.search_student
               ).place(x=375, y=80, width=80, height=28)

        Label(self.root, text="Name",
              font=("Goudy Old Style", 14, "bold"), bg="white").place(x=40, y=130)
        Entry(self.root, textvariable=self.var_name, state="readonly",
              font=("Goudy Old Style", 13), bg="#eeeeee"
              ).place(x=220, y=130, width=235, height=28)

        Label(self.root, text="Course",
              font=("Goudy Old Style", 14, "bold"), bg="white").place(x=40, y=180)
        Entry(self.root, textvariable=self.var_course, state="readonly",
              font=("Goudy Old Style", 13), bg="#eeeeee"
              ).place(x=220, y=180, width=235, height=28)

        Label(self.root, text="Marks Obtained",
              font=("Goudy Old Style", 14, "bold"), bg="white").place(x=40, y=230)
        Entry(self.root, textvariable=self.var_obtained,
              font=("Goudy Old Style", 13), bg="lightyellow"
              ).place(x=220, y=230, width=235, height=28)

        Label(self.root, text="Full Marks",
              font=("Goudy Old Style", 14, "bold"), bg="white").place(x=40, y=280)
        Entry(self.root, textvariable=self.var_full,
              font=("Goudy Old Style", 13), bg="lightyellow"
              ).place(x=220, y=280, width=235, height=28)

        # ====Right Side Image=====
        try:
            img = Image.open("pic2.jpeg")
            img = img.resize((260, 200), Image.LANCZOS)
            self.result_img = ImageTk.PhotoImage(img)
            Label(self.root, image=self.result_img, bg="white").place(x=560, y=90)
        except Exception:
            pass

        # ====Buttons=====
        Button(self.root, text="Submit",
               font=("Goudy Old Style", 14, "bold"),
               bg="#4caf50", fg="white", cursor="hand2",
               command=self.submit_result
               ).place(x=220, y=350, width=110, height=38)

        Button(self.root, text="Clear",
               font=("Goudy Old Style", 14, "bold"),
               bg="#607d8b", fg="white", cursor="hand2",
               command=self.clear_fields
               ).place(x=345, y=350, width=110, height=38)

        self.load_roll_numbers()

    # ================================================================
    # Database Methods
    # ================================================================
    def get_connection(self):
        return sqlite3.connect(database="rms.db")

    def load_roll_numbers(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()
            con.close()
            self.roll_combo["values"] = [r[0] for r in rows]
        except Exception:
            self.roll_combo["values"] = []

    def search_student(self):
        roll = self.var_roll.get().strip()
        if not roll:
            messagebox.showwarning("Warning", "Please select a Roll No.", parent=self.root)
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT name, course FROM student WHERE roll=?", (roll,))
            row = cur.fetchone()
            con.close()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showinfo("Result", "No student found with this Roll No.", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def submit_result(self):
        roll = self.var_roll.get().strip()
        name = self.var_name.get().strip()
        course = self.var_course.get().strip()
        obtained = self.var_obtained.get().strip()
        full = self.var_full.get().strip()

        if not roll or not name:
            messagebox.showwarning("Warning", "Please select and search a student first", parent=self.root)
            return
        if not obtained or not full:
            messagebox.showwarning("Warning", "Please enter Marks Obtained and Full Marks", parent=self.root)
            return

        try:
            obtained_val = float(obtained)
            full_val = float(full)
            if full_val <= 0:
                messagebox.showwarning("Warning", "Full Marks must be greater than 0", parent=self.root)
                return
            if obtained_val < 0 or obtained_val > full_val:
                messagebox.showwarning("Warning", "Marks Obtained must be between 0 and Full Marks", parent=self.root)
                return
        except ValueError:
            messagebox.showwarning("Warning", "Marks must be numeric", parent=self.root)
            return

        percentage = round((obtained_val / full_val) * 100, 2)

        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                """INSERT INTO result (roll, name, course, marks_obtained, full_marks, percentage)
                   VALUES (?,?,?,?,?,?)""",
                (roll, name, course, obtained, full, f"{percentage}%")
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", f"Result saved successfully\nPercentage: {percentage}%", parent=self.root)
            self.clear_fields()
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_obtained.set("")
        self.var_full.set("")
        self.load_roll_numbers()


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()
