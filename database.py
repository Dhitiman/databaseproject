import sqlite3
import streamlit as st

# Function to create the SQLite database and tables if they don't exist
def create_database_and_tables():
    try:
        # Connect to SQLite in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # Create the Department table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Department (
                department_id INTEGER PRIMARY KEY,
                department_name TEXT NOT NULL
            )
        """)

        # Create Student table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Student (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                date_of_birth TEXT,
                email TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES Department(department_id)
            )
        """)

        # Create Course table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT,
                department_id INTEGER,
                credits INTEGER,
                FOREIGN KEY (department_id) REFERENCES Department(department_id)
            )
        """)

        # Create Enrollment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enrollment (
                enrollment_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                course_id INTEGER,
                enrollment_date TEXT,
                grade TEXT,
                FOREIGN KEY (student_id) REFERENCES Student(student_id),
                FOREIGN KEY (course_id) REFERENCES Course(course_id)
            )
        """)

        # Commit and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and tables created successfully.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

# Function to get a SQLite database connection
def get_db_connection():
    return sqlite3.connect(':memory:')

# Function to add department
def add_department(department_id, department_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Department (department_id, department_name) VALUES (?, ?)",
                       (department_id, department_name))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Department added successfully!")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to add student
def add_student(student_id, first_name, last_name, dob, email, department_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Student (student_id, first_name, last_name, date_of_birth, email, department_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, first_name, last_name, dob, email, department_id))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Student added successfully!")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to display students
def display_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, first_name, last_name, date_of_birth, email FROM Student")
        students = cursor.fetchall()
        cursor.close()
        conn.close()

        if students:
            st.write("### Students List")
            st.table(students)
        else:
            st.write("No students found.")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to display courses
def display_courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name, credits FROM Course")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()

        if courses:
            st.write("### Courses List")
            st.table(courses)
        else:
            st.write("No courses found.")
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Streamlit UI
def main():
    st.title("Student Database Management System")
    
    # Initialize database and tables on app load
    create_database_and_tables()

    menu = ["Add Department", "Add Student", "Display Students", "Display Courses"]
    choice = st.sidebar.selectbox("Select an option", menu)
    
    if choice == "Add Department":
        st.subheader("Add Department")
        department_id = st.number_input("Department ID", min_value=1)
        department_name = st.text_input("Department Name")
        
        if st.button("Add Department"):
            if department_id and department_name:
                add_department(department_id, department_name)
            else:
                st.error("Please provide valid data for department.")
    
    elif choice == "Add Student":
        st.subheader("Add Student")
        student_id = st.number_input("Student ID", min_value=1)
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        dob = st.date_input("Date of Birth").strftime('%Y-%m-%d')
        email = st.text_input("Email")
        department_id = st.number_input("Department ID", min_value=1)
        
        if st.button("Add Student"):
            if student_id and first_name and last_name and dob and email and department_id:
                add_student(student_id, first_name, last_name, dob, email, department_id)
            else:
                st.error("Please provide valid data for student.")
    
    elif choice == "Display Students":
        st.subheader("Student List")
        display_students()
    
    elif choice == "Display Courses":
        st.subheader("Course List")
        display_courses()


# Run the Streamlit app
if __name__ == "__main__":
    main()
