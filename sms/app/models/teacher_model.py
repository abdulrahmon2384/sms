from sqlalchemy import JSON
from datetime import datetime
from flask_login import UserMixin
from .. import db
from .base_model import BaseModel, EncryptedMixin


class Teachers(BaseModel, UserMixin, EncryptedMixin):
    id = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    subject_specialization = db.Column(db.String(100), nullable=True)
    employment_date = db.Column(db.String(50), nullable=True)
    employee_id = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.Float, nullable=True)
    image_link = db.Column(db.String(100), default='default.png')
    role = db.Column(db.String(50), default="Teacher")
    key = db.Column(db.String(200), nullable=True)
    others = db.Column(JSON, default={})
    virtual_account_number = db.Column(db.String(10), nullable=True)
    payment_history = db.Column(JSON, default=[])
    
    # Define fields to encrypt
    _encrypted_fields = ['email', 'phonenumber', 'address', 'salary', 'key', 'virtual_account_number']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['others', 'payment_history']

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.id


# Register encryption listeners
Teachers.register_encrypted_listeners()


class TeacherAttendance(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    term = db.Column(db.String(50), nullable=True)
    session = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f"TeacherAttendance(teacher_id='{self.teacher_id}', date='{self.date}', status='{self.status}')"


class TeacherPerformance(BaseModel, EncryptedMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    evaluation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    evaluator = db.Column(db.String(100), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    term = db.Column(db.String(50), nullable=True)
    session = db.Column(db.String(50), nullable=True)
    detailed_evaluation = db.Column(JSON, default={})
    
    # Define fields to encrypt
    _encrypted_fields = ['rating']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['detailed_evaluation']
    
    def __repr__(self):
        return f"TeacherPerformance(teacher_id='{self.teacher_id}', rating='{self.rating}')"

# Register encryption listeners
TeacherPerformance.register_encrypted_listeners()


class TeacherSalary(BaseModel, EncryptedMixin):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    payment_method = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(20), nullable=False)  # paid, pending
    month = db.Column(db.String(20), nullable=True)
    year = db.Column(db.String(10), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    transaction_reference = db.Column(db.String(100), nullable=True)
    payment_details = db.Column(JSON, default={})
    
    # Define fields to encrypt
    _encrypted_fields = ['amount', 'transaction_reference']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['payment_details']
    
    def __repr__(self):
        return f"TeacherSalary(teacher_id='{self.teacher_id}', amount='{self.amount}', status='{self.payment_status}')"


# Register encryption listeners
TeacherSalary.register_encrypted_listeners()
