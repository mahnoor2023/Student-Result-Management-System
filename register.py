from tkinter import *
from tkinter import messagebox
import sqlite3
import re


class RegisterClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System - Register")
        self.root.geometry("900x550+250+120")
        self.root.config(bg="#13294b")
        self.root.resizable(False, False)
        self.root.focus_force()

        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_confirm = StringVar()

        # ====Left Panel=====
        left = Frame(self.root, bg="#0d1f33")
        left.place(x=0, y=0, width=350, height=550)

        Label(left, text="SRMS", font=("Goudy Old Style", 36, "bold"),
              bg="#0d1f33", fg="white").place(x=90, y=200)
        Label(left, text="Student Result\nManagement System",
              font=("Goudy Old Style", 14), bg="#0d1f33", fg="#9fb3c8",
              justify=CENTER).place(x=60, y=270)

        # ====Right Panel (Register Form)=====
        right = Frame(self.root, bg="white")
        right.place(x=350, y=0, width=550, height=550)

        Label(right, text="CREATE ACCOUNT", font=("Goudy Old Style", 24, "bold"),
              bg="white", fg="#13294b").place(x=140, y=50)

        Label(right, text="EMAIL ADDRESS", font=("Goudy Old Style", 11, "bold"),
              bg="white", fg="#555555").place(x=120, y=140)
        Entry(right, textvariable=self.var_email,
              font=("Goudy Old Style", 13), bg="#eeeeee", relief=FLAT
              ).place(x=120, y=165, width=320, height=32)

        Label(right, text="PASSWORD", font=("Goudy Old Style", 11, "bold"),
              bg="white", fg="#555555").place(x=120, y=215)
        Entry(right, textvariable=self.var_password, show="*",
              font=("Goudy Old Style", 13), bg="#eeeeee", relief=FLAT
              ).place(x=120, y=240, width=320, height=32)

        Label(right, text="CONFIRM PASSWORD", font=("Goudy Old Style", 11, "bold"),
              bg="white", fg="#555555").place(x=120, y=290)
        Entry(right, textvariable=self.var_confirm, show="*",
              font=("Goudy Old Style", 13), bg="#eeeeee", relief=FLAT
              ).place(x=120, y=315, width=320, height=32)

        Button(right, text="Register", font=("Goudy Old Style", 14, "bold"),
               bg="#c2185b", fg="white", cursor="hand2",
               command=self.register_user
               ).place(x=120, y=375, width=320, height=42)

        back_lbl = Label(right, text="Already have an account? Login here",
                          font=("Goudy Old Style", 11, "underline"),
                          bg="white", fg="#1565c0", cursor="hand2")
        back_lbl.place(x=120, y=430)
        back_lbl.bind("<Button-1>", lambda event: self.back_to_login())

        self.root.bind("<Return>", lambda event: self.register_user())

    def get_connection(self):
        return sqlite3.connect(database="rms.db")

    def register_user(self):
        email = self.var_email.get().strip()
        password = self.var_password.get().strip()
        confirm = self.var_confirm.get().strip()

        if not email or not password or not confirm:
            messagebox.showwarning("Warning", "Please fill all fields", parent=self.root)
            return

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_pattern, email):
            messagebox.showwarning("Warning", "Please enter a valid email address", parent=self.root)
            return

        if len(password) < 6:
            messagebox.showwarning("Warning", "Password must be at least 6 characters long", parent=self.root)
            return

        if password != confirm:
            messagebox.showwarning("Warning", "Password and Confirm Password do not match", parent=self.root)
            return

        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM admin WHERE email=?", (email,))
            if cur.fetchone():
                con.close()
                messagebox.showerror("Error", "An account with this email already exists", parent=self.root)
                return

            cur.execute("INSERT INTO admin (email, password) VALUES (?,?)", (email, password))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Account created successfully. Please login.", parent=self.root)
            self.back_to_login()
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def back_to_login(self):
        self.root.destroy()
        from login import LoginClass
        login_root = Tk()
        LoginClass(login_root)
        login_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = RegisterClass(root)
    root.mainloop()
