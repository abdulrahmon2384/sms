from flask import Flask, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from dotenv import load_dotenv
import os
from sqlalchemy import text


# Load environment variables from the .env file
load_dotenv()


## Initialize Flask App
app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



# Backblaze B2 Credentials
B2_ACCOUNT_ID = os.getenv("B2_ACCOUNT_ID")
B2_APP_KEY = os.getenv("B2_APP_KEY")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")
B2_BUCKET_URL = os.getenv("B2_BUCKET_URL")


# Initialize Backblaze B2 API
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_ACCOUNT_ID, B2_APP_KEY)
bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


# Import and register blueprints at the bottom
from .routes import routes_bp
from .api import api_bp

app.register_blueprint(routes_bp)
app.register_blueprint(api_bp)




@login_manager.user_loader
def load_user(user_id):
    # import User model Blueprint
    from .models.admin_model import Admin
    from .models.student_model import Students
    from .models.teacher_model import Teachers

    user_models = [Admin, Teachers, Students]
    for model in user_models:
        user = model.query.get(user_id)
        if user:
             return user
    return None




# Function to dynamically set the school schema for each request
@app.before_request
def set_school_schema():
    """Ensure the user has selected a school before proceeding."""
    schoolChoosed = session.get("schoolID")
    alreadyLogged = session.get("login")

    if schoolChoosed:
        schoolID = schoolChoosed
        db.session.execute(text("SET search_path TO :schoolID"), {"schoolID": schoolID})
        db.session.commit()

    # Redirect user to dashboard ir logged else login page
    if alreadyLogged:
        login_manager.login_view = 'dashboard'
    else:
        login_manager.login_view = 'login'  
    






# redirect unauthorize user to login page 
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to the login page
    return redirect('/login')




