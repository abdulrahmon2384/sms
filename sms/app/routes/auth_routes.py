from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import logout_user



# Define a Blueprint for auth routes
auth_bp = Blueprint('auth', __name__)




# homepage
@auth_bp.route("/", methods=['GET', 'POST'])
def home():
    return render_template("auth/homepage.html")




# choose school 
@auth_bp.route('/choose-school', methods=['GET', 'POST'])
def select_school():
     return render_template("auth/choose_school.html")




# register school
@auth_bp.route('/register_school', methods=['GET', 'POST'])
def register_school():
    return render_template("auth/register.html")



# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
      school_choosed = session.get("schoolID")
      if school_choosed:
            return render_template("auth/login.html")
      return redirect(url_for("routes.auth.select_school"))



# Logout route
@auth_bp.route('/logout')
def logout():
	logout_user()
	session["login"] = False
	return redirect(url_for('routes.auth.login'))


# Logout route
@auth_bp.route('/intelleva')
def dashboard():
	return render_template('nav.html')


