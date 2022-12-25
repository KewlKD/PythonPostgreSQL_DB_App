from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:flexywitdatech1@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'student'
    studentid = db.Column(db.Integer, primary_key=True)
    studentfirstname = db.Column(db.String(80), unique=True, nullable=False)
    studentlastname = db.Column(db.String(120), nullable=False)
    studentadd = db.Column(db.String(120), nullable=False)
    studentcity = db.Column(db.String(120), nullable=False)
    studentstate = db.Column(db.String(120), nullable=False)
    studentemail = db.Column(db.String(120), nullable=False)
    bacourse= db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<Student %r>" % self.studentfirstname,self.studentlastname

  
@cross_origin()
@app.route('/')
def index():
    return jsonify({"Welcome my PostgreSQL/Flask API"})

@cross_origin()
@app.route('/addstudent', methods = ['POST'])
def create_student():
    student_data = request.json

    studentfirstname = student_data['studentfirstname']
    studentlastname = student_data['studentlastname']
    studentadd = student_data['studentadd']
    studentcity = student_data['studentcity']
    studentstate= student_data['studentstate']
    studentemail = student_data['studentemail']
    bacourse = student_data['bacourse']

    #pet_description = student_data['student_description']
    student = Student(
                  studentfirstname =studentfirstname ,
                  studentlastname = studentlastname, 
                  studentadd = studentadd, 
                  studentcity =studentcity,
                  studentstate= studentstate,
                  studentemail = studentemail,
                  bacourse = bacourse)

    db.session.add(student)
    db.session.commit()
    

    return jsonify({"success": True,"response":"student added"})


@cross_origin()    
@app.route('/getstudent/<studentid>', methods = ['GET'])
def getstudent(studentid):
    student = Student.query.get(studentid)
    del student.__dict__['_sa_instance_state']
    return jsonify(student.__dict__)

@cross_origin()    
@app.route('/getstudents', methods = ['GET'])
def getstudents():
     all_students = []
     students = Student.query.all()
     print(type(students))
     for student in students:
          results = {
                    "studentid":student.studentid,
                    "studentfirstname":student.studentfirstname,
                    "studentlastname":student.studentlastname,
                    "studentadd":student.studentadd,
                    "studentcity":student.studentcity,
                    "studentstate":student.studentstate,
                    "studentemail":student.studentemail,
                    "bacourse":student.bacourse, }
          all_students.append(results)

     return jsonify(
            {
                "success": True,
                "students": all_students,
                "total_students": len(students),
            }
        )


@app.route("/deletestudent/<int:student_id>", methods = ["DELETE"])
def delete_student(studentid):
    student = Student.query.get(studentid)
    if student is None:
        abort(404)
    else:
        db.session.delete(student)
        return jsonify({"success": True, "response": "Student deleted"})
        

    
@app.route("/updatestudent/<int:studentid>", methods = ["PATCH"])
def update_student(studentid):
    student = Student.query.get(studentid)
    studentcity = request.json['studentcity']
    studentstate = request.json['studentstate']

    if student is None:
        abort(404)
    else:
        student.studentcity = studentcity
        student.studentstate = studentstate
        db.session.add(student)
        db.session.commit()
        return jsonify({"success": True, "response": "Student details updated"})
        



if __name__ == '__main__':
    app.run(debug=True,port=4000)
    app.app_context().push()
    db.create_all()