from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Create uploads folder if not exists
if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")

# Initialize database
def init_db():
    conn = sqlite3.connect("animals_v3.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal TEXT,
        location TEXT,
        description TEXT,
        image TEXT,
        helper_name TEXT,
        helper_contact TEXT
    )
    """)

    conn.commit()
    conn.close()

# Call DB init
init_db()


# Homepage
@app.route('/')
def home():
    conn = sqlite3.connect("animals_v3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cases")
    data = cursor.fetchall()

    conn.close()

    return render_template("index.html", cases=data)


# Post new case
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        animal = request.form['animal']
        location = request.form['location']
        description = request.form['description']

        image = request.files['image']
        filename = image.filename

        image.save(os.path.join('static/uploads', filename))

        conn = sqlite3.connect("animals_v3.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO cases (animal, location, description, image) VALUES (?,?,?,?)",
            (animal, location, description, filename)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template("post.html")


# Help route
@app.route('/help/<int:case_id>', methods=['GET', 'POST'])
def help_case(case_id):
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']

        conn = sqlite3.connect("animals_v3.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE cases SET helper_name=?, helper_contact=? WHERE id=?",
            (name, contact, case_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template("help.html")


# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
