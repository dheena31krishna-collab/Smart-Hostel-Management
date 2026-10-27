import sys
import os

# Add current directory to path
_root = os.path.dirname(os.path.abspath(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)

from app import create_app
from models import db

app = create_app()

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("DB init error:", e)

if __name__ == "__main__":
    app.run()
