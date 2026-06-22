from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class ViewResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("950x500+120+150")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====Variables=====
        self.var_search = StringVar()

        # ====Title Bar=====
        Label(
            self.root,
            text="View Student Results",
            font=("Goudy Old Style", 22, "bold"),
            bg="#f5a623", fg="white"
        ).place(x=0, y=0, relwidth=1, height=45)

        # ====Search Panel=====
        Label(self.root, text="Search By | Roll No.",
              font=("Goudy Old Style", 14, "bold"), bg="white"
              ).place(x=40, y=70)

        Entry(self.root, textvariable=self.var_search,
              font=("Goudy Old Style", 13), bg="lightyellow"
              ).place(x=270, y=70, width=200, height=28)

        Button(self.root, text="Search",
               font=("Goudy Old Style", 12, "bold"),
               bg="#2196f3", fg="white", cursor="hand2",
               command=self.search_data
               ).place(x=490, y=70, width=80, height=28)

        Button(self.root, text="Clear",
               font=("Goudy Old Style", 12, "bold"),
               bg="#607d8b", fg="white", cursor="hand2",
               command=self.clear_search
               ).place(x=580, y=70, width=80, height=28)

        # ====Table=====
        self.R_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.R_Frame.place(x=40, y=120, width=870, height=300)

        scrolly = Scrollbar(self.R_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.R_Frame, orient=HORIZONTAL)

        self.ResultTable = ttk.Treeview(
            self.R_Frame,
            columns=("rid", "roll", "name", "course", "obtained", "full", "percentage"),
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ResultTable.xview)
        scrolly.config(command=self.ResultTable.yview)

        self.ResultTable.heading("rid",        text="ID")
        self.ResultTable.heading("roll",       text="Roll No")
        self.ResultTable.heading("name",       text="Name")
        self.ResultTable.heading("course",     text="Course")
        self.ResultTable.heading("obtained",   text="Marks Obtained")
        self.ResultTable.heading("full",       text="Total Marks")
        self.ResultTable.heading("percentage", text="Percentage")
        self.ResultTable["show"] = "headings"

        self.ResultTable.column("rid",        width=50)
        self.ResultTable.column("roll",       width=90)
        self.ResultTable.column("name",       width=130)
        self.ResultTable.column("course",     width=120)
        self.ResultTable.column("obtained",   width=130)
        self.ResultTable.column("full",       width=110)
        self.ResultTable.column("percentage", width=110)

        self.ResultTable.pack(fill=BOTH, expand=1)

        # ====Delete Button=====
        Button(self.root, text="Delete",
               font=("Goudy Old Style", 14, "bold"),
               bg="#f44336", fg="white", cursor="hand2",
               command=self.delete_data
               ).place(x=405, y=435, width=140, height=38)

        # ====Load data on startup=====
        self.fetch_data()

    # ================================================================
    # Database Methods
    # ================================================================
    def get_connection(self):
        return sqlite3.connect(database="rms.db")

    def fetch_data(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute("SELECT rid, roll, name, course, marks_obtained, full_marks, percentage FROM result")
        rows = cur.fetchall()
        con.close()

        self.ResultTable.delete(*self.ResultTable.get_children())
        for row in rows:
            self.ResultTable.insert("", END, values=row)

    def search_data(self):
        query = self.var_search.get().strip()
        if not query:
            self.fetch_data()
            return
        try:
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(
                "SELECT rid, roll, name, course, marks_obtained, full_marks, percentage FROM result WHERE roll LIKE ?",
                (f"%{query}%",)
            )
            rows = cur.fetchall()
            con.close()

            self.ResultTable.delete(*self.ResultTable.get_children())
            for row in rows:
                self.ResultTable.insert("", END, values=row)

            if not rows:
                messagebox.showinfo("Result", "No result found for this Roll No.", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)

    def clear_search(self):
        self.var_search.set("")
        self.fetch_data()

    def delete_data(self):
        selected = self.ResultTable.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete", parent=self.root)
            return
        rid = self.ResultTable.item(selected[0], "values")[0]

        if messagebox.askyesno("Confirm", "Delete this result record?", parent=self.root):
            try:
                con = self.get_connection()
                cur = con.cursor()
                cur.execute("DELETE FROM result WHERE rid=?", (rid,))
                con.commit()
                con.close()
                self.fetch_data()
            except Exception as es:
                messagebox.showerror("Error", f"Error: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = ViewResultClass(root)
    root.mainloop()
