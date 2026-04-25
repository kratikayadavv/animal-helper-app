from flask import Flask, render_template
from flask import request
import sqlite3
from flask import redirect, url_for
import os

app= Flask(__name__) #flask app created and __name__ is where the app is located 

@app.route('/') # maps url path to a function ,route = URL path , / means homepage . it shows index.html
def home():
    conn = sqlite3.connect("animals_v3.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cases")
    data = cursor.fetchall()

    conn.close()

    return render_template("index.html", cases=data)

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

if __name__ == "__main__":
    app.run()
