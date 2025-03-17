"""
Data generator module for Intelleva School Management System.
Creates encrypted fake dataset for development and testing.
"""
from faker import Faker
import random
import uuid
import json
from datetime import datetime, timedelta
from sqlalchemy import text
from .db_config import get_db_engine, create_schema_if_not_exists, set_schema
from .models.admin_model import Admin, Events, Announcements, School_information
from .models.student_model import Students, Attendance, Fees, Results, Classes, Subjects
from .models.teacher_model import Teachers, TeacherAttendance, TeacherPerformance, TeacherSalary
from . import db

# Initialize Faker
fake = Faker()

# Configuration
NUM_SCHOOLS = 3
NUM_ADMINS_PER_SCHOOL = 2
NUM_TEACHERS_PER_SCHOOL = 10
NUM_STUDENTS_PER_CLASS = 20
NUM_CLASSES_PER_SCHOOL = 6
SUBJECTS_LIST = [
    "Mathematics", "English Language", "Physics", "Chemistry", "Biology",
    "Geography", "History", "Computer Science", "Economics", "Business Studies",
    "French", "Physical Education", "Art", "Music", "Religious Studies"
]
TERMS = ["First Term", "Second Term", "Third Term"]
CURRENT_SESSION = "2024/2025"
PAYMENT_METHODS = ["Cash", "Bank Transfer", "Credit Card", "Paystack"]
PAYMENT_STATUSES = ["paid", "pending", "overdue"]
ATTENDANCE_STATUSES = ["present", "absent", "late"]
PERFORMANCE_RATINGS = [3.0, 3.5, 4.0, 4.5, 5.0]

