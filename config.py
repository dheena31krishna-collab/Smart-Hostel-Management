import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "smart-hostel-secret-key-98765")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    
    if DB_TYPE == "mysql":
        db_user = os.getenv("MYSQL_USER", "root")
        db_password = os.getenv("MYSQL_PASSWORD", "")
        db_host = os.getenv("MYSQL_HOST", "localhost")
        db_port = os.getenv("MYSQL_PORT", "3306")
        db_name = os.getenv("MYSQL_DB", "smart_hostel_db")
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        # Detect Vercel / Serverless / Linux container environment
        if os.getenv("VERCEL") or os.getenv("VERCEL_ENV") or os.getenv("AWS_LAMBDA_FUNCTION_NAME") or os.name != "nt":
            SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/smart_hostel.db"
        else:
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'smart_hostel.db')}"
