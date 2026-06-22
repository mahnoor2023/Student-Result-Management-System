Student Result Management System (SRMS)
=========================================

FILES
-----
login.py        -> START HERE. Run this file to launch the app (Login screen).
register.py     -> Create a new admin account (opened via "Register new Account?" link).
dashboard.py    -> Main dashboard, opened automatically after successful login.
course.py       -> Course management window  (Course button)
student.py      -> Student management window (Student button)
result.py       -> Add student result window  (Result button)
view_result.py  -> View/search/delete results (View Student Results button)
create_db.py    -> Creates rms.db with all required tables.
rms.db          -> SQLite database (course, student, result, admin tables).
pic1.PNG        -> Background image used on the dashboard.
pic2.jpeg       -> Logo image (dashboard title bar + result page).
Doc1.docx       -> Reference/screenshot document.

HOW TO RUN
----------
1. Install requirements:
   pip install pillow

2. Keep ALL files (including rms.db, pic1.PNG, pic2.jpeg) in the SAME folder.
   The app loads images/database using relative paths.

3. Run:
   python login.py

4. Login with the default admin account:
   Email:    admin@rms.com
   Password: admin123

   OR click "Register new Account?" on the login screen to create your own
   admin account (email + password, minimum 6 characters), then log in
   with it.

5. From the dashboard, use the menu buttons:
   - Course               -> Add / Update / Delete / Search courses
   - Student               -> Add / Update / Delete / Search students
   - Result                -> Select a student by Roll No, enter marks,
                              percentage is calculated automatically
   - View Student Results  -> Search results by Roll No, delete a record
   - Logout                -> Confirms, then returns to the Login screen
   - Exit                  -> Confirms, then closes the application

NOTES
-----
- To reset the database at any time, delete rms.db and run:
      python create_db.py
  This recreates all tables and adds the default admin login above.

- In the Result window, before adding a result you must first add the
  student in the Student window (Result form looks up Name/Course by Roll No).

- Marks Obtained cannot exceed Full Marks -- the form validates this and
  shows a warning if you try.

- The dashboard's "Total Course / Total Students / Total Results" counters
  refresh automatically whenever you close a sub-window (Course/Student/
  Result/View Results).
