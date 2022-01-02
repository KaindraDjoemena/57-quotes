from flask import Flask, redirect, render_template, request, session
import sqlite3
import random

app = Flask(__name__)
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

@app.route("/")
def index():
    fetched_data = cursor.execute("""SELECT * FROM quotes""").fetchall()

    # See if there is data
    if len(fetched_data) < 1:
        return render_template("error.html", message="database error")

    random_data = random.choice(fetched_data)
    quote = random_data[2]
    teacher_id = random_data[1]

    teacher, image, sex = cursor.execute("""SELECT name, image, sex FROM teachers WHERE id=?""", (teacher_id,)).fetchall()[0]
    if sex == "m":
        name = "Pak " + teacher.capitalize()
    elif sex == "f":
        name = "Bu " + teacher.capitalize()
    print("="*23)
    print(image)

    return render_template("index.html", image=image, quote='"'+quote+'"', teacher=name)