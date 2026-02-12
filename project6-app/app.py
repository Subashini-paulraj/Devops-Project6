from flask import Flask, request, render_template_string
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = "project6-mysql"


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            location VARCHAR(100),
            course VARCHAR(100)
        )
    """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    student_data = None

    try:
        init_db()

        if request.method == "POST":

            # Insert Student
            if "submit" in request.form:
                name = request.form["name"]
                location = request.form["location"]
                course = request.form["course"]

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO students (name, location, course) VALUES (%s, %s, %s)",
                    (name, location, course)
                )
                conn.commit()
                conn.close()

                message = "Student added successfully!"

            # Search Student
            if "search" in request.form:
                student_id = request.form["student_id"]

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
                student_data = cursor.fetchone()
                conn.close()

        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Management System</title>
            <style>
                body {
                    font-family: Arial;
                    background-color: #f4f6f9;
                    padding: 40px;
                }
                h1 {
                    color: #2c3e50;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    width: 500px;
                }
                input {
                    width: 100%;
                    padding: 8px;
                    margin: 5px 0 10px 0;
                }
                button {
                    padding: 10px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #2980b9;
                }
                .result {
                    margin-top: 20px;
                    background: #ecf0f1;
                    padding: 10px;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>

            <div class="container">
                <h1>🎓 Student Management System</h1>

                <h3>Add Student</h3>
                <form method="POST">
                    Name:
                    <input type="text" name="name" required>

                    Location:
                    <input type="text" name="location" required>

                    Course:
                    <input type="text" name="course" required>

                    <button type="submit" name="submit">Submit</button>
                </form>

                <hr>

                <h3>Search Student</h3>
                <form method="POST">
                    Search Student ID:
                    <input type="number" name="student_id" required>

                    <button type="submit" name="search">Search</button>
                </form>

                {% if message %}
                    <div class="result">{{ message }}</div>
                {% endif %}

                {% if student_data %}
                    <div class="result">
                        <h4>Student Details:</h4>
                        ID: {{ student_data.id }} <br>
                        Name: {{ student_data.name }} <br>
                        Location: {{ student_data.location }} <br>
                        Course: {{ student_data.course }}
                    </div>
                {% endif %}

            </div>

        </body>
        </html>
        """, message=message, student_data=student_data)

    except Exception as e:
        return str(e)


@app.route("/health")
def health():
    return "Healthy", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
