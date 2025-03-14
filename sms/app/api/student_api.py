from flask import Blueprint, jsonify, request, session, abort
from flask_login import current_user, login_required
from ..models.student_model import Student
from ..models.attendance_model import Attendance
from ..models.performance_model import Performance
from ..models.fee_model import Fee, Payment
from .. import db
import json
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd
import numpy as np

# Create a Blueprint with the proper URL prefix
student_api_bp = Blueprint("student_api", __name__, url_prefix="/api/student")

# Dashboard statistics
@student_api_bp.route("/dashboard/stats", methods=["GET"])
@login_required
def dashboard_stats():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get student ID
        student_id = current_user.id
        
        # In a real implementation, you would fetch actual data
        # For now, we'll generate some sample data
        
        # Get attendance rate
        attendance_rate = 91.9  # Example rate
        
        # Get performance summary
        performance_summary = {
            "gpa": 3.75,
            "class_rank": 5,
            "total_students": 30,
            "subjects": [
                {"name": "Mathematics", "grade": "A", "score": 92},
                {"name": "English", "grade": "A-", "score": 88},
                {"name": "Physics", "grade": "B+", "score": 85},
                {"name": "Chemistry", "grade": "A", "score": 90},
                {"name": "Biology", "grade": "B", "score": 82}
            ]
        }
        
        # Get upcoming assignments
        upcoming_assignments = [
            {"subject": "Mathematics", "title": "Calculus Problem Set", "due_date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')},
            {"subject": "Physics", "title": "Lab Report", "due_date": (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')},
            {"subject": "English", "title": "Essay Submission", "due_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
        ]
        
        # Get recent activities
        recent_activities = [
            {"type": "grade", "description": "New grade posted for Physics", "timestamp": datetime.now().isoformat()},
            {"type": "attendance", "description": "Marked present for all classes", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()},
            {"type": "assignment", "description": "Submitted Chemistry lab report", "timestamp": (datetime.now() - timedelta(days=2)).isoformat()},
            {"type": "payment", "description": "Fee payment received", "timestamp": (datetime.now() - timedelta(days=5)).isoformat()}
        ]
        
        # Get fee summary
        fee_summary = {
            "total_fees": 2500,
            "paid_amount": 1750,
            "outstanding": 750,
            "next_due_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        }
        
        return jsonify({
            "success": True,
            "stats": {
                "attendance_rate": attendance_rate,
                "performance_summary": performance_summary,
                "upcoming_assignments": upcoming_assignments,
                "recent_activities": recent_activities,
                "fee_summary": fee_summary
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch dashboard statistics: {str(e)}"}), 500

# Attendance endpoints
@student_api_bp.route("/attendance", methods=["GET"])
@login_required
def get_attendance():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get query parameters
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        # In a real implementation, you would fetch attendance data from the database
        # For now, we'll generate sample data
        
        # Generate dates between start_date and end_date
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        dates = [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end - start).days + 1)]
        
        # Generate attendance records for each date
        attendance_records = []
        for date in dates:
            # Skip weekends
            day_of_week = datetime.strptime(date, '%Y-%m-%d').weekday()
            if day_of_week >= 5:  # 5 = Saturday, 6 = Sunday
                continue
                
            # Generate random status with higher probability of present
            rand = np.random.random()
            if rand < 0.92:  # 92% chance of present
                status = "present"
            elif rand < 0.97:  # 5% chance of late
                status = "late"
            else:  # 3% chance of absent
                status = "absent"
                
            attendance_records.append({
                "date": date,
                "day": datetime.strptime(date, '%Y-%m-%d').strftime('%A'),
                "status": status,
                "marked_by": "Mr. Robert Johnson",
                "marked_at": f"{date}T08:15:00"
            })
        
        # Calculate attendance summary
        total_days = len(attendance_records)
        present_days = sum(1 for record in attendance_records if record["status"] == "present")
        late_days = sum(1 for record in attendance_records if record["status"] == "late")
        absent_days = sum(1 for record in attendance_records if record["status"] == "absent")
        
        attendance_summary = {
            "total_days": total_days,
            "present_days": present_days,
            "late_days": late_days,
            "absent_days": absent_days,
            "attendance_rate": round((present_days / total_days) * 100, 1) if total_days > 0 else 0
        }
        
        # Generate monthly attendance trend
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        current_month = datetime.now().month - 1  # 0-indexed
        trend_months = months[current_month-5:current_month+1] if current_month >= 5 else months[7+current_month-5:] + months[:current_month+1]
        trend_rates = [round(np.random.uniform(85, 98), 1) for _ in range(6)]
        
        attendance_trend = {
            "months": trend_months,
            "rates": trend_rates
        }
        
        return jsonify({
            "success": True,
            "attendance": {
                "records": attendance_records,
                "summary": attendance_summary,
                "trend": attendance_trend
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch attendance data: {str(e)}"}), 500

# Performance endpoints
@student_api_bp.route("/performance", methods=["GET"])
@login_required
def get_performance():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get query parameters
        term = request.args.get('term', 'current')
        
        # In a real implementation, you would fetch performance data from the database
        # For now, we'll generate sample data
        
        # Generate subjects with performance data
        subjects = [
            {
                "name": "Mathematics",
                "teacher": "Mr. Robert Johnson",
                "assessments": [
                    {"type": "Assignment", "name": "Problem Set 1", "score": 90, "max_score": 100, "date": (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d')},
                    {"type": "Quiz", "name": "Quiz 1", "score": 85, "max_score": 100, "date": (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')},
                    {"type": "Test", "name": "Midterm Exam", "score": 92, "max_score": 100, "date": (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')},
                    {"type": "Assignment", "name": "Problem Set 2", "score": 95, "max_score": 100, "date": (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')}
                ],
                "average": 92,
                "grade": "A",
                "comments": "Excellent work in problem-solving and mathematical concepts."
            },
            {
                "name": "English",
                "teacher": "Ms. Sarah Williams",
                "assessments": [
                    {"type": "Assignment", "name": "Essay 1", "score": 88, "max_score": 100, "date": (datetime.now() - timedelta(days=28)).strftime('%Y-%m-%d')},
                    {"type": "Quiz", "name": "Vocabulary Quiz", "score": 92, "max_score": 100, "date": (datetime.now() - timedelta(days=21)).strftime('%Y-%m-%d')},
                    {"type": "Test", "name": "Literature Analysis", "score": 85, "max_score": 100, "date": (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')},
                    {"type": "Assignment", "name": "Book Report", "score": 90, "max_score": 100, "date": (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}
                ],
                "average": 88,
                "grade": "A-",
                "comments": "Strong writing skills with good critical analysis."
            },
            {
                "name": "Physics",
                "teacher": "Dr. Michael Chen",
                "assessments": [
                    {"type": "Assignment", "name": "Lab Report 1", "score": 82, "max_score": 100, "date": (datetime.now() - timedelta(days=26)).strftime('%Y-%m-%d')},
                    {"type": "Quiz", "name": "Mechanics Quiz", "score": 88, "max_score": 100, "date": (datetime.now() - timedelta(days=19)).strftime('%Y-%m-%d')},
                    {"type": "Test", "name": "Forces Exam", "score": 85, "max_score": 100, "date": (datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d')},
                    {"type": "Assignment", "name": "Problem Set", "score": 87, "max_score": 100, "date": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')}
                ],
                "average": 85,
                "grade": "B+",
                "comments": "Good understanding of physical concepts. Could improve on mathematical applications."
            },
            {
                "name": "Chemistry",
                "teacher": "Dr. Emily Rodriguez",
                "assessments": [
                    {"type": "Assignment", "name": "Lab Report 1", "score": 88, "max_score": 100, "date": (datetime.now() - timedelta(days=27)).strftime('%Y-%m-%d')},
                    {"type": "Quiz", "name": "Periodic Table Quiz", "score": 95, "max_score": 100, "date": (datetime.now() - timedelta(days=18)).strftime('%Y-%m-%d')},
                    {"type": "Test", "name": "Chemical Reactions Exam", "score": 90, "max_score": 100, "date": (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d')},
                    {"type": "Assignment", "name": "Molecular Structures", "score": 92, "max_score": 100, "date": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')}
                ],
                "average": 90,
                "grade": "A",
                "comments": "Excellent lab work and theoretical understanding."
            },
            {
                "name": "Biology",
                "teacher": "Mrs. Lisa Thompson",
                "assessments": [
                    {"type": "Assignment", "name": "Ecosystem Report", "score": 85, "max_score": 100, "date": (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')},
                    {"type": "Quiz", "name": "Cell Structure Quiz", "score": 80, "max_score": 100, "date": (datetime.now() - timedelta(days=22)).strftime('%Y-%m-%d')},
                    {"type": "Test", "name": "Genetics Exam", "score": 82, "max_score": 100, "date": (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')},
                    {"type": "Assignment", "name": "Lab Report", "score": 88, "max_score": 100, "date": (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')}
                ],
                "average": 82,
                "grade": "B",
                "comments": "Good understanding of biological concepts. More attention to detail needed in lab work."
            }
        ]
        
        # Calculate overall performance
        overall_average = round(sum(subject["average"] for subject in subjects) / len(subjects), 1)
        
        # Determine GPA and class rank
        gpa = 3.75
        class_rank = 5
        total_students = 30
        
        # Generate performance trend over terms
        terms = ["Term 1 (2023-2024)", "Term 2 (2023-2024)", "Term 3 (2023-2024)", "Term 1 (2024-2025)"]
        trend_averages = [round(np.random.uniform(80, 90), 1) for _ in range(4)]
        
        performance_trend = {
            "terms": terms,
            "averages": trend_averages
        }
        
        return jsonify({
            "success": True,
            "performance": {
                "subjects": subjects,
                "overall_average": overall_average,
                "gpa": gpa,
                "class_rank": class_rank,
                "total_students": total_students,
                "trend": performance_trend
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch performance data: {str(e)}"}), 500

# Class information endpoints
@student_api_bp.route("/class", methods=["GET"])
@login_required
def get_class_info():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch class information from the database
        # For now, we'll generate sample data
        
        # Class details
        class_details = {
            "name": "Grade 10-A",
            "class_teacher": "Mr. Robert Johnson",
            "room": "Room 203",
            "students_count": 30
        }
        
        # Class schedule
        schedule = [
            {"day": "Monday", "periods": [
                {"period": 1, "time": "08:00 - 08:45", "subject": "Mathematics", "teacher": "Mr. Robert Johnson"},
                {"period": 2, "time": "08:50 - 09:35", "subject": "English", "teacher": "Ms. Sarah Williams"},
                {"period": 3, "time": "09:40 - 10:25", "subject": "Physics", "teacher": "Dr. Michael Chen"},
                {"period": 4, "time": "10:40 - 11:25", "subject": "Chemistry", "teacher": "Dr. Emily Rodriguez"},
                {"period": 5, "time": "11:30 - 12:15", "subject": "Biology", "teacher": "Mrs. Lisa Thompson"},
                {"period": 6, "time": "13:00 - 13:45", "subject": "Physical Education", "teacher": "Mr. James Wilson"},
                {"period": 7, "time": "13:50 - 14:35", "subject": "History", "teacher": "Mr. David Brown"}
            ]},
            {"day": "Tuesday", "periods": [
                {"period": 1, "time": "08:00 - 08:45", "subject": "English", "teacher": "Ms. Sarah Williams"},
                {"period": 2, "time": "08:50 - 09:35", "subject": "Mathematics", "teacher": "Mr. Robert Johnson"},
                {"period": 3, "time": "09:40 - 10:25", "subject": "Chemistry", "teacher": "Dr. Emily Rodriguez"},
                {"period": 4, "time": "10:40 - 11:25", "subject": "Physics", "teacher": "Dr. Michael Chen"},
                {"period": 5, "time": "11:30 - 12:15", "subject": "Computer Science", "teacher": "Ms. Jennifer Lee"},
                {"period": 6, "time": "13:00 - 13:45", "subject": "Art", "teacher": "Mrs. Patricia Garcia"},
                {"period": 7, "time": "13:50 - 14:35", "subject": "Geography", "teacher": "Mr. Thomas Martinez"}
            ]},
            {"day": "Wednesday", "periods": [
                {"period": 1, "time": "08:00 - 08:45", "subject": "Physics", "teacher": "Dr. Michael Chen"},
                {"period": 2, "time": "08:50 - 09:35", "subject": "Chemistry", "teacher": "Dr. Emily Rodriguez"},
                {"period": 3, "time": "09:40 - 10:25", "subject": "Mathematics", "teacher": "Mr. Robert Johnson"},
                {"period": 4, "time": "10:40 - 11:25", "subject": "English", "teacher": "Ms. Sarah Williams"},
                {"period": 5, "time": "11:30 - 12:15", "subject": "Biology", "teacher": "Mrs. Lisa Thompson"},
                {"period": 6, "time": "13:00 - 13:45", "subject": "Music", "teacher": "Mr. Richard Taylor"},
                {"period": 7, "time": "13:50 - 14:35", "subject": "Foreign Language", "teacher": "Ms. Maria Gonzalez"}
            ]},
            {"day": "Thursday", "periods": [
                {"period": 1, "time": "08:00 - 08:45", "subject": "Biology", "teacher": "Mrs. Lisa Thompson"},
                {"period": 2, "time": "08:50 - 09:35", "subject": "Physics", "teacher": "Dr. Michael Chen"},
                {"period": 3, "time": "09:40 - 10:25", "subject": "English", "teacher": "Ms. Sarah Williams"},
                {"period": 4, "time": "10:40 - 11:25", "subject": "Mathematics", "teacher": "Mr. Robert Johnson"},
                {"period": 5, "time": "11:30 - 12:15", "subject": "Chemistry", "teacher": "Dr. Emily Rodriguez"},
                {"period": 6, "time": "13:00 - 13:45", "subject": "Physical Education", "teacher": "Mr. James Wilson"},
                {"period": 7, "time": "13:50 - 14:35", "subject": "Computer Science", "teacher": "Ms. Jennifer Lee"}
            ]},
            {"day": "Friday", "periods": [
                {"period": 1, "time": "08:00 - 08:45", "subject": "Mathematics", "teacher": "Mr. Robert Johnson"},
                {"period": 2, "time": "08:50 - 09:35", "subject": "Biology", "teacher": "Mrs. Lisa Thompson"},
                {"period": 3, "time": "09:40 - 10:25", "subject": "English", "teacher": "Ms. Sarah Williams"},
                {"period": 4, "time": "10:40 - 11:25", "subject": "Physics", "teacher": "Dr. Michael Chen"},
                {"period": 5, "time": "11:30 - 12:15", "subject": "Chemistry", "teacher": "Dr. Emily Rodriguez"},
                {"period": 6, "time": "13:00 - 13:45", "subject": "History", "teacher": "Mr. David Brown"},
                {"period": 7, "time": "13:50 - 14:35", "subject": "Art", "teacher": "Mrs. Patricia Garcia"}
            ]}
        ]
        
        # Teachers
        teachers = [
            {"name": "Mr. Robert Johnson", "subject": "Mathematics", "email": "r.johnson@intelleva-academy.edu", "image_link": "https://f005.backblazeb2.com/file/School-management-system/teacher-1.jpg"},
            {"name": "Ms. Sarah Williams", "subject": "English", "email": "s.williams@intelleva-academy.edu", "image_link": "https://f005.backblazeb2.com/file/School-management-system/teacher-2.jpg"},
            {"name": "Dr. Michael Chen", "subject": "Physics", "email": "m.chen@intelleva-academy.edu", "image_link": "https://f005.backblazeb2.com/file/School-management-system/teacher-3.jpg"},
            {"name": "Dr. Emily Rodriguez", "subject": "Chemistry", "email": "e.rodriguez@intelleva-academy.edu", "image_link": "https://f005.backblazeb2.com/file/School-management-system/teacher-4.jpg"},
            {"name": "Mrs. Lisa Thompson", "subject": "Biology", "email": "l.thompson@intelleva-academy.edu", "image_link": "https://f005.backblazeb2.com/file/School-management-system/teacher-5.jpg"}
        ]
        
        # Classmates (sample data, in a real implementation you would fetch actual classmates)
        classmates = []
        for i in range(1, 31):
            if i == current_user.id:  # Skip current user
                continue
                
            classmates.append({
                "id": i,
                "name": f"Student {i}",
                "image_link": f"https://f005.backblazeb2.com/file/School-management-system/student-{i % 10}.jpg"
            })
        
        return jsonify({
            "success": True,
            "class_info": {
                "details": class_details,
                "schedule": schedule,
                "teachers": teachers,
                "classmates": classmates
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch class information: {str(e)}"}), 500

# Fees management endpoints
@student_api_bp.route("/fees", methods=["GET"])
@login_required
def get_fees():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch fee information from the database
        # For now, we'll generate sample data
        
        # Fee summary
        fee_summary = {
            "total_fees": 2500,
            "paid_amount": 1750,
            "outstanding": 750,
            "next_due_date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            "payment_progress": 70  # Percentage
        }
        
        # Fee structure
        fee_structure = [
            {"fee_type": "Tuition Fee", "description": "Regular academic instruction fees", "amount": 1800, "frequency": "Per Term", "payment_progress": 70},
            {"fee_type": "Laboratory Fee", "description": "Science and computer lab usage", "amount": 300, "frequency": "Per Term", "payment_progress": 70},
            {"fee_type": "Library Fee", "description": "Access to library resources", "amount": 150, "frequency": "Per Term", "payment_progress": 70},
            {"fee_type": "Technology Fee", "description": "IT infrastructure and services", "amount": 200, "frequency": "Per Term", "payment_progress": 70},
            {"fee_type": "Extracurricular Fee", "description": "Clubs and activities", "amount": 50, "frequency": "Per Term", "payment_progress": 70}
        ]
        
        # Payment installments
        installments = [
            {"installment_number": 1, "amount": 1000, "due_date": "2025-01-15", "paid_date": "2025-01-12", "status": "paid"},
            {"installment_number": 2, "amount": 750, "due_date": "2025-02-15", "paid_date": "2025-02-14", "status": "paid"},
            {"installment_number": 3, "amount": 750, "due_date": "2025-03-30", "paid_date": None, "status": "pending"}
        ]
        
        # Payment history
        payment_history = [
            {"receipt_number": "INV-2025-001", "date": "2025-01-12", "payment_method": "Credit Card", "description": "First Term Fees - Installment #1", "amount": 1000, "status": "completed"},
            {"receipt_number": "INV-2025-015", "date": "2025-02-14", "payment_method": "Bank Transfer", "description": "First Term Fees - Installment #2", "amount": 750, "status": "completed"}
        ]
        
        return jsonify({
            "success": True,
            "fees": {
                "summary": fee_summary,
                "structure": fee_structure,
                "installments": installments,
                "payment_history": payment_history
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch fee information: {str(e)}"}), 500

@student_api_bp.route("/fees/pay", methods=["POST"])
@login_required
def pay_fees():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # In a real implementation, you would process the payment through Paystack
        # For now, we'll just return a success message
        
        return jsonify({
            "success": True,
            "message": "Payment initiated successfully",
            "payment_reference": f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to process payment: {str(e)}"}), 500

# Profile management endpoints
@student_api_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch the student's profile from the database
        # For now, we'll use the current_user object and add some sample data
        
        # Basic profile information
        profile = {
            "id": current_user.id,
            "student_id": current_user.student_id,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname,
            "email": current_user.email,
            "phone": current_user.phone if hasattr(current_user, 'phone') else "",
            "class_assigned": current_user.class_assigned,
            "gender": current_user.gender,
            "image_link": current_user.image_link,
            "date_of_birth": current_user.date_of_birth.isoformat() if hasattr(current_user, 'date_of_birth') and current_user.date_of_birth else None,
            "address": current_user.address if hasattr(current_user, 'address') else "",
            "status": current_user.status
        }
        
        # Academic information
        academic_info = {
            "student_id": current_user.student_id,
            "class": "Grade 10-A (Science Stream)",
            "class_teacher": "Mr. Robert Johnson",
            "current_gpa": 3.75,
            "class_rank": "5th out of 30 students",
            "attendance_rate": "91.9% (Current Term)"
        }
        
        # Emergency contacts (sample data)
        emergency_contacts = [
            {
                "type": "primary",
                "name": "Michael Doe",
                "relationship": "Father",
                "phone": "+1 (555) 987-6543",
                "email": "michael.doe@example.com",
                "address": "123 Student Lane, Knowledge City, KN 12345"
            },
            {
                "type": "secondary",
                "name": "Sarah Doe",
                "relationship": "Mother",
                "phone": "+1 (555) 789-0123",
                "email": "sarah.doe@example.com",
                "address": "123 Student Lane, Knowledge City, KN 12345"
            }
        ]
        
        # Health information (sample data)
        health_info = {
            "blood_type": "A+",
            "allergies": "Peanuts, Penicillin",
            "medications": "None",
            "medical_conditions": "Mild asthma",
            "doctor_name": "Dr. Emily Wilson",
            "doctor_contact": "+1 (555) 456-7890"
        }
        
        return jsonify({
            "success": True,
            "profile": {
                "basic_info": profile,
                "academic_info": academic_info,
                "emergency_contacts": emergency_contacts,
                "health_info": health_info
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch profile: {str(e)}"}), 500

@student_api_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # In a real implementation, you would update the student's profile in the database
        # For now, we'll just return a success message
        
        # Fields that can be updated
        updatable_fields = ['phone', 'address', 'image_link', 'emergency_contacts', 'health_info']
        
        # Check if any updatable field is provided
        if not any(field in data for field in updatable_fields):
            return jsonify({"error": "No valid fields to update"}), 400
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

@student_api_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['current_password', 'new_password', 'confirm_password']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if new password and confirm password match
        if data['new_password'] != data['confirm_password']:
            return jsonify({"error": "New password and confirm password do not match"}), 400
        
        # In a real implementation, you would verify the current password and update the password in the database
        # For now, we'll just return a success message
        
        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to change password: {str(e)}"}), 500

# Session-based caching implementation
@student_api_bp.route("/cache/clear", methods=["POST"])
@login_required
def clear_cache():
    if current_user.role.lower() != "student":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Clear all cached data in the session
        for key in list(session.keys()):
            if key.startswith('cache_student_'):
                session.pop(key)
        
        return jsonify({
            "success": True,
            "message": "Cache cleared successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to clear cache: {str(e)}"}), 500
