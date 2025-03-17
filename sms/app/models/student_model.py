from sqlalchemy import JSON
from datetime import datetime
from flask_login import UserMixin
from .. import db
from .base_model import BaseModel, EncryptedMixin


class Students(BaseModel, UserMixin, EncryptedMixin):
    id = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    parent_name = db.Column(db.String(100), nullable=True)
    parent_phonenumber = db.Column(db.String(50), nullable=True)
    parent_email = db.Column(db.String(100), nullable=True)
    parent_address = db.Column(db.String(100), nullable=True)
    parent_occupation = db.Column(db.String(100), nullable=True)
    class_id = db.Column(db.String(50), nullable=True)
    admission_date = db.Column(db.String(50), nullable=True)
    admission_number = db.Column(db.String(50), nullable=True)
    image_link = db.Column(db.String(100), default='default.png')
    role = db.Column(db.String(50), default="Student")
    key = db.Column(db.String(200), nullable=True)
    others = db.Column(JSON, default={})
    virtual_account_number = db.Column(db.String(10), nullable=True)
    payment_history = db.Column(JSON, default=[])
    
    # Define fields to encrypt
    _encrypted_fields = ['email', 'phonenumber', 'address', 'parent_phonenumber', 
                         'parent_email', 'parent_address', 'key', 'virtual_account_number']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['others', 'payment_history']

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.id


# Register encryption listeners
Students.register_encrypted_listeners()


class Attendance(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    class_id = db.Column(db.String(50), nullable=False)
    term = db.Column(db.String(50), nullable=True)
    session = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f"Attendance(student_id='{self.student_id}', date='{self.date}', status='{self.status}')"


class Fees(BaseModel, EncryptedMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    payment_method = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(20), nullable=False)  # paid, pending, overdue
    term = db.Column(db.String(50), nullable=True)
    session = db.Column(db.String(50), nullable=True)
    class_id = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    transaction_reference = db.Column(db.String(100), nullable=True)
    payment_details = db.Column(JSON, default={})
    
    # Define fields to encrypt
    _encrypted_fields = ['amount', 'transaction_reference']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['payment_details']
    
    def __repr__(self):
        return f"Fees(student_id='{self.student_id}', amount='{self.amount}', status='{self.payment_status}')"

# Register encryption listeners
Fees.register_encrypted_listeners()


class Results(BaseModel, EncryptedMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(5), nullable=True)
    term = db.Column(db.String(50), nullable=True)
    session = db.Column(db.String(50), nullable=True)
    class_id = db.Column(db.String(50), nullable=True)
    exam_type = db.Column(db.String(50), nullable=True)  # midterm, final
    comment = db.Column(db.String(200), nullable=True)
    detailed_scores = db.Column(JSON, default={})
    
    # Define fields to encrypt
    _encrypted_fields = ['score']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['detailed_scores']
    
    def __repr__(self):
        return f"Results(student_id='{self.student_id}', subject='{self.subject}', score='{self.score}')"

# Register encryption listeners
Results.register_encrypted_listeners()


class Classes(BaseModel, EncryptedMixin):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.String(100), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    current_students = db.Column(db.Integer, default=0)
    subjects = db.Column(JSON, nullable=True)
    fee_amount = db.Column(db.Float, nullable=True)
    class_schedule = db.Column(JSON, default={})
    
    # Define fields to encrypt
    _encrypted_fields = ['fee_amount']
    
    # Define JSON fields to encrypt
    _encrypted_json_fields = ['subjects', 'class_schedule']
    
    def __repr__(self):
        return f"Class(name='{self.name}', teacher='{self.teacher_id}')"

# Register encryption listeners
Classes.register_encrypted_listeners()


class Subjects(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.String(100), nullable=True)
    class_id = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return f"Subject(name='{self.name}', teacher='{self.teacher_id}')"
