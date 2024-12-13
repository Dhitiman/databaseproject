import mysql.connector
import streamlit as st
from mysql.connector import Error


# Function to create the MySQL database and tables if they don't exist
def create_database_and_tables():
    try:
        # Connect to MySQL (use root or appropriate credentials)
        conn = mysql.connector.connect(
            host='localhost',  # Your MySQL host (use 'localhost' if on your local machine)
            user='root',       # Your MySQL username
            password='',       # Your MySQL password (make sure it's correct)
        )
        cursor = conn.cursor()

        # Create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_database")
        cursor.execute("USE student_database")

        # Create Department table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Department (
                department_id INT PRIMARY KEY,
                department_name VARCHAR(255) NOT NULL
            )
        """)

        # Create Student table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Student (
                student_id INT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                date_of_birth DATE,
                email VARCHAR(255),
                department_id INT,
                FOREIGN KEY (department_id) REFERENCES Department(department_id)
            )
        """)

        # Create Course table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Course (
                course_id INT PRIMARY KEY,
                course_name VARCHAR(255),
                department_id INT,
                credits INT,
                FOREIGN KEY (department_id) REFERENCES Department(department_id)
            )
        """)

        # Create Enrollment table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Enrollment (
                enrollment_id INT PRIMARY KEY,
                student_id INT,
                course_id INT,
                enrollment_date DATE,
                grade VARCHAR(2),
                FOREIGN KEY (student_id) REFERENCES Student(student_id),
                FOREIGN KEY (course_id) REFERENCES Course(course_id)
            )
        """)

        # Commit and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and tables created successfully.")

    except Error as e:
        print(f"Error: {e}")


# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  # Your MySQL host (use 'localhost' if on your local machine)
        user='root',       # Your MySQL username
        password='',       # Your MySQL password (make sure it's correct)
        database='student_database'
    )


# Function to add department
def add_department(department_id, department_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Department (department_id, department_name) VALUES (%s, %s)",
                       (department_id, department_name))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Department added successfully!")
    except Error as e:
        st.error(f"Error: {e}")


# Function to add student
def add_student(student_id, first_name, last_name, dob, email, department_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Student (student_id, first_name, last_name, date_of_birth, email, department_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_id, first_name, last_name, dob, email, department_id))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Student added successfully!")
    except Error as e:
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
    except Error as e:
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
    except Error as e:
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
        dob = st.date_input("Date of Birth")
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
