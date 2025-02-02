from sqlalchemy import JSON, func
from . import db
from datetime import datetime
from flask_login import UserMixin







class Students(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    othername = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    city = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    homephone = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(50), nullable=False)
    placeofbirth = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    enroll_date = db.Column(db.Date, nullable=False)
    previous_school = db.Column(db.String(200), nullable=True)
    medical_information = db.Column(db.String(200), nullable=True) 
    parental_consent = db.Column(db.Boolean, default=True)
    languages_spoken = db.Column(db.String(200), nullable=True)
    image_link = db.Column(db.String(200), default='default.png')
	
    mother_firstname = db.Column(db.String(100), nullable=True)
    mother_lastname = db.Column(db.String(100), nullable=True)
    mother_address = db.Column(db.String(200), nullable=True)
    mother_placeofemployment = db.Column(db.String(200), nullable=True)
    mother_occupation = db.Column(db.String(200), nullable=True)
    mother_town = db.Column(db.String(200), nullable=True)
    mother_state = db.Column(db.String(200), nullable=True)
    mother_cellphonenumber = db.Column(db.String(50), nullable=True)
    mother_homephonenumber = db.Column(db.String(50), nullable=True)
    mother_email = db.Column(db.String(200), nullable=True)
	
	
    father_firstname = db.Column(db.String(100), nullable=True)
    father_lastname = db.Column(db.String(100), nullable=True)
    father_address = db.Column(db.String(200), nullable=True)
    father_placeofemployment = db.Column(db.String(200), nullable=True)
    father_occupation = db.Column(db.String(200), nullable=True)
    father_town = db.Column(db.String(200), nullable=True)
    father_state = db.Column(db.String(200), nullable=True)
    father_cellphonenumber = db.Column(db.String(50), nullable=True)
    father_homephonenumber = db.Column(db.String(50), nullable=True)
    father_email = db.Column(db.String(200), nullable=True)
    
    left_date = db.Column(db.Date, nullable=True)
    key = db.Column(db.String(300), nullable=True)
    role = db.Column(db.String(50), default="Student")
    access = db.Column(db.Boolean, default=False)
    others_expenses = db.Column(JSON, nullable=True)
    unique_payment_account = db.Column(JSON, nullable=True)

    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=True)
    attendance = db.relationship("Student_attendance",backref='student',lazy='dynamic')
    result = db.relationship("Results", backref='student', lazy='dynamic')
    fee = db.relationship("Student_fee", backref='student', lazy='dynamic')
    history = db.relationship("Student_history",backref='student',lazy='dynamic')


    attendance_count = db.Column(JSON, default={})
    years = db.Column(JSON, default={})
    others = db.Column(JSON, default={})
	
    def __repr__(self):
        return f"{self.lastname} {self.firstname}"
	
    def get_id(self):
        return self.username
	
    def full(self):
        return f"{self.firstname} {self.lastname}"


class Student_attendance(db.Model):
	attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	term = db.Column(db.String(50), nullable=False)
	morning_attendance = db.Column(db.DateTime, default=None)
	evening_attendance = db.Column(db.DateTime, default=None)
	comment = db.Column(db.Text, nullable=True)
	status = db.Column(db.String(50), default="absent")
	late_arrival = db.Column(db.Boolean, nullable=True)

	student_username = db.Column(db.String(200),
	                             db.ForeignKey("students.username"),
	                             nullable=False)
	class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)


class Results(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	result_type = db.Column(db.String(100), nullable=False)
	term = db.Column(db.String(50), nullable=False)
	subject = db.Column(db.String(100), nullable=False)
	marks_obtain = db.Column(db.Integer, nullable=False)
	total_mark = db.Column(db.Integer, nullable=False)
	submission_date = db.Column(db.DateTime, nullable=False)
	comment = db.Column(db.String(1000), nullable=True)
	year = db.Column(db.String(100), nullable=True)

	student_username = db.Column(db.String(200),
	                             db.ForeignKey('students.username'),
	                             nullable=False)
	class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)


class Student_fee(db.Model):
	transaction_id = db.Column(db.String(300),
	                           primary_key=True)
	year = db.Column(db.String(20), nullable=False)
	term = db.Column(db.String(50), nullable=False)
	fee_amount = db.Column(db.Integer, nullable=False)
	payment_date = db.Column(db.DateTime, nullable=False)
	payment_method = db.Column(db.String(100), nullable=True)
	payment_status = db.Column(db.String(100), nullable=True)
	payment_note = db.Column(db.String(1000), nullable=True)

	student_username = db.Column(db.String(200),
	                             db.ForeignKey('students.username'),
	                             nullable=False)
	class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)


class Student_history(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	academy_year = db.Column(db.String(50), nullable=False)
	fee_paid = db.Column(JSON, nullable=True)
	exam_result = db.Column(JSON, nullable=True)
	attendance = db.Column(JSON, nullable=True)
	date = db.Column(db.DateTime, default=datetime.utcnow)
	promotion_status = db.Column(db.String(50), nullable=True)
	behavioral_notes = db.Column(db.Text, nullable=True)
	achievements = db.Column(db.String(1000), nullable=True)
	special_programs = db.Column(db.String(1000), nullable=True)

	student_username = db.Column(db.String(200),
	                             db.ForeignKey('students.username'),
	                             nullable=False)
	class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
	teacher_username = db.Column(db.String(200),
	                             db.ForeignKey("teachers.username"),
	                             nullable=True)

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(100), nullable=False)
    class_fee = db.Column(db.Integer, nullable=True)
    class_subjects = db.Column(JSON, nullable=True)
    class_books = db.Column(JSON, nullable=True)
    class_description = db.Column(db.Text, nullable=True)
    class_time_table = db.Column(JSON, nullable=True)
    class_lesson_fee = db.Column(db.Integer, nullable=True)
    materials = db.Column(db.String(200), nullable=True)
    class_number_of_students = db.Column(JSON, nullable=True)
	
    teacher_username = db.Column(db.String(100),
	                             db.ForeignKey("teachers.username"),
	                             nullable=True)
    students = db.relationship("Students", backref="class_", lazy="dynamic")
    result = db.relationship("Results", backref='class_', lazy='dynamic')
    fee = db.relationship("Student_fee", backref='class_', lazy='dynamic')
    student_historys = db.relationship("Student_history",
	                                   backref='class_',
	                                   lazy='dynamic')
    students_attendance = db.relationship("Student_attendance",
	                                      backref='class_',
	                                      lazy='dynamic')



