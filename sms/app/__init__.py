from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os, zlib
from sqlalchemy import text
from sqlalchemy.orm import scoped_session
from cryptography.fernet import Fernet
from .db_config import cipher, FERNET_KEY
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from the .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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

# Make B2 integration optional
b2_api = None
bucket = None

try:
    if B2_ACCOUNT_ID and B2_APP_KEY and B2_BUCKET_NAME:
        from b2sdk.v2 import B2Api, InMemoryAccountInfo
        # Initialize Backblaze B2 API
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", B2_ACCOUNT_ID, B2_APP_KEY)
        bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)
        logger.info("Backblaze B2 integration initialized successfully")
    else:
        logger.warning("Backblaze B2 credentials not found, B2 integration disabled")
except Exception as e:
    logger.error(f"Error initializing Backblaze B2: {e}")
    logger.warning("Backblaze B2 integration disabled due to error")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Import and register blueprints at the bottom
from .routes import routes_bp
from .api import api_bp

app.register_blueprint(routes_bp)
app.register_blueprint(api_bp)

def is_schema_set(session: scoped_session) -> bool:
    result = session.execute(text("SELECT current_schema();")).fetchone()
    current_schema = result[0] if result else None
    return current_schema is not None and current_schema != 'public'

@login_manager.user_loader
def load_user(user_id):
    # import User model Blueprint
    from .models.admin_model import Admin
    from .models.student_model import Students
    from .models.teacher_model import Teachers

    user_models = [Admin, Teachers, Students]
    if not is_schema_set(db.session):
        return redirect(url_for("routes.auth.select_school"))
    
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
    else:
        login_manager.login_view = 'select_school'

    if alreadyLogged:
        login_manager.login_view = 'dashboard'
    else:
        login_manager.login_view = 'login'  

# redirect unauthorize user to login page 
@login_manager.unauthorized_handler
def unauthorized():
    schoolChoosed = session.get("schoolID")
    alreadyLogged = session.get("login")

    if alreadyLogged:
        redirect("/dashboard")
    elif not schoolChoosed:
        redirect('/choose-school')

    return redirect('/login')
