from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:/testdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'hi'

db = SQLAlchemy(app)


class Student(db.Model):
    studentid = db.Column(db.Integer, primary_key=True)
    studentfirstname = db.Column(db.String(80), unique=True, nullable=False)
    studentlastname = db.Column(db.String(120), nullable=False)
    studentadd = db.Column(db.String(120), nullable=False)
    studentcity = db.Column(db.String(120), nullable=False)
    studentstate = db.Column(db.String(120), nullable=False)
    studentemail = db.Column(db.String(120), nullable=False)
    bacourse= db.Column(db.String(120), nullable=False)

    def __init__(self, studentid, studentfirstname, studentlastname, studentadd, studentcity,studentstate, studentemail, bacourse ):
        self.studentid = studentid
        self.studentfirstname = studentfirstname
        self.studentlastname = studentlastname
        self.studentadd = studentadd
        self.studentcity = studentcity
        self.studentstate = studentstate
        self.studentemail = studentemail
        self.bacourse = bacourse


@app.route('/')
def home():
    return '<a href="/addperson"><button> Click here </button></a>'



@app.route("/addperson")
def addperson():
    return render_template("index.html")


@app.route("/personadd", methods=['POST'])
def personadd():
    studentid = request.form["studentid"]
    studentfirstname = request.form["studentfirstname"]
    studentlastname = request.form["studentlastname"]
    studentadd = request.form["studentadd"]
    studentcity = request.form["studentcity"]
    studentstate = request.form["studentstate"]
    studentemail = request.form["studentemail"]
    bacourse = request.form["bacourse"]
    entry = Student(studentid,studentfirstname, studentlastname, studentadd, studentcity,studentstate, studentemail, bacourse )
    db.session.add(entry)
    db.session.commit()

    return render_template("index.html")


if __name__ == '__main__':
    db.create_all()
    app.run()