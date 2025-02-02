from sqlalchemy import JSON
from datetime import datetime
from flask_login import UserMixin
from .. import db


class Admin(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(50), nullable=True)
    access = db.Column(db.Boolean, nullable=True)
    key = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(50), default="Admin")
    others = db.Column(JSON, default={})
    image_link = db.Column(db.String(100),
                           default='default.png')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username



class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}')"



class Announcements(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f"Announcement(title='{self.title}', content='{self.content}', created_at='{self.created_at}')"



class School_information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_name = db.Column(db.String(100), nullable=False)
    school_address = db.Column(db.String(100), nullable=True)
    school_phone = db.Column(db.String(100), nullable=True)
    school_email = db.Column(db.String(100), nullable=True)
    school_logo_link = db.Column(db.String(500), nullable=True, default="https://f005.backblazeb2.com/file/School-management-system/images-1.jpeg")
    school_other_website = db.Column(db.String(100), nullable=True)
	
    school_total_students = db.Column(db.Integer, default=0)
    school_total_teachers = db.Column(db.Integer, default=0)
    school_total_admin = db.Column(db.Integer, default=0)
	
    school_classes = db.Column(JSON, nullable=True)
    school_teachers = db.Column(JSON, nullable=True)
	
    school_terms = db.Column(JSON, nullable=True)
    school_result_type = db.Column(JSON, nullable=True)
    school_founded_year = db.Column(db.String(50), nullable=False)
    
    school_total_revenues = db.Column(JSON, nullable=True)
    school_total_expenses = db.Column(JSON, nullable=True)
    school_total_budget = db.Column(JSON, nullable=True)
    school_grades = db.Column(JSON, default={})

    school_location =  db.Column(db.String(300), nullable=True)
    nationality = db.Column(db.String(200), nullable=True)
    zipcode = db.Column(db.String(50), nullable=True)







