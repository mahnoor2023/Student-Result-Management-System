from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x500+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====Variables=====
        self.var_roll       = StringVar()
        self.var_name       = StringVar()
        self.var_dob        = StringVar()
        self.var_contact    = StringVar()
        self.var_email      = StringVar()
        self.var_gender     = StringVar()
        self.var_course     = StringVar()
        self.var_admission  = StringVar()
        self.var_state      = StringVar()
        self.var_city       = StringVar()
        self.var_pin        = StringVar()
        self.var_search     = StringVar()

        # ====Title Bar=====
        Label(
            self.root,
            text="  Manage Student Details",
            font=("Goudy Old Style", 20, "bold"),
            bg="#033054", fg="white"
        ).place(x=0, y=0, width=1200, height=40)

        # ====Left Form Frame=====
        Label(self.root, text="Roll No.",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=10, y=55)
        Entry(self.root, textvariable=self.var_roll,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=140, y=55, width=180, height=28)

        Label(self.root, text="D.O.B(dd-mm-yyyy)",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=400, y=55)
        Entry(self.root, textvariable=self.var_dob,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=620, y=55, width=180, height=28)

        Label(self.root, text="Name",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=10, y=95)
        Entry(self.root, textvariable=self.var_name,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=140, y=95, width=180, height=28)

        Label(self.root, text="Contact No.",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=400, y=95)
        Entry(self.root, textvariable=self.var_contact,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=620, y=95, width=180, height=28)

        Label(self.root, text="Email",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=10, y=135)
        Entry(self.root, textvariable=self.var_email,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=140, y=135, width=180, height=28)

        Label(self.root, text="Select Course",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=400, y=135)
        self.course_combo = ttk.Combobox(self.root, textvariable=self.var_course,
              font=("Goudy Old Style", 12), state="readonly")
        self.course_combo.place(x=620, y=135, width=180, height=28)

        Label(self.root, text="Gender",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=10, y=175)
        self.gender_combo = ttk.Combobox(self.root, textvariable=self.var_gender,
              font=("Goudy Old Style", 12), state="readonly",
              values=("Male", "Female", "Other"))
        self.gender_combo.place(x=140, y=175, width=180, height=28)

        Label(self.root, text="Admission Date",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=400, y=175)
        Entry(self.root, textvariable=self.var_admission,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=620, y=175, width=180, height=28)

        Label(self.root, text="State",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=10, y=215)
        Entry(self.root, textvariable=self.var_state,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=140, y=215, width=180, height=28)

        Label(self.root, text="City",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=400, y=215)
        Entry(self.root, textvariable=self.var_city,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=460, y=215, width=140, height=28)

        Label(self.root, text="Pin Code",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=620, y=215)
        Entry(self.root, textvariable=self.var_pin,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=700, y=215, width=100, height=28)

        Label(self.root, text="Address",
              font=("Goudy Old Style", 13, "bold"), bg="white").place(x=10, y=255)
        self.txt_address = Text(self.root,
              font=("Goudy Old Style", 13), bg="lightyellow")
        self.txt_address.place(x=140, y=255, width=660, height=70)

        # ====Buttons=====
        Button(self.root, text="Save",
               font=("Goudy Old Style", 14, "bold"),
               bg="#2196f3", fg="white", cursor="hand2",
               command=self.save_data
               ).place(x=140, y=345, width=110, height=38)

        Button(self.root, text="Update",
               font=("Goudy Old Style", 14, "bold"),
               bg="#4caf50", fg="white", cursor="hand2",
               command=self.update_data
               ).place(x=260, y=345, width=110, height=38)

        Button(self.root, text="Delete",
               font=("Goudy Old Style", 14, "bold"),
               bg="#f44336", fg="white", cursor="hand2",
               command=self.delete_data
               ).place(x=380, y=345, width=110, height=38)

        Button(self.root, text="Clear",
               font=("Goudy Old Style", 14, "bold"),
               bg="#607d8b", fg="white", cursor="hand2",
               command=self.clear_fields
               ).place(x=500, y=345, width=110, height=38)

        # ====Search Panel (right side)=====
        Label(self.root, text="Search | Roll No.",
              font=("Goudy Old Style", 14, "bold"), bg="white"
              ).place(x=830, y=55)

        Entry(self.root, textvariable=self.var_search,
              font=("Goudy Old Style", 13, "bold"), bg="lightyellow"
              ).place(x=1010, y=58, width=110, height=28)

        Button(self.root, text="Search",
               font=("Goudy Old Style", 12, "bold"),
               bg="#03a9f4", fg="white", cursor="hand2",
               command=self.search_data
               ).place(x=1130, y=58, width=60, height=28)

        # ====Content / Treeview=====
        self.S_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.S_Frame.place(x=830, y=95, width=360, height=290)

        scrolly = Scrollbar(self.S_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.S_Frame, orient=HORIZONTAL)

        self.StudentTable = ttk.Treeview(
            self.S_Frame,
            columns=("roll", "name", "email", "gender", "dob"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        self.StudentTable.heading("roll",   text="Roll No.")
        self.StudentTable.heading("name",   text="Name")
        self.StudentTable.heading("email",  text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("dob",    text="D.O.B")
        self.StudentTable["show"] = "headings"

        self.StudentTable.column("roll",   width=70)
        self.StudentTable.column("name",   width=90)
        self.StudentTable.column("email",  width=120)
        self.StudentTable.column("gender", width=70)
        self.StudentTable.column("dob",    width=80)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_cursor)

        # ====Load data on startup=====
        self.load_courses()
        self.fetch_data()

    # ================================================================
    # Database Methods
    # ================================================================
    def get_connection(self):
        con = sqlite3.connect(database="rms.db")
        return con

    def load_courses(self):
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            con.close()
            self.course_combo["values"] = [r[0] for r in rows]
        except Exception:
            self.course_combo["values"] = []

    def fetch_data(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute("SELECT sid, roll, name, email, gender, dob FROM student")
        rows = cur.fetchall()
        con.close()

        self.StudentTable.delete(*self.StudentTable.get_children())
        for row in rows:
            # row[0] is sid (hidden), show roll,name,email,gender,dob
            self.StudentTable.insert("", END, values=row[1:])

    def validate_fields(self):
        if not self.var_roll.get().strip():
            messagebox.showwarning("Warning", "Please enter Roll No.", parent=self.root)
            return False
        if not self.var_name.get().strip():
            messagebox.showwarning("Warning", "Please enter Name", parent=self.root)
            return False
        return True

    def save_data(self):
        if not self.validate_fields():
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                """INSERT INTO student
                   (roll, name, email, gender, dob, contact, admission,
                    course, state, city, pin, address)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    self.var_roll.get().strip(), self.var_name.get().strip(),
                    self.var_email.get().strip(), self.var_gender.get().strip(),
                    self.var_dob.get().strip(), self.var_contact.get().strip(),
                    self.var_admission.get().strip(), self.var_course.get().strip(),
                    self.var_state.get().strip(), self.var_city.get().strip(),
                    self.var_pin.get().strip(), self.txt_address.get("1.0", END).strip()
                )
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Student saved successfully", parent=self.root)
            self.clear_fields()
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def update_data(self):
        selected = self.StudentTable.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to update", parent=self.root)
            return
        if not self.validate_fields():
            return
        roll_in_table = self.StudentTable.item(selected[0], "values")[0]
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                """UPDATE student SET roll=?, name=?, email=?, gender=?, dob=?,
                   contact=?, admission=?, course=?, state=?, city=?, pin=?, address=?
                   WHERE roll=?""",
                (
                    self.var_roll.get().strip(), self.var_name.get().strip(),
                    self.var_email.get().strip(), self.var_gender.get().strip(),
                    self.var_dob.get().strip(), self.var_contact.get().strip(),
                    self.var_admission.get().strip(), self.var_course.get().strip(),
                    self.var_state.get().strip(), self.var_city.get().strip(),
                    self.var_pin.get().strip(), self.txt_address.get("1.0", END).strip(),
                    roll_in_table
                )
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
            self.clear_fields()
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def delete_data(self):
        selected = self.StudentTable.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete", parent=self.root)
            return
        roll_in_table = self.StudentTable.item(selected[0], "values")[0]

        if messagebox.askyesno("Confirm", "Delete this record?", parent=self.root):
            try:
                con = self.get_connection()
                cur = con.cursor()
                cur.execute("DELETE FROM student WHERE roll=?", (roll_in_table,))
                con.commit()
                con.close()
                self.clear_fields()
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def search_data(self):
        query = self.var_search.get().strip()
        if not query:
            self.fetch_data()
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                "SELECT sid, roll, name, email, gender, dob FROM student WHERE roll LIKE ?",
                (f"%{query}%",)
            )
            rows = cur.fetchall()
            con.close()

            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row[1:])

            if not rows:
                messagebox.showinfo("Result", "No matching student found", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_course.set("")
        self.var_admission.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")
        self.txt_address.delete("1.0", END)
        self.load_courses()
        self.fetch_data()

    def get_cursor(self, event):
        selected = self.StudentTable.selection()
        if not selected:
            return
        roll_in_table = self.StudentTable.item(selected[0], "values")[0]
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM student WHERE roll=?", (roll_in_table,))
            row = cur.fetchone()
            con.close()
            if row:
                # sid, roll, name, email, gender, dob, contact, admission, course, state, city, pin, address
                self.var_roll.set(row[1])
                self.var_name.set(row[2])
                self.var_email.set(row[3])
                self.var_gender.set(row[4])
                self.var_dob.set(row[5])
                self.var_contact.set(row[6])
                self.var_admission.set(row[7])
                self.var_course.set(row[8])
                self.var_state.set(row[9])
                self.var_city.set(row[10])
                self.var_pin.set(row[11])
                self.txt_address.delete("1.0", END)
                self.txt_address.insert("1.0", row[12] if row[12] else "")
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()
