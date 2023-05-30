from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

# create the student model


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/showall', methods=['GET', 'POST'])
def show_all():
    if request.method == 'POST':
        student_id = request.json['id']
        student = Student.query.filter_by(id=student_id).first()
        if student:
            student.name = request.json['stuName']
            student.age = request.json['stuAge']
            student.email = request.json['stuEmail']
            db.session.add(student)
            db.session.commit()

    if request.method == 'GET' and 'id' in request.args:
        student_id = int(request.args['id'])
        student = Student.query.filter_by(id=student_id).first()
        if student:
            db.session.delete(student)
            db.session.commit()

    students = Student.query.all()

    return render_template('showall.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)
