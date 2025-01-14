from flask import Blueprint, render_template
from flask_login import login_required

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
@login_required
def student_dashboard():
    # Sample student dashboard route
    return render_template('student/index.html')


@student_bp.route('/profile')
@login_required
def student_profile():
    # Return student's profile page
    return render_template('student/profile.html')


@student_bp.route('/grade')
@login_required
def student_performance():
    # Return student's profile page
    return render_template('student/performance.html')


@student_bp.route('/AI')
@login_required
def student_ai():
    # Admin manages all users (students, teachers, etc.)
    return render_template('student/ai.html')





@student_bp.route('/attendance')
@login_required
def student_attendance():
    # Return student's profile page
    return render_template('student/attendance.html')


@student_bp.route('/class')
@login_required
def student_class_info():
    # Return student's profile page
    return render_template('student/class_info.html')



@student_bp.route('/communication')
@login_required
def student_communication():
    # Admin manages all users (students, teachers, etc.)
    return render_template('student/communication.html')




@student_bp.route('/fees')
@login_required
def student_fee():
    # Return student's profile page
    return render_template('student/fee.html')


