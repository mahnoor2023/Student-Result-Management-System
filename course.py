from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====Variables=====
        self.var_courseName = StringVar()
        self.var_duration   = StringVar()
        self.var_charges    = StringVar()
        self.var_search     = StringVar()

        # ====Title Bar=====
        Label(
            self.root,
            text="  Manage Course Details",
            font=("Goudy Old Style", 20, "bold"),
            bg="#033054", fg="white"
        ).place(x=0, y=0, width=1200, height=40)

        # ====Labels=====
        Label(self.root, text="Course Name",
              font=("Goudy Old Style", 15, "bold"), bg="white").place(x=10, y=60)
        Label(self.root, text="Duration",
              font=("Goudy Old Style", 15, "bold"), bg="white").place(x=10, y=100)
        Label(self.root, text="Charges",
              font=("Goudy Old Style", 15, "bold"), bg="white").place(x=10, y=140)
        Label(self.root, text="Description",
              font=("Goudy Old Style", 15, "bold"), bg="white").place(x=10, y=180)

        # ====Entry Fields=====
        Entry(self.root, textvariable=self.var_courseName,
              font=("Goudy Old Style", 15, "bold"), bg="lightyellow"
              ).place(x=150, y=60, width=300, height=30)

        Entry(self.root, textvariable=self.var_duration,
              font=("Goudy Old Style", 15, "bold"), bg="lightyellow"
              ).place(x=150, y=100, width=300, height=30)

        Entry(self.root, textvariable=self.var_charges,
              font=("Goudy Old Style", 15, "bold"), bg="lightyellow"
              ).place(x=150, y=140, width=300, height=30)

        self.txt_description = Text(self.root,
              font=("Goudy Old Style", 15, "bold"), bg="lightyellow")
        self.txt_description.place(x=150, y=180, width=300, height=120)

        # ====Buttons=====
        Button(self.root, text="Save",
               font=("Goudy Old Style", 15, "bold"),
               bg="#2196f3", fg="white", cursor="hand2",
               command=self.save_data
               ).place(x=150, y=400, width=110, height=40)

        Button(self.root, text="Update",
               font=("Goudy Old Style", 15, "bold"),
               bg="#4caf50", fg="white", cursor="hand2",
               command=self.update_data
               ).place(x=270, y=400, width=110, height=40)

        Button(self.root, text="Delete",
               font=("Goudy Old Style", 15, "bold"),
               bg="#f44336", fg="white", cursor="hand2",
               command=self.delete_data
               ).place(x=390, y=400, width=110, height=40)

        Button(self.root, text="Clear",
               font=("Goudy Old Style", 15, "bold"),
               bg="#607d8b", fg="white", cursor="hand2",
               command=self.clear_fields
               ).place(x=510, y=400, width=110, height=40)

        # ====Search Panel=====
        Label(self.root, text="Course Name",
              font=("Goudy Old Style", 15, "bold"), bg="white"
              ).place(x=720, y=60)

        Entry(self.root, textvariable=self.var_search,
              font=("Goudy Old Style", 15, "bold"), bg="lightyellow"
              ).place(x=900, y=60, width=200, height=30)

        Button(self.root, text="Search",
               font=("Goudy Old Style", 15, "bold"),
               bg="#03a9f4", fg="white", cursor="hand2",
               command=self.search_data
               ).place(x=1110, y=60, width=80, height=30)

        # ====Content / Treeview=====
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(
            self.C_Frame,
            columns=("cid", "name", "duration", "charges", "description"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid",         text="Course ID")
        self.CourseTable.heading("name",        text="Name")
        self.CourseTable.heading("duration",    text="Duration")
        self.CourseTable.heading("charges",     text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = "headings"

        self.CourseTable.column("cid",         width=80)
        self.CourseTable.column("name",        width=100)
        self.CourseTable.column("duration",    width=80)
        self.CourseTable.column("charges",     width=80)
        self.CourseTable.column("description", width=120)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_cursor)

        # ====Load data on startup=====
        self.fetch_data()

    # ================================================================
    # Database Methods
    # ================================================================
    def get_connection(self):
        con = sqlite3.connect(database="rms.db")
        return con

    def fetch_data(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM course")
        rows = cur.fetchall()
        con.close()

        # Clear table first
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert("", END, values=row)

    def save_data(self):
        name = self.var_courseName.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter Course Name", parent=self.root)
            return
        dur  = self.var_duration.get().strip()
        chg  = self.var_charges.get().strip()
        desc = self.txt_description.get("1.0", END).strip()

        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO course (name, duration, charges, description) VALUES (?,?,?,?)",
                (name, dur, chg, desc)
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Course saved successfully", parent=self.root)
            self.clear_fields()
            self.fetch_data()
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def update_data(self):
        selected = self.CourseTable.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to update", parent=self.root)
            return
        cid  = self.CourseTable.item(selected[0], "values")[0]
        name = self.var_courseName.get().strip()
        dur  = self.var_duration.get().strip()
        chg  = self.var_charges.get().strip()
        desc = self.txt_description.get("1.0", END).strip()

        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                "UPDATE course SET name=?, duration=?, charges=?, description=? WHERE cid=?",
                (name, dur, chg, desc, cid)
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
            self.fetch_data()
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def delete_data(self):
        selected = self.CourseTable.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete", parent=self.root)
            return
        cid = self.CourseTable.item(selected[0], "values")[0]

        if messagebox.askyesno("Confirm", "Delete this record?", parent=self.root):
            try:
                con = self.get_connection()
                cur = con.cursor()
                cur.execute("DELETE FROM course WHERE cid=?", (cid,))
                con.commit()
                con.close()
                self.clear_fields()
                self.fetch_data()
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
            cur.execute("SELECT * FROM course WHERE name LIKE ?", (f"%{query}%",))
            rows = cur.fetchall()
            con.close()

            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)

            if not rows:
                messagebox.showinfo("Result", "No matching course found", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def clear_fields(self):
        self.var_courseName.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0", END)
        self.fetch_data()

    def get_cursor(self, event):
        selected = self.CourseTable.selection()
        if not selected:
            return
        row = self.CourseTable.item(selected[0], "values")
        self.var_courseName.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_description.delete("1.0", END)
        self.txt_description.insert("1.0", row[4])


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()