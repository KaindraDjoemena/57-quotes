from flask import Flask, render_template
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)

# Initialize database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Make tables
class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    nip = db.Column(db.Integer)
    nuptk = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<id: {self.id}, name: {self.name}, sex: {self.sex}, image_path: {self.image}, nip: {self.nip}, nuptk: {self.nuptk}, time: {self.time}>"

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, nullable=False)
    quote = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<id: {self.id}, teacher_id: {self.teacher_id}, quote: {self.quote}, source: {self.source}, time: {self.time}>"


@app.route("/")
def index():
    fetched_data = Quotes.query.all()

    # See if there is data
    if len(fetched_data) < 1:
        return render_template("error.html", message="database error")

    random_data = random.choice(fetched_data)
    quote = random_data.quote
    teacher_id = random_data.teacher_id

    teacher_data = Teachers.query.filter_by(id=teacher_id).all()[0]
    if teacher_data.sex == "m":
        name = "Pak " + teacher_data.name.capitalize()
    if teacher_data.sex == "f":
        name = "Bu " + teacher_data.name.capitalize()
    

    return render_template("index.html", image=random_data.image, quote='"'+quote+'"', teacher=name)