def generate_virtual_account_number():
    """Generate a unique 10-digit virtual account number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

def generate_transaction_reference():
    """Generate a unique transaction reference for payments."""
    return f"TRX-{uuid.uuid4().hex[:12].upper()}"

def generate_school_id(school_name):
    """Generate a unique school ID based on school name."""
    # Create a deterministic but unique ID based on school name
    school_id = school_name.lower().replace(' ', '_')
    # Add a random suffix to ensure uniqueness
    random_suffix = str(uuid.uuid4())[:8]
    return f"{school_id}_{random_suffix}"

def generate_fake_data():
    """Generate complete fake dataset for Intelleva School Management System."""
    print("Starting fake data generation...")
    
    # Get database engine
    engine, is_postgres = get_db_engine()
    
    # Create schools and their data
    schools = []
    for i in range(NUM_SCHOOLS):
        school_name = f"{fake.company()} Academy"
        school_id = generate_school_id(school_name)
        schools.append({
            "name": school_name,
            "id": school_id
        })
        
        # Create schema for this school if using PostgreSQL
        if is_postgres:
            create_schema_if_not_exists(engine, school_id)
        
        # Set schema for this school
        with engine.connect() as conn:
            if is_postgres:
                set_schema(conn, school_id)
            
            # Create tables for this school
            db.metadata.create_all(conn)
            
            # Generate school data
            generate_school_data(conn, school_id, school_name)
    
    print(f"Generated data for {len(schools)} schools")
    return schools

def generate_school_data(conn, school_id, school_name):
    """Generate all data for a single school."""
    print(f"Generating data for school: {school_name} (ID: {school_id})")
    
    # Create school information
    school_info = School_information(
        school_name=school_name,
        school_address=fake.address(),
        school_phone=fake.phone_number(),
        school_email=fake.email(),
        school_other_website=fake.domain_name(),
        school_founded_year=str(random.randint(1950, 2010)),
        school_location=fake.city(),
        nationality=fake.country(),
        zipcode=fake.zipcode(),
        school_classes={},
        school_teachers={},
        school_terms=TERMS,
        school_result_type=["Midterm", "Final"],
        school_grades={
            "A": {"min": 70, "max": 100},
            "B": {"min": 60, "max": 69},
            "C": {"min": 50, "max": 59},
            "D": {"min": 45, "max": 49},
            "E": {"min": 40, "max": 44},
            "F": {"min": 0, "max": 39}
        },
        school_total_revenues={
            "2023": random.uniform(5000000, 10000000),
            "2024": random.uniform(5500000, 12000000)
        },
        school_total_expenses={
            "2023": random.uniform(4000000, 8000000),
            "2024": random.uniform(4500000, 9000000)
        },
        school_total_budget={
            "2023": random.uniform(6000000, 12000000),
            "2024": random.uniform(7000000, 14000000)
        }
    )
    db.session.add(school_info)
    
    # Create admin accounts
    admins = []
    for i in range(NUM_ADMINS_PER_SCHOOL):
        admin = Admin(
            username=f"admin{i+1}_{school_id}",
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            email=fake.email(),
            phonenumber=fake.phone_number(),
            access=True,
            key=fake.password(length=12),
            others={
                "permissions": ["full_access", "manage_users", "manage_finances"],
                "last_login": fake.date_time_this_month().isoformat(),
                "login_history": [fake.date_time_this_year().isoformat() for _ in range(5)],
                "preferences": {
                    "theme": random.choice(["light", "dark"]),
                    "notifications": random.choice([True, False]),
                    "language": random.choice(["en", "fr", "es"])
                }
            }
        )
        admins.append(admin)
        db.session.add(admin)
    
    # Create classes
    classes = []
    for i in range(NUM_CLASSES_PER_SCHOOL):
        class_name = f"Grade {i+1}"
        class_id = f"class_{i+1}_{school_id}"
        class_subjects = random.sample(SUBJECTS_LIST, k=min(10, len(SUBJECTS_LIST)))
        
        class_schedule = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        periods = ["8:00-9:00", "9:00-10:00", "10:00-11:00", "11:30-12:30", "12:30-1:30", "2:00-3:00"]
        
        for day in days:
            class_schedule[day] = {}
            for period in periods:
                if random.random() > 0.2:  # 80% chance of having a class in this period
                    class_schedule[day][period] = random.choice(class_subjects)
        
        class_obj = Classes(
            id=class_id,
            name=class_name,
            capacity=30,
            current_students=0,
            fee_amount=random.uniform(500, 2000),
            subjects=class_subjects,
            class_schedule=class_schedule
        )
        classes.append(class_obj)
        db.session.add(class_obj)
    
    # Create teachers
    teachers = []
    for i in range(NUM_TEACHERS_PER_SCHOOL):
        teacher_id = str(uuid.uuid4())
        virtual_account = generate_virtual_account_number()
        
        # Generate payment history
        payment_history = []
        for month in range(1, 13):
            if random.random() > 0.2:  # 80% chance of having a payment record
                salary_amount = random.uniform(30000, 100000)
                payment_date = fake.date_between(
                    start_date=datetime(2024, month, 1),
                    end_date=datetime(2024, month, 28)
                )
                
                payment_history.append({
                    "date": payment_date.isoformat(),
                    "amount": salary_amount,
                    "type": "salary",
                    "status": random.choice(["successful", "pending"]),
                    "reference": generate_transaction_reference(),
                    "method": random.choice(PAYMENT_METHODS),
                    "details": {
                        "month": datetime(2024, month, 1).strftime("%B"),
                        "year": "2024",
                        "processor": "Paystack",
                        "processor_fee": round(salary_amount * 0.015, 2)
                    }
                })
        
        teacher = Teachers(
            id=teacher_id,
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            middlename=fake.first_name() if random.random() > 0.5 else None,
            gender=random.choice(["Male", "Female"]),
            dob=fake.date_of_birth(minimum_age=25, maximum_age=65).strftime("%Y-%m-%d"),
            address=fake.address(),
            phonenumber=fake.phone_number(),
            email=fake.email(),
            qualification=random.choice(["B.Sc", "M.Sc", "Ph.D", "B.Ed", "M.Ed"]),
            subject_specialization=random.choice(SUBJECTS_LIST),
            employment_date=fake.date_this_decade().strftime("%Y-%m-%d"),
            employee_id=f"TCH{i+1:03d}",
            salary=random.uniform(30000, 100000),
            key=fake.password(length=12),
            virtual_account_number=virtual_account,
            payment_history=payment_history,
            others={
                "emergency_contact": {
                    "name": fake.name(),
                    "relationship": random.choice(["Spouse", "Parent", "Sibling", "Friend"]),
                    "phone": fake.phone_number()
                },
                "qualifications": [
                    {
                        "degree": random.choice(["Bachelor's", "Master's", "PhD"]),
                        "field": random.choice(["Education", "Mathematics", "Science", "Arts", "Languages"]),
                        "institution": fake.company(),
                        "year": random.randint(1990, 2020)
                    }
                ],
                "certifications": [
                    {
                        "name": random.choice(["Teaching Certificate", "Special Education", "Advanced Pedagogy"]),
                        "issuer": fake.company(),
                        "year": random.randint(2010, 2023)
                    }
                ]
            }
        )
        teachers.append(teacher)
        db.session.add(teacher)
        
        # Assign teacher to class if available
        if i < len(classes):
            classes[i].teacher_id = teacher_id
    
    # Create subjects
    subjects = []
    for class_obj in classes:
        for subject_name in class_obj.subjects:
            # Find a teacher with matching specialization if possible
            matching_teachers = [t for t in teachers if t.subject_specialization == subject_name]
            teacher_id = random.choice(matching_teachers).id if matching_teachers else random.choice(teachers).id
            
            subject = Subjects(
                name=subject_name,
                teacher_id=teacher_id,
                class_id=class_obj.id
            )
            subjects.append(subject)
            db.session.add(subject)
    
    # Create students
    students = []
    for class_obj in classes:
        for i in range(NUM_STUDENTS_PER_CLASS):
            student_id = str(uuid.uuid4())
            virtual_account = generate_virtual_account_number()
            
            # Generate payment history
            payment_history = []
            for term in TERMS:
                if random.random() > 0.2:  # 80% chance of having a payment record
                    fee_amount = class_obj.fee_amount
                    payment_date = fake.date_this_year()
                    
                    payment_history.append({
                        "date": payment_date.isoformat(),
                        "amount": fee_amount,
                        "type": "tuition",
                        "status": random.choice(["successful", "pending", "failed"]),
                        "reference": generate_transaction_reference(),
                        "method": random.choice(PAYMENT_METHODS),
                        "details": {
                            "term": term,
                            "session": CURRENT_SESSION,
                            "processor": "Paystack",
                            "processor_fee": round(fee_amount * 0.015, 2)
                        }
                    })
            
            student = Students(
                id=student_id,
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                middlename=fake.first_name() if random.random() > 0.5 else None,
                gender=random.choice(["Male", "Female"]),
                dob=fake.date_of_birth(minimum_age=5, maximum_age=18).strftime("%Y-%m-%d"),
                address=fake.address(),
                phonenumber=fake.phone_number(),
                email=fake.email(),
                parent_name=f"{fake.first_name()} {fake.last_name()}",
                parent_phonenumber=fake.phone_number(),
                parent_email=fake.email(),
                parent_address=fake.address(),
                parent_occupation=fake.job(),
                class_id=class_obj.id,
                admission_date=fake.date_this_decade().strftime("%Y-%m-%d"),
                admission_number=f"STD{i+1:03d}",
                key=fake.password(length=12),
                virtual_account_number=virtual_account,
                payment_history=payment_history,
                others={
                    "medical_info": {
                        "blood_type": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                        "allergies": random.choice([[], ["Peanuts"], ["Dust"], ["Pollen"], ["Seafood"]]),
                        "conditions": random.choice([[], ["Asthma"], ["Diabetes"], ["None"]])
                    },
                    "emergency_contact": {
                        "name": fake.name(),
                        "relationship": random.choice(["Parent", "Guardian", "Relative"]),
                        "phone": fake.phone_number()
                    },
                    "extracurricular": random.sample(
                        ["Sports", "Music", "Drama", "Debate", "Art", "Science Club", "Chess"], 
                        k=random.randint(0, 3)
                    )
                }
            )
            students.append(student)
            db.session.add(student)
            
            # Increment class student count
            class_obj.current_students += 1
            
            # Create attendance records
            for _ in range(random.randint(10, 30)):
                attendance_date = fake.date_this_year()
                attendance = Attendance(
                    student_id=student_id,
                    date=attendance_date,
                    status=random.choice(ATTENDANCE_STATUSES),
                    class_id=class_obj.id,
                    term=random.choice(TERMS),
                    session=CURRENT_SESSION
                )
                db.session.add(attendance)
            
            # Create fee records
            for term in TERMS:
                transaction_ref = generate_transaction_reference()
                payment_details = {
                    "processor": "Paystack",
                    "processor_fee": round(class_obj.fee_amount * 0.015, 2),
                    "payment_date": fake.date_this_year().isoformat(),
                    "payment_time": fake.time().isoformat(),
                    "payer_name": f"{fake.first_name()} {fake.last_name()}",
                    "payer_email": fake.email(),
                    "receipt_number": f"RCP-{uuid.uuid4().hex[:8].upper()}",
                    "notes": random.choice(["", "Paid in full", "Partial payment", "Scholarship applied"])
                }
                
                fee = Fees(
                    student_id=student_id,
                    amount=class_obj.fee_amount,
                    payment_date=fake.date_this_year(),
                    payment_method=random.choice(PAYMENT_METHODS),
                    payment_status=random.choice(PAYMENT_STATUSES),
                    term=term,
                    session=CURRENT_SESSION,
                    class_id=class_obj.id,
                    description=f"Tuition fee for {term}, {CURRENT_SESSION}",
                    transaction_reference=transaction_ref,
                    payment_details=payment_details
                )
                db.session.add(fee)
            
            # Create result records
            for subject in [s for s in subjects if s.class_id == class_obj.id]:
                for term in TERMS:
                    score = random.uniform(0, 100)
                    # Determine grade based on score
                    grade = None
                    for g, range_val in school_info.school_grades.items():
                        if range_val["min"] <= score <= range_val["max"]:
                            grade = g
                            break
                    
                    # Create detailed scores
                    detailed_scores = {
                        "assignments": [
                            {"name": "Assignment 1", "score": random.uniform(0, 100), "weight": 0.1},
                            {"name": "Assignment 2", "score": random.uniform(0, 100), "weight": 0.1}
                        ],
                        "tests": [
                            {"name": "Quiz 1", "score": random.uniform(0, 100), "weight": 0.15},
                            {"name": "Test 1", "score": random.uniform(0, 100), "weight": 0.25}
                        ],
                        "exam": {"score": random.uniform(0, 100), "weight": 0.4},
                        "participation": {"score": random.uniform(0, 100), "weight": 0.1}
                    }
                    
                    result = Results(
                        student_id=student_id,
                        subject=subject.name,
                        score=score,
                        grade=grade,
                        term=term,
                        session=CURRENT_SESSION,
                        class_id=class_obj.id,
                        exam_type=random.choice(["Midterm", "Final"]),
                        comment=random.choice([
                            "Excellent performance", 
                            "Good effort", 
                            "Satisfactory", 
                            "Needs improvement", 
                            "Poor performance"
                        ]),
                        detailed_scores=detailed_scores
                    )
                    db.session.add(result)
    
    # Create teacher attendance records
    for teacher in teachers:
        for _ in range(random.randint(10, 30)):
            attendance_date = fake.date_this_year()
            attendance = TeacherAttendance(
                teacher_id=teacher.id,
                date=attendance_date,
                status=random.choice(ATTENDANCE_STATUSES),
                term=random.choice(TERMS),
                session=CURRENT_SESSION
            )
            db.session.add(attendance)
        
        # Create teacher performance records
        for term in TERMS:
            detailed_evaluation = {
                "categories": {
                    "teaching_methodology": random.uniform(3.0, 5.0),
                    "classroom_management": random.uniform(3.0, 5.0),
                    "student_engagement": random.uniform(3.0, 5.0),
                    "curriculum_knowledge": random.uniform(3.0, 5.0),
                    "professional_conduct": random.uniform(3.0, 5.0)
                },
                "strengths": random.sample([
                    "Excellent communication skills",
                    "Strong subject knowledge",
                    "Effective classroom management",
                    "Creative teaching methods",
                    "Good rapport with students",
                    "Consistent assessment practices"
                ], k=random.randint(1, 3)),
                "areas_for_improvement": random.sample([
                    "Time management",
                    "Technology integration",
                    "Differentiated instruction",
                    "Student feedback",
                    "Parent communication",
                    "Documentation"
                ], k=random.randint(0, 2)),
                "goals": random.sample([
                    "Implement more project-based learning",
                    "Improve assessment techniques",
                    "Enhance digital teaching skills",
                    "Develop better classroom resources",
                    "Increase student participation"
                ], k=random.randint(1, 2))
            }
            
            performance = TeacherPerformance(
                teacher_id=teacher.id,
                rating=random.choice(PERFORMANCE_RATINGS),
                evaluation_date=fake.date_this_year(),
                evaluator=random.choice(admins).username,
                comments=fake.paragraph(),
                term=term,
                session=CURRENT_SESSION,
                detailed_evaluation=detailed_evaluation
            )
            db.session.add(performance)
        
        # Create teacher salary records
        for month in range(1, 13):
            transaction_ref = generate_transaction_reference()
            payment_details = {
                "processor": "Paystack",
                "processor_fee": round(teacher.salary * 0.015, 2),
                "payment_date": fake.date_between(
                    start_date=datetime(2024, month, 1),
                    end_date=datetime(2024, month, 28)
                ).isoformat(),
                "payment_time": fake.time().isoformat(),
                "approver": random.choice(admins).username,
                "bank_name": random.choice(["First Bank", "GTBank", "Zenith Bank", "UBA", "Access Bank"]),
                "account_type": random.choice(["Savings", "Current"]),
                "tax_deductions": round(teacher.salary * 0.1, 2),
                "benefits": round(teacher.salary * 0.05, 2),
                "net_amount": round(teacher.salary * 0.95, 2)
            }
            
            salary = TeacherSalary(
                teacher_id=teacher.id,
                amount=teacher.salary,
                payment_date=fake.date_between(
                    start_date=datetime(2024, month, 1),
                    end_date=datetime(2024, month, 28)
                ),
                payment_method=random.choice(PAYMENT_METHODS),
                payment_status=random.choice(["paid", "pending"]),
                month=datetime(2024, month, 1).strftime("%B"),
                year="2024",
                description=f"Salary for {datetime(2024, month, 1).strftime('%B')} 2024",
                transaction_reference=transaction_ref,
                payment_details=payment_details
            )
            db.session.add(salary)
    
    # Create events
    for _ in range(random.randint(5, 10)):
        event = Events(
            name=random.choice([
                "Parent-Teacher Meeting", 
                "Sports Day", 
                "Annual Day", 
                "Science Exhibition", 
                "Cultural Fest",
                "Graduation Ceremony",
                "Inter-School Competition"
            ]),
            description=fake.paragraph(),
            date=fake.date_this_year()
        )
        db.session.add(event)
    
    # Create announcements
    for _ in range(random.randint(5, 10)):
        announcement = Announcements(
            title=random.choice([
                "Important Notice", 
                "Upcoming Event", 
                "Holiday Announcement", 
                "Exam Schedule", 
                "Fee Payment Reminder",
                "New Policy Implementation",
                "Staff Meeting"
            ]),
            content=fake.paragraph(),
            created_at=fake.date_time_this_year()
        )
        db.session.add(announcement)
    
    # Update school information with counts
    school_info.school_total_students = len(students)
    school_info.school_total_teachers = len(teachers)
    school_info.school_total_admin = len(admins)
    
    # Commit all changes
    db.session.commit()
    print(f"Data generation complete for school: {school_name}")

def clear_all_data():
    """Delete all existing data from the database."""
    print("Clearing all existing data...")
    
    # Get database engine
    engine, is_postgres = get_db_engine()
    
    with engine.connect() as conn:
        # Drop all tables
        db.metadata.drop_all(conn)
        
        # If PostgreSQL, also drop all schemas
        if is_postgres:
            try:
                # Get list of schemas
                result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('public', 'information_schema', 'pg_catalog', 'pg_toast')"))
                schemas = [row[0] for row in result]
                
                # Drop each schema
                for schema in schemas:
                    conn.execute(text(f"DROP SCHEMA IF EXISTS {schema} CASCADE"))
                
                print(f"Dropped {len(schemas)} schemas")
            except Exception as e:
                print(f"Error dropping schemas: {e}")
    
    print("All data cleared successfully")

def initialize_database():
    """Initialize database with fake data."""
    try:
        # Clear existing data
        clear_all_data()
        
        # Generate new fake data
        schools = generate_fake_data()
        
        return {
            "success": True,
            "message": f"Successfully initialized database with {len(schools)} schools",
            "schools": schools
        }
    except Exception as e:
        print(f"Error initializing database: {e}")
        return {
            "success": False,
            "message": f"Error initializing database: {e}"
        }

if __name__ == "__main__":
    initialize_database()
