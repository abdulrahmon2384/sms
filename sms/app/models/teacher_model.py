from sqlalchemy import JSON
from . import db
from flask_login import UserMixin



class Teachers(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=True)

    address = db.Column(db.String(300), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    qualification = db.Column(db.String(50), nullable=True)
    years_of_experience = db.Column(db.Integer, nullable=True)
    certifications = db.Column(db.String(200), nullable=True)
    teaching_specializations = db.Column(db.String(100), nullable=True)
    
    languages_spoken = db.Column(db.String(100), nullable=True)
    emergency_contact = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    left_date = db.Column(db.Date, nullable=True)
    current_salary = db.Column(db.Integer, nullable=True)
    salarys = db.Column(db.JSON, nullable=True)
    subject_taught = db.Column(db.JSON, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    marital_status = db.Column(db.String(50), nullable=True)
    attendance_count = db.Column(JSON, default={})

    role = db.Column(db.String(50), default='Teacher')
    key = db.Column(db.String(200), nullable=True)
    access = db.Column(db.Boolean, default=False)
    others = db.Column(JSON, default={})
    image_link = db.Column(db.String(200), default='default.png')

    class_teacher = db.relationship("Classes", backref="teacher", lazy="dynamic")
    attendance = db.relationship("Teacher_attendance",
                                 backref='teacher',
                                 lazy='dynamic')
    historys = db.relationship("Teacher_history",
                               backref='teacher',
                               lazy='dynamic')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username

    def marital_status_options(self):
        title_map = {
            ('Single', 'Male'): 'Mr',
            ('Single', 'Female'): 'Miss',
            ('Married', 'Male'): 'Mr',
            ('Married', 'Female'): 'Mrs',
            ('Divorced', 'Male'): 'Mr',
            ('Divorced', 'Female'): 'Mrs',
            ('Widowed', 'Male'): 'Mr',
            ('Widowed', 'Female'): 'Mrs',
        }
        title = title_map.get((self.marital_status, self.gender), 'Unknown')
        return title

    def about(self):
        return {
            "name": f"{self.lastname} {self.firstname}",
            "subject_taught": self.subject_taught,
            "contact": {
                'email': self.phonenumber,
                'phonenumber': self.email
            },
            "bio": self.bio,
            "age": 50,
            "image": self.image_link,
            "marital_status": self.marital_status_options()
        }


class Teacher_attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String(100), nullable=False)
    morning_attendance = db.Column(db.DateTime, nullable=False)
    evening_attendance = db.Column(db.DateTime, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    late_arrival = db.Column(db.Boolean, nullable=True)

    teacher_username = db.Column(db.String(200),
                                 db.ForeignKey('teachers.username'),
                                 nullable=False)


class Teacher_history(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    salarys = db.Column(JSON, nullable=True)
    attendance = db.Column(JSON, nullable=True)
    termclass = db.Column(JSON, nullable=True)
    role = db.Column(db.String(50), nullable=True)

    teacher_username = db.Column(db.String(200),
                                 db.ForeignKey('teachers.username'),
                                 nullable=False)
