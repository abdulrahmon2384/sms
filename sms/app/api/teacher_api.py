from flask import Blueprint, jsonify, request, session, abort
from flask_login import current_user, login_required
from ..models.teacher_model import Teacher
from ..models.student_model import Student
from ..models.attendance_model import Attendance
from ..models.performance_model import Performance
from .. import db
import json
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd
import numpy as np

# Create a Blueprint with the proper URL prefix
teacher_api_bp = Blueprint("teacher_api", __name__, url_prefix="/api/teacher")

# Dashboard statistics
@teacher_api_bp.route("/dashboard/stats", methods=["GET"])
@login_required
def dashboard_stats():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get assigned classes
        teacher_id = current_user.id
        
        # In a real implementation, you would fetch actual data
        # For now, we'll generate some sample data
        
        # Get total students in teacher's classes
        total_students = 75  # Example count
        
        # Get average attendance rate
        attendance_rate = 94.2  # Example rate
        
        # Get average performance score
        average_performance = 78.5  # Example score
        
        # Get recent activities
        recent_activities = [
            {"type": "attendance", "description": "Marked attendance for Grade 10-A", "timestamp": datetime.now().isoformat()},
            {"type": "grade", "description": "Updated test scores for Mathematics", "timestamp": (datetime.now() - timedelta(hours=3)).isoformat()},
            {"type": "assignment", "description": "Posted new assignment for Science", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()},
            {"type": "meeting", "description": "Scheduled parent-teacher meeting", "timestamp": (datetime.now() - timedelta(days=2)).isoformat()},
        ]
        
        # Get upcoming events
        upcoming_events = [
            {"title": "Science Quiz", "date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'), "class": "Grade 10-A"},
            {"title": "Mathematics Test", "date": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'), "class": "Grade 10-B"},
            {"title": "Parent-Teacher Meeting", "date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'), "class": "All Classes"},
        ]
        
        return jsonify({
            "success": True,
            "stats": {
                "total_students": total_students,
                "attendance_rate": attendance_rate,
                "average_performance": average_performance,
                "recent_activities": recent_activities,
                "upcoming_events": upcoming_events
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch dashboard statistics: {str(e)}"}), 500

# Attendance management endpoints
@teacher_api_bp.route("/attendance/classes", methods=["GET"])
@login_required
def get_classes_for_attendance():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch the teacher's assigned classes
        # For now, we'll return sample data
        
        classes = [
            {"id": 1, "name": "Grade 10-A", "subject": "Mathematics", "students_count": 30},
            {"id": 2, "name": "Grade 10-B", "subject": "Mathematics", "students_count": 28},
            {"id": 3, "name": "Grade 11-A", "subject": "Physics", "students_count": 25},
        ]
        
        return jsonify({
            "success": True,
            "classes": classes
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch classes: {str(e)}"}), 500

@teacher_api_bp.route("/attendance/students/<int:class_id>", methods=["GET"])
@login_required
def get_students_for_attendance(class_id):
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch students in the specified class
        # For now, we'll return sample data
        
        # Sample class names based on class_id
        class_names = {
            1: "Grade 10-A",
            2: "Grade 10-B",
            3: "Grade 11-A"
        }
        
        class_name = class_names.get(class_id, "Unknown Class")
        
        # Generate sample students
        students = []
        for i in range(1, 26):  # 25 students
            students.append({
                "id": i,
                "student_id": f"STU-2025-{i:03d}",
                "name": f"Student {i}",
                "image_link": f"https://f005.backblazeb2.com/file/School-management-system/student-{i % 10}.jpg",
                "attendance_history": {
                    "present": np.random.randint(15, 20),
                    "absent": np.random.randint(0, 3),
                    "late": np.random.randint(0, 2)
                }
            })
        
        return jsonify({
            "success": True,
            "class_name": class_name,
            "date": datetime.now().strftime('%Y-%m-%d'),
            "students": students
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch students: {str(e)}"}), 500

@teacher_api_bp.route("/attendance/mark", methods=["POST"])
@login_required
def mark_attendance():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['class_id', 'date', 'attendance_data']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # In a real implementation, you would save the attendance data to the database
        # For now, we'll just return a success message
        
        # Example of how attendance_data might look:
        # [
        #   {"student_id": 1, "status": "present"},
        #   {"student_id": 2, "status": "absent"},
        #   {"student_id": 3, "status": "late"}
        # ]
        
        return jsonify({
            "success": True,
            "message": "Attendance marked successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to mark attendance: {str(e)}"}), 500

@teacher_api_bp.route("/attendance/history/<int:class_id>", methods=["GET"])
@login_required
def get_attendance_history(class_id):
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Get query parameters
        start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        
        # In a real implementation, you would fetch attendance history from the database
        # For now, we'll generate sample data
        
        # Sample class names based on class_id
        class_names = {
            1: "Grade 10-A",
            2: "Grade 10-B",
            3: "Grade 11-A"
        }
        
        class_name = class_names.get(class_id, "Unknown Class")
        
        # Generate dates between start_date and end_date
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        dates = [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end - start).days + 1)]
        
        # Generate attendance summary for each date
        attendance_summary = []
        for date in dates:
            # Skip weekends
            day_of_week = datetime.strptime(date, '%Y-%m-%d').weekday()
            if day_of_week >= 5:  # 5 = Saturday, 6 = Sunday
                continue
                
            present = np.random.randint(20, 26)
            absent = np.random.randint(0, 4)
            late = np.random.randint(0, 3)
            total = present + absent + late
            
            attendance_summary.append({
                "date": date,
                "present": present,
                "absent": absent,
                "late": late,
                "total": total,
                "attendance_rate": round((present / total) * 100, 1)
            })
        
        return jsonify({
            "success": True,
            "class_name": class_name,
            "attendance_summary": attendance_summary
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch attendance history: {str(e)}"}), 500

# Performance tracking endpoints
@teacher_api_bp.route("/performance/classes", methods=["GET"])
@login_required
def get_classes_for_performance():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch the teacher's assigned classes
        # For now, we'll return sample data
        
        classes = [
            {"id": 1, "name": "Grade 10-A", "subject": "Mathematics", "students_count": 30},
            {"id": 2, "name": "Grade 10-B", "subject": "Mathematics", "students_count": 28},
            {"id": 3, "name": "Grade 11-A", "subject": "Physics", "students_count": 25},
        ]
        
        return jsonify({
            "success": True,
            "classes": classes
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch classes: {str(e)}"}), 500

@teacher_api_bp.route("/performance/students/<int:class_id>", methods=["GET"])
@login_required
def get_students_for_performance(class_id):
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch students in the specified class
        # For now, we'll return sample data
        
        # Sample class names based on class_id
        class_names = {
            1: "Grade 10-A",
            2: "Grade 10-B",
            3: "Grade 11-A"
        }
        
        class_name = class_names.get(class_id, "Unknown Class")
        
        # Generate sample students with performance data
        students = []
        for i in range(1, 26):  # 25 students
            students.append({
                "id": i,
                "student_id": f"STU-2025-{i:03d}",
                "name": f"Student {i}",
                "image_link": f"https://f005.backblazeb2.com/file/School-management-system/student-{i % 10}.jpg",
                "performance": {
                    "assignments": round(np.random.uniform(60, 100), 1),
                    "quizzes": round(np.random.uniform(60, 100), 1),
                    "tests": round(np.random.uniform(60, 100), 1),
                    "participation": round(np.random.uniform(60, 100), 1),
                    "overall": round(np.random.uniform(60, 100), 1)
                }
            })
        
        return jsonify({
            "success": True,
            "class_name": class_name,
            "term": "First Term",
            "academic_year": "2024-2025",
            "students": students
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch students: {str(e)}"}), 500

@teacher_api_bp.route("/performance/record", methods=["POST"])
@login_required
def record_performance():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['class_id', 'student_id', 'assessment_type', 'score', 'max_score', 'assessment_name']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # In a real implementation, you would save the performance data to the database
        # For now, we'll just return a success message
        
        return jsonify({
            "success": True,
            "message": "Performance recorded successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to record performance: {str(e)}"}), 500

@teacher_api_bp.route("/performance/analytics/<int:class_id>", methods=["GET"])
@login_required
def get_performance_analytics(class_id):
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch performance analytics from the database
        # For now, we'll generate sample data
        
        # Sample class names based on class_id
        class_names = {
            1: "Grade 10-A",
            2: "Grade 10-B",
            3: "Grade 11-A"
        }
        
        class_name = class_names.get(class_id, "Unknown Class")
        
        # Generate performance distribution
        score_ranges = ['0-59', '60-69', '70-79', '80-89', '90-100']
        distribution = [np.random.randint(0, 5), np.random.randint(3, 8), np.random.randint(5, 10), np.random.randint(5, 10), np.random.randint(2, 7)]
        
        # Generate performance by assessment type
        assessment_types = ['Assignments', 'Quizzes', 'Tests', 'Participation']
        assessment_averages = [round(np.random.uniform(70, 85), 1) for _ in range(4)]
        
        # Generate performance trend over time
        months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
        trend = [round(np.random.uniform(70, 85), 1) for _ in range(6)]
        
        return jsonify({
            "success": True,
            "class_name": class_name,
            "term": "First Term",
            "academic_year": "2024-2025",
            "analytics": {
                "distribution": {
                    "ranges": score_ranges,
                    "counts": distribution
                },
                "by_assessment_type": {
                    "types": assessment_types,
                    "averages": assessment_averages
                },
                "trend": {
                    "months": months,
                    "averages": trend
                },
                "class_average": round(sum(trend) / len(trend), 1)
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch performance analytics: {str(e)}"}), 500

# Profile management endpoints
@teacher_api_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # In a real implementation, you would fetch the teacher's profile from the database
        # For now, we'll use the current_user object
        
        return jsonify({
            "success": True,
            "profile": {
                "id": current_user.id,
                "teacher_id": current_user.teacher_id,
                "firstname": current_user.firstname,
                "lastname": current_user.lastname,
                "email": current_user.email,
                "phone": current_user.phone,
                "department": current_user.department,
                "subjects": current_user.subjects,
                "gender": current_user.gender,
                "image_link": current_user.image_link,
                "date_of_birth": current_user.date_of_birth.isoformat() if hasattr(current_user, 'date_of_birth') and current_user.date_of_birth else None,
                "address": current_user.address if hasattr(current_user, 'address') else "",
                "status": current_user.status
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch profile: {str(e)}"}), 500

@teacher_api_bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        data = request.get_json()
        
        # In a real implementation, you would update the teacher's profile in the database
        # For now, we'll just return a success message
        
        # Fields that can be updated
        updatable_fields = ['phone', 'address', 'image_link']
        
        # Check if any updatable field is provided
        if not any(field in data for field in updatable_fields):
            return jsonify({"error": "No valid fields to update"}), 400
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

@teacher_api_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    if current_user.role.lower() != "teacher":
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
@teacher_api_bp.route("/cache/clear", methods=["POST"])
@login_required
def clear_cache():
    if current_user.role.lower() != "teacher":
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Clear all cached data in the session
        for key in list(session.keys()):
            if key.startswith('cache_teacher_'):
                session.pop(key)
        
        return jsonify({
            "success": True,
            "message": "Cache cleared successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to clear cache: {str(e)}"}), 500
