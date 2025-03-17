"""
Payment module for Intelleva School Management System.
Implements Paystack integration for payment processing.
"""
import os
import json
import random
import string
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from .models.student_model import Students, Fees
from .models.teacher_model import Teachers, TeacherSalary
from .models.admin_model import School_information
from . import db
from .db_config import encrypt_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Paystack configuration (demo mode)
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_demo_key_for_development")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY", "pk_test_demo_key_for_development")
PAYSTACK_BASE_URL = "https://api.paystack.co"

# Initialize payment blueprint
payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

def generate_reference():
    """Generate a unique transaction reference."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"INTELLEVA-{timestamp}-{random_str}"

def initialize_transaction(email, amount, reference, metadata=None, callback_url=None):
    """
    Initialize a Paystack transaction.
    
    Args:
        email: Customer email
        amount: Amount in kobo (Naira * 100)
        reference: Unique transaction reference
        metadata: Additional data to store with transaction
        callback_url: URL to redirect after payment
        
    Returns:
        Dictionary with transaction details or error
    """
    # In demo mode, simulate Paystack API response
    if "test" in PAYSTACK_SECRET_KEY or "demo" in PAYSTACK_SECRET_KEY:
        logger.info(f"DEMO MODE: Initializing transaction for {email}, amount: {amount/100} Naira")
        
        # Simulate successful transaction initialization
        return {
            "status": True,
            "message": "Authorization URL created",
            "data": {
                "authorization_url": f"/payment/demo-payment/{reference}",
                "access_code": "demo_access_code",
                "reference": reference
            }
        }
    
    # Real Paystack integration
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email,
        "amount": amount,  # Amount in kobo
        "reference": reference,
        "callback_url": callback_url
    }
    
    if metadata:
        payload["metadata"] = metadata
    
    try:
        response = requests.post(
            f"{PAYSTACK_BASE_URL}/transaction/initialize",
            headers=headers,
            json=payload
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error initializing Paystack transaction: {e}")
        return {
            "status": False,
            "message": f"Error initializing transaction: {str(e)}"
        }

def verify_transaction(reference):
    """
    Verify a Paystack transaction.
    
    Args:
        reference: Transaction reference to verify
        
    Returns:
        Dictionary with transaction details or error
    """
    # In demo mode, simulate Paystack API response
    if "test" in PAYSTACK_SECRET_KEY or "demo" in PAYSTACK_SECRET_KEY:
        logger.info(f"DEMO MODE: Verifying transaction {reference}")
        
        # Simulate successful transaction verification
        return {
            "status": True,
            "message": "Verification successful",
            "data": {
                "status": "success",
                "reference": reference,
                "amount": 50000,  # 500 Naira in kobo
                "paid_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "channel": "card",
                "metadata": {}
            }
        }
    
    # Real Paystack integration
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers=headers
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error verifying Paystack transaction: {e}")
        return {
            "status": False,
            "message": f"Error verifying transaction: {str(e)}"
        }

def create_virtual_account(customer_code, first_name, last_name, email, phone):
    """
    Create a dedicated virtual account for a customer.
    
    Args:
        customer_code: Paystack customer code
        first_name: Customer first name
        last_name: Customer last name
        email: Customer email
        phone: Customer phone number
        
    Returns:
        Dictionary with virtual account details or error
    """
    # In demo mode, simulate Paystack API response
    if "test" in PAYSTACK_SECRET_KEY or "demo" in PAYSTACK_SECRET_KEY:
        logger.info(f"DEMO MODE: Creating virtual account for {email}")
        
        # Generate a random 10-digit account number
        account_number = ''.join(random.choices(string.digits, k=10))
        
        # Simulate successful virtual account creation
        return {
            "status": True,
            "message": "Virtual account created",
            "data": {
                "account_number": account_number,
                "account_name": f"{first_name} {last_name}",
                "bank_name": "Intelleva Demo Bank",
                "customer_code": customer_code
            }
        }
    
    # Real Paystack integration
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "customer": customer_code,
        "preferred_bank": "test-bank"
    }
    
    try:
        response = requests.post(
            f"{PAYSTACK_BASE_URL}/dedicated_account",
            headers=headers,
            json=payload
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error creating Paystack virtual account: {e}")
        return {
            "status": False,
            "message": f"Error creating virtual account: {str(e)}"
        }

def create_customer(email, first_name, last_name, phone):
    """
    Create a Paystack customer.
    
    Args:
        email: Customer email
        first_name: Customer first name
        last_name: Customer last name
        phone: Customer phone number
        
    Returns:
        Dictionary with customer details or error
    """
    # In demo mode, simulate Paystack API response
    if "test" in PAYSTACK_SECRET_KEY or "demo" in PAYSTACK_SECRET_KEY:
        logger.info(f"DEMO MODE: Creating customer for {email}")
        
        # Generate a random customer code
        customer_code = f"CUS_{''.join(random.choices(string.ascii_uppercase + string.digits, k=12))}"
        
        # Simulate successful customer creation
        return {
            "status": True,
            "message": "Customer created",
            "data": {
                "id": random.randint(1000000, 9999999),
                "customer_code": customer_code,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone
            }
        }
    
    # Real Paystack integration
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone
    }
    
    try:
        response = requests.post(
            f"{PAYSTACK_BASE_URL}/customer",
            headers=headers,
            json=payload
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error creating Paystack customer: {e}")
        return {
            "status": False,
            "message": f"Error creating customer: {str(e)}"
        }

def process_student_payment(student_id, amount, payment_type, term=None, session_name=None, description=None):
    """
    Process a payment for a student.
    
    Args:
        student_id: Student ID
        amount: Amount to pay in Naira
        payment_type: Type of payment (tuition, lesson, textbook, etc.)
        term: School term
        session_name: School session
        description: Payment description
        
    Returns:
        Dictionary with payment details or error
    """
    try:
        # Get student details
        student = Students.query.get(student_id)
        if not student:
            return {
                "status": False,
                "message": "Student not found"
            }
        
        # Generate a unique reference
        reference = generate_reference()
        
        # Convert amount to kobo (Naira * 100)
        amount_kobo = int(float(amount) * 100)
        
        # Prepare metadata
        metadata = {
            "student_id": student_id,
            "payment_type": payment_type,
            "term": term,
            "session": session_name,
            "description": description
        }
        
        # Initialize transaction
        callback_url = f"/payment/verify/{reference}"
        result = initialize_transaction(
            email=student.email or "student@intelleva.com",
            amount=amount_kobo,
            reference=reference,
            metadata=metadata,
            callback_url=callback_url
        )
        
        if result["status"]:
            # Create a new fee record with pending status
            fee = Fees(
                student_id=student_id,
                amount=float(amount),
                payment_date=datetime.now(),
                payment_method="Paystack",
                payment_status="pending",
                term=term,
                session=session_name,
                description=description or f"{payment_type} payment",
                transaction_reference=reference,
                payment_details={
                    "payment_type": payment_type,
                    "processor": "Paystack",
                    "authorization_url": result["data"]["authorization_url"],
                    "access_code": result["data"]["access_code"],
                    "reference": reference,
                    "status": "pending",
                    "initiated_at": datetime.now().isoformat()
                }
            )
            db.session.add(fee)
            
            # Update student payment history
            payment_history = student.payment_history or []
            payment_history.append({
                "date": datetime.now().isoformat(),
                "amount": float(amount),
                "type": payment_type,
                "status": "pending",
                "reference": reference,
                "method": "Paystack",
                "details": {
                    "term": term,
                    "session": session_name,
                    "processor": "Paystack",
                    "initiated_at": datetime.now().isoformat()
                }
            })
            student.payment_history = payment_history
            
            db.session.commit()
            
            return {
                "status": True,
                "message": "Payment initiated successfully",
                "data": {
                    "authorization_url": result["data"]["authorization_url"],
                    "reference": reference
                }
            }
        else:
            return result
    except Exception as e:
        logger.error(f"Error processing student payment: {e}")
        db.session.rollback()
        return {
            "status": False,
            "message": f"Error processing payment: {str(e)}"
        }

def process_teacher_salary(teacher_id, amount, month, year, description=None):
    """
    Process a salary payment for a teacher.
    
    Args:
        teacher_id: Teacher ID
        amount: Salary amount in Naira
        month: Month of salary
        year: Year of salary
        description: Payment description
        
    Returns:
        Dictionary with payment details or error
    """
    try:
        # Get teacher details
        teacher = Teachers.query.get(teacher_id)
        if not teacher:
            return {
                "status": False,
                "message": "Teacher not found"
            }
        
        # Generate a unique reference
        reference = generate_reference()
        
        # Prepare payment details
        payment_details = {
            "processor": "Paystack",
            "processor_fee": round(float(amount) * 0.015, 2),
            "payment_date": datetime.now().isoformat(),
            "payment_time": datetime.now().strftime("%H:%M:%S"),
            "approver": session.get("username", "admin"),
            "bank_name": "Intelleva Bank",
            "account_type": "Salary",
            "tax_deductions": round(float(amount) * 0.1, 2),
            "benefits": round(float(amount) * 0.05, 2),
            "net_amount": round(float(amount) * 0.95, 2),
            "reference": reference,
            "status": "paid",
            "processed_at": datetime.now().isoformat()
        }
        
        # Create a new salary record
        salary = TeacherSalary(
            teacher_id=teacher_id,
            amount=float(amount),
            payment_date=datetime.now(),
            payment_method="Paystack",
            payment_status="paid",
            month=month,
            year=year,
            description=description or f"Salary for {month} {year}",
            transaction_reference=reference,
            payment_details=payment_details
        )
        db.session.add(salary)
        
        # Update teacher payment history
        payment_history = teacher.payment_history or []
        payment_history.append({
            "date": datetime.now().isoformat(),
            "amount": float(amount),
            "type": "salary",
            "status": "successful",
            "reference": reference,
            "method": "Paystack",
            "details": {
                "month": month,
                "year": year,
                "processor": "Paystack",
                "processor_fee": round(float(amount) * 0.015, 2),
                "tax_deductions": round(float(amount) * 0.1, 2),
                "net_amount": round(float(amount) * 0.95, 2)
            }
        })
        teacher.payment_history = payment_history
        
        db.session.commit()
        
        return {
            "status": True,
            "message": "Salary payment processed successfully",
            "data": {
                "reference": reference,
                "amount": float(amount),
                "net_amount": round(float(amount) * 0.95, 2)
            }
        }
    except Exception as e:
        logger.error(f"Error processing teacher salary: {e}")
        db.session.rollback()
        return {
            "status": False,
            "message": f"Error processing salary: {str(e)}"
        }

def verify_and_update_payment(reference):
    """
    Verify a payment and update records.
    
    Args:
        reference: Transaction reference to verify
        
    Returns:
        Dictionary with verification details or error
    """
    try:
        # Verify transaction with Paystack
        result = verify_transaction(reference)
        
        if result["status"] and result["data"]["status"] == "success":
            # Find the fee record
            fee = Fees.query.filter_by(transaction_reference=reference).first()
            if fee:
                # Update fee status
                fee.payment_status = "paid"
                
                # Update payment details
                payment_details = fee.payment_details or {}
                payment_details.update({
                    "status": "successful",
                    "paid_at": result["data"]["paid_at"],
                    "channel": result["data"]["channel"],
                    "verified_at": datetime.now().isoformat()
                })
                fee.payment_details = payment_details
                
                # Get student
                student = Students.query.get(fee.student_id)
                if student:
                    # Update student payment history
                    payment_history = student.payment_history or []
                    for i, payment in enumerate(payment_history):
                        if payment.get("reference") == reference:
                            payment_history[i]["status"] = "successful"
                            payment_history[i]["details"]["paid_at"] = result["data"]["paid_at"]
                            payment_history[i]["details"]["verified_at"] = datetime.now().isoformat()
                            break
                    student.payment_history = payment_history
                
                db.session.commit()
                
                return {
                    "status": True,
                    "message": "Payment verified successfully",
                    "data": {
                        "reference": reference,
                        "amount": fee.amount,
                        "student_id": fee.student_id,
                        "payment_type": payment_details.get("payment_type")
                    }
                }
            else:
                return {
                    "status": False,
                    "message": "Fee record not found for this reference"
                }
        else:
            return {
                "status": False,
                "message": "Payment verification failed",
                "data": result
            }
    except Exception as e:
        logger.error(f"Error verifying payment: {e}")
        db.session.rollback()
        return {
            "status": False,
            "message": f"Error verifying payment: {str(e)}"
        }

def get_payment_history(student_id=None, teacher_id=None, start_date=None, end_date=None, payment_type=None, status=None):
    """
    Get payment history for a student or teacher.
    
    Args:
        student_id: Student ID (optional)
        teacher_id: Teacher ID (optional)
        start_date: Start date for filtering (optional)
        end_date: End date for filtering (optional)
        payment_type: Type of payment for filtering (optional)
        status: Payment status for filtering (optional)
        
    Returns:
        List of payments
    """
    try:
        if student_id:
            # Get student payment history
            query = Fees.query.filter_by(student_id=student_id)
            
            # Apply filters
            if start_date:
                query = query.filter(Fees.payment_date >= start_date)
            if end_date:
                query = query.filter(Fees.payment_date <= end_date)
            if payment_type:
                # Filter by payment type in payment_details
                pass  # Requires custom SQL or post-processing
            if status:
                query = query.filter_by(payment_status=status)
            
            # Execute query
            fees = query.order_by(Fees.payment_date.desc()).all()
            
            # Convert to list of dictionaries
            payments = []
            for fee in fees:
                payment_details = fee.payment_details or {}
                payments.append({
                    "id": fee.id,
                    "student_id": fee.student_id,
                    "amount": fee.amount,
                    "payment_date": fee.payment_date.isoformat() if fee.payment_date else None,
                    "payment_method": fee.payment_method,
                    "payment_status": fee.payment_status,
                    "term": fee.term,
                    "session": fee.session,
                    "description": fee.description,
                    "transaction_reference": fee.transaction_reference,
                    "payment_type": payment_details.get("payment_type"),
                    "processor": payment_details.get("processor"),
                    "paid_at": payment_details.get("paid_at"),
                    "channel": payment_details.get("channel")
                })
            
            return {
                "status": True,
                "message": "Payment history retrieved successfully",
                "data": payments
            }
        elif teacher_id:
            # Get teacher payment history
            query = TeacherSalary.query.filter_by(teacher_id=teacher_id)
            
            # Apply filters
            if start_date:
                query = query.filter(TeacherSalary.payment_date >= start_date)
            if end_date:
                query = query.filter(TeacherSalary.payment_date <= end_date)
            if status:
                query = query.filter_by(payment_status=status)
            
            # Execute query
            salaries = query.order_by(TeacherSalary.payment_date.desc()).all()
            
            # Convert to list of dictionaries
            payments = []
            for salary in salaries:
                payment_details = salary.payment_details or {}
                payments.append({
                    "id": salary.id,
                    "teacher_id": salary.teacher_id,
                    "amount": salary.amount,
                    "payment_date": salary.payment_date.isoformat() if salary.payment_date else None,
                    "payment_method": salary.payment_method,
                    "payment_status": salary.payment_status,
                    "month": salary.month,
                    "year": salary.year,
                    "description": salary.description,
                    "transaction_reference": salary.transaction_reference,
                    "processor": payment_details.get("processor"),
                    "net_amount": payment_details.get("net_amount"),
                    "tax_deductions": payment_details.get("tax_deductions"),
                    "benefits": payment_details.get("benefits")
                })
            
            return {
                "status": True,
                "message": "Salary history retrieved successfully",
                "data": payments
            }
        else:
            return {
                "status": False,
                "message": "Either student_id or teacher_id must be provided"
            }
    except Exception as e:
        logger.error(f"Error getting payment history: {e}")
        return {
            "status": False,
            "message": f"Error getting payment history: {str(e)}"
        }

def get_payment_summary(school_id=None, start_date=None, end_date=None):
    """
    Get payment summary for a school.
    
    Args:
        school_id: School ID (optional)
        start_date: Start date for filtering (optional)
        end_date: End date for filtering (optional)
        
    Returns:
        Dictionary with payment summary
    """
    try:
        # Set schema for this school if provided
        if school_id:
            db.session.execute(text(f"SET search_path TO {school_id}"))
            db.session.commit()
        
        # Query for student fees
        fee_query = Fees.query
        if start_date:
            fee_query = fee_query.filter(Fees.payment_date >= start_date)
        if end_date:
            fee_query = fee_query.filter(Fees.payment_date <= end_date)
        
        # Get all fees
        fees = fee_query.all()
        
        # Query for teacher salaries
        salary_query = TeacherSalary.query
        if start_date:
            salary_query = salary_query.filter(TeacherSalary.payment_date >= start_date)
        if end_date:
            salary_query = salary_query.filter(TeacherSalary.payment_date <= end_date)
        
        # Get all salaries
        salaries = salary_query.all()
        
        # Calculate summary
        total_fees = sum(fee.amount for fee in fees if fee.payment_status == "paid")
        total_pending_fees = sum(fee.amount for fee in fees if fee.payment_status == "pending")
        total_overdue_fees = sum(fee.amount for fee in fees if fee.payment_status == "overdue")
        
        total_salaries = sum(salary.amount for salary in salaries if salary.payment_status == "paid")
        total_pending_salaries = sum(salary.amount for salary in salaries if salary.payment_status == "pending")
        
        # Group fees by term and session
        fees_by_term = {}
        for fee in fees:
            if fee.payment_status == "paid":
                key = f"{fee.term}_{fee.session}"
                if key not in fees_by_term:
                    fees_by_term[key] = 0
                fees_by_term[key] += fee.amount
        
        # Group salaries by month and year
        salaries_by_month = {}
        for salary in salaries:
            if salary.payment_status == "paid":
                key = f"{salary.month}_{salary.year}"
                if key not in salaries_by_month:
                    salaries_by_month[key] = 0
                salaries_by_month[key] += salary.amount
        
        return {
            "status": True,
            "message": "Payment summary retrieved successfully",
            "data": {
                "total_fees": total_fees,
                "total_pending_fees": total_pending_fees,
                "total_overdue_fees": total_overdue_fees,
                "total_salaries": total_salaries,
                "total_pending_salaries": total_pending_salaries,
                "net_income": total_fees - total_salaries,
                "fees_by_term": fees_by_term,
                "salaries_by_month": salaries_by_month,
                "total_transactions": len(fees) + len(salaries),
                "period": {
                    "start_date": start_date.isoformat() if start_date else None,
                    "end_date": end_date.isoformat() if end_date else None
                }
            }
        }
    except Exception as e:
        logger.error(f"Error getting payment summary: {e}")
        return {
            "status": False,
            "message": f"Error getting payment summary: {str(e)}"
        }

# Routes

@payment_bp.route('/initiate-student-payment', methods=['POST'])
def initiate_student_payment():
    """API endpoint to initiate a student payment."""
    data = request.json
    
    student_id = data.get('student_id')
    amount = data.get('amount')
    payment_type = data.get('payment_type')
    term = data.get('term')
    session_name = data.get('session')
    description = data.get('description')
    
    result = process_student_payment(
        student_id=student_id,
        amount=amount,
        payment_type=payment_type,
        term=term,
        session_name=session_name,
        description=description
    )
    
    return jsonify(result)

@payment_bp.route('/process-teacher-salary', methods=['POST'])
def process_teacher_salary_route():
    """API endpoint to process a teacher salary payment."""
    data = request.json
    
    teacher_id = data.get('teacher_id')
    amount = data.get('amount')
    month = data.get('month')
    year = data.get('year')
    description = data.get('description')
    
    result = process_teacher_salary(
        teacher_id=teacher_id,
        amount=amount,
        month=month,
        year=year,
        description=description
    )
    
    return jsonify(result)

@payment_bp.route('/verify/<reference>', methods=['GET'])
def verify_payment_route(reference):
    """Route to verify a payment."""
    result = verify_and_update_payment(reference)
    
    if result["status"]:
        return redirect(url_for('payment.payment_success', reference=reference))
    else:
        return redirect(url_for('payment.payment_failed', reference=reference, message=result["message"]))

@payment_bp.route('/demo-payment/<reference>', methods=['GET'])
def demo_payment(reference):
    """Demo payment page for testing."""
    # Get fee details
    fee = Fees.query.filter_by(transaction_reference=reference).first()
    if not fee:
        return render_template('payment/error.html', message="Payment not found")
    
    student = Students.query.get(fee.student_id)
    if not student:
        return render_template('payment/error.html', message="Student not found")
    
    return render_template(
        'payment/demo_payment.html',
        reference=reference,
        amount=fee.amount,
        student_name=f"{student.firstname} {student.lastname}",
        payment_type=fee.payment_details.get("payment_type", "Fee"),
        description=fee.description
    )

@payment_bp.route('/demo-payment/<reference>/complete', methods=['POST'])
def complete_demo_payment(reference):
    """Complete a demo payment."""
    # Simulate payment verification
    result = verify_and_update_payment(reference)
    
    if result["status"]:
        return redirect(url_for('payment.payment_success', reference=reference))
    else:
        return redirect(url_for('payment.payment_failed', reference=reference, message=result["message"]))

@payment_bp.route('/success', methods=['GET'])
def payment_success():
    """Payment success page."""
    reference = request.args.get('reference')
    
    # Get payment details
    fee = Fees.query.filter_by(transaction_reference=reference).first()
    if not fee:
        return render_template('payment/error.html', message="Payment not found")
    
    student = Students.query.get(fee.student_id)
    if not student:
        return render_template('payment/error.html', message="Student not found")
    
    return render_template(
        'payment/success.html',
        reference=reference,
        amount=fee.amount,
        student_name=f"{student.firstname} {student.lastname}",
        payment_type=fee.payment_details.get("payment_type", "Fee"),
        description=fee.description
    )

@payment_bp.route('/failed', methods=['GET'])
def payment_failed():
    """Payment failed page."""
    reference = request.args.get('reference')
    message = request.args.get('message', "Payment failed")
    
    return render_template(
        'payment/failed.html',
        reference=reference,
        message=message
    )

@payment_bp.route('/history/<student_id>', methods=['GET'])
def student_payment_history(student_id):
    """API endpoint to get student payment history."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_type = request.args.get('payment_type')
    status = request.args.get('status')
    
    result = get_payment_history(
        student_id=student_id,
        start_date=start_date,
        end_date=end_date,
        payment_type=payment_type,
        status=status
    )
    
    return jsonify(result)

@payment_bp.route('/salary-history/<teacher_id>', methods=['GET'])
def teacher_salary_history(teacher_id):
    """API endpoint to get teacher salary history."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    
    result = get_payment_history(
        teacher_id=teacher_id,
        start_date=start_date,
        end_date=end_date,
        status=status
    )
    
    return jsonify(result)

@payment_bp.route('/summary', methods=['GET'])
def payment_summary():
    """API endpoint to get payment summary."""
    school_id = request.args.get('school_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result = get_payment_summary(
        school_id=school_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify(result)
