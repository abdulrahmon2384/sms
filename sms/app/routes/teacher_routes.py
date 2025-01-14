from flask import Blueprint, render_template, request
from flask_login import login_required


teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')




@teacher_bp.route('/dashboard')
@login_required
def teacher_dashboard():
    # Teacher's main dashboard
    return render_template('teacher/index.html')



@teacher_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def manage_attendance():
    return render_template('teacher/attendance.html')



@teacher_bp.route('/AI')
@login_required
def teacher_ai():
    # Admin manages all users (students, teachers, etc.)
    return render_template('teacher/ai.html')




@teacher_bp.route('/grades', methods=['GET', 'POST'])
@login_required
def manage_performance():
    return render_template('teacher/performance.html')


@teacher_bp.route('/finance', methods=['GET', 'POST'])
@login_required
def finacial_insight():
    return render_template('teacher/fee.html')

@teacher_bp.route('/class', methods=['GET', 'POST'])
@login_required
def fclass_management():
    return render_template('teacher/class.html')



@teacher_bp.route('/communication')
@login_required
def teacher_communication():
    # Admin manages all users (students, teachers, etc.)
    return render_template('teacher/communication.html')




@teacher_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def about_me():
    return render_template('teacher/profile.html')




