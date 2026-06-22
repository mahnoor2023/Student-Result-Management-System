from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from course import CourseClass
from student import StudentClass
from result import ResultClass
from view_result import ViewResultClass

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # === Logo Image ===
        img = Image.open("pic2.jpeg")
        img = img.resize((45, 45), Image.LANCZOS)
        self.logo_dash = ImageTk.PhotoImage(img)

        # === Title Bar ===
        title = Label(
            self.root,
            text="  Student Result Management System",
            image=self.logo_dash,
            compound=LEFT,
            font=("Goudy Old Style", 20, "bold"),
            bg="#033054",
            fg="white"
        )
        title.place(x=0, y=0, relwidth=1, height=55)

        # === Menu ===
        M_fRAME = LabelFrame(self.root, text="Menus", font=("times new roman", 15), bg="white")
        M_fRAME.place(x=10, y=70, width=1340, height=80)

        Button(M_fRAME, text="Course", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_course).place(x=20, y=5, width=200, height=40)
        Button(M_fRAME, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_student).place(x=240, y=5, width=200, height=40)
        Button(M_fRAME, text="Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_result).place(x=460, y=5, width=200, height=40)
        Button(M_fRAME, text="View Student Results", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.view_results).place(x=680, y=5, width=200, height=40)
        Button(M_fRAME, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.logout).place(x=900, y=5, width=200, height=40)
        Button(M_fRAME, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.exit_app).place(x=1120, y=5, width=200, height=40)

        # === Content Window (Background Image) ===
        self.bg_img = Image.open("pic1.PNG")
        self.bg_img = self.bg_img.resize((1340, 360), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg = Label(self.root, image=self.bg_img)
        self.lbl_bg.place(x=0, y=160, width=1340, height=360)

        # === Update Details (center mein, image ke neeche) ===
        self.lbl_course = Label(self.root, text="Total Course\n[0]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_course.place(x=175, y=535, width=300, height=100)

        self.lbl_student = Label(self.root, text="Total Students\n[0]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_student.place(x=520, y=535, width=300, height=100)

        self.lbl_Result = Label(self.root, text="Total Results\n[0]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_Result.place(x=865, y=535, width=300, height=100)

        # === Footer ===
        footer = Label(self.root, text="SRMS - Student Result Management System\nContact us for any technical Issue: 987xxxx01", font=("goudy old style", 12), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        # === Load live counts ===
        self.load_counts()

    # ================================================================
    # Menu Button Actions
    # ================================================================
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.close_child(self.new_win))

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.close_child(self.new_win))

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ResultClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.close_child(self.new_win))

    def view_results(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ViewResultClass(self.new_win)
        self.new_win.protocol("WM_DELETE_WINDOW", lambda: self.close_child(self.new_win))

    def close_child(self, win):
        win.destroy()
        self.load_counts()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root):
            self.root.destroy()
            from login import LoginClass
            login_root = Tk()
            LoginClass(login_root)
            login_root.mainloop()

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.destroy()

    # ================================================================
    # Dashboard Counts
    # ================================================================
    def load_counts(self):
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM course")
            course_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM student")
            student_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM result")
            result_count = cur.fetchone()[0]
            con.close()

            self.lbl_course.config(text=f"Total Course\n[{course_count}]")
            self.lbl_student.config(text=f"Total Students\n[{student_count}]")
            self.lbl_Result.config(text=f"Total Results\n[{result_count}]")
        except Exception:
            pass


if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()