from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # Admin's main dashboard
    return render_template('admin/index.html')


@admin_bp.route('/students')
@login_required
def students_management():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/student_management.html')


@admin_bp.route('/teachers')
@login_required
def teachers_management():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/teacher_management.html')


@admin_bp.route('/classes')
@login_required
def fclasses_management():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/class_management.html')


@admin_bp.route('/schools')
@login_required
def school_management():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/school_management.html')



@admin_bp.route('/communication')
@login_required
def admin_communication():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/communication.html')



@admin_bp.route('/finance')
@login_required
def financial_insights():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/finacial_management.html')


@admin_bp.route('/profile')
@login_required
def admin_profile():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/profile.html')


@admin_bp.route('/AI')
@login_required
def admin_ai():
    # Admin manages all users (students, teachers, etc.)
    return render_template('admin/ai.html')

