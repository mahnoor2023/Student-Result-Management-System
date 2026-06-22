from tkinter import *
from tkinter import messagebox
import sqlite3


class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System - Login")
        self.root.geometry("900x500+250+150")
        self.root.config(bg="#13294b")
        self.root.resizable(False, False)
        self.root.focus_force()

        self.var_email = StringVar()
        self.var_password = StringVar()

        # ====Left Panel=====
        left = Frame(self.root, bg="#0d1f33")
        left.place(x=0, y=0, width=350, height=500)

        Label(left, text="SRMS", font=("Goudy Old Style", 36, "bold"),
              bg="#0d1f33", fg="white").place(x=90, y=180)
        Label(left, text="Student Result\nManagement System",
              font=("Goudy Old Style", 14), bg="#0d1f33", fg="#9fb3c8",
              justify=CENTER).place(x=60, y=250)

        # ====Right Panel (Login Form)=====
        right = Frame(self.root, bg="white")
        right.place(x=350, y=0, width=550, height=500)

        Label(right, text="LOGIN HERE", font=("Goudy Old Style", 24, "bold"),
              bg="white", fg="#13294b").place(x=170, y=60)

        Label(right, text="EMAIL ADDRESS", font=("Goudy Old Style", 11, "bold"),
              bg="white", fg="#555555").place(x=120, y=150)
        Entry(right, textvariable=self.var_email,
              font=("Goudy Old Style", 13), bg="#eeeeee", relief=FLAT
              ).place(x=120, y=175, width=320, height=32)

        Label(right, text="PASSWORD", font=("Goudy Old Style", 11, "bold"),
              bg="white", fg="#555555").place(x=120, y=225)
        Entry(right, textvariable=self.var_password, show="*",
              font=("Goudy Old Style", 13), bg="#eeeeee", relief=FLAT
              ).place(x=120, y=250, width=320, height=32)

        Button(right, text="Login", font=("Goudy Old Style", 14, "bold"),
               bg="#c2185b", fg="white", cursor="hand2",
               command=self.login_check
               ).place(x=120, y=310, width=320, height=42)

        register_lbl = Label(right, text="Register new Account?",
                              font=("Goudy Old Style", 11, "underline"),
                              bg="white", fg="#1565c0", cursor="hand2")
        register_lbl.place(x=120, y=365)
        register_lbl.bind("<Button-1>", lambda event: self.open_register())

        self.root.bind("<Return>", lambda event: self.login_check())

    def get_connection(self):
        return sqlite3.connect(database="rms.db")

    def login_check(self):
        email = self.var_email.get().strip()
        password = self.var_password.get().strip()

        if not email or not password:
            messagebox.showwarning("Warning", "Please enter Email and Password", parent=self.root)
            return

        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM admin WHERE email=? AND password=?", (email, password))
            row = cur.fetchone()
            con.close()

            if row:
                self.root.destroy()
                open_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def open_register(self):
        self.root.destroy()
        from register import RegisterClass
        reg_root = Tk()
        RegisterClass(reg_root)
        reg_root.mainloop()


def open_dashboard():
    from dashboard import RMS
    dash_root = Tk()
    RMS(dash_root)
    dash_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = LoginClass(root)
    root.mainloop()
