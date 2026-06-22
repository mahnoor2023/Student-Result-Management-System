import sqlite3

def create_db():
    con = sqlite3.connect(database='rms.db')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS course (
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, duration TEXT, charges TEXT, description TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS student (
        sid INTEGER PRIMARY KEY AUTOINCREMENT,
        roll TEXT, name TEXT, email TEXT, gender TEXT,
        dob TEXT, contact TEXT, admission TEXT,
        course TEXT, state TEXT, city TEXT,
        pin TEXT, address TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS result (
        rid INTEGER PRIMARY KEY AUTOINCREMENT,
        roll TEXT, name TEXT, course TEXT,
        marks_obtained TEXT, full_marks TEXT, percentage TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS admin (
        aid INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT, password TEXT
    )""")

    # Default admin
    cur.execute("SELECT * FROM admin WHERE email='admin@rms.com'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (email,password) VALUES ('admin@rms.com','admin123')")

    con.commit()
    con.close()

create_db()