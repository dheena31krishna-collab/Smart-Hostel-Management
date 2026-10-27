import os
import unittest
from datetime import datetime, date, time
from app import create_app
from models import db
from models.user import User
from models.student import Student
from models.warden import Warden
from models.complaint import Complaint
from models.attendance import AttendanceSession, Attendance
from models.outing import OutingRequest

from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class SmartHostelTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app to use in-memory SQLite database for testing
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation_and_password_hashing(self):
        """Test that passwords are correctly hashed and validated."""
        with self.app.app_context():
            u = User(name="Test User", email="test@domain.com", role="student")
            u.set_password("mypassword123")
            db.session.add(u)
            db.session.commit()

            user_db = User.query.filter_by(email="test@domain.com").first()
            self.assertIsNotNone(user_db)
            self.assertTrue(user_db.check_password("mypassword123"))
            self.assertFalse(user_db.check_password("wrongpassword"))
            self.assertNotEqual(user_db.password_hash, "mypassword123")

    def test_student_and_warden_profile_linkage(self):
        """Test the 1-to-1 relationship mapping of user roles."""
        with self.app.app_context():
            # Warden User
            w_user = User(name="Warden Xavier", email="warden@test.com", role="warden")
            w_user.set_password("admin123")
            db.session.add(w_user)
            db.session.commit()

            w_profile = Warden(user_id=w_user.id, employee_id="EMP001")
            db.session.add(w_profile)

            # Student User
            s_user = User(name="Student Alex", email="student@test.com", role="student")
            s_user.set_password("student123")
            db.session.add(s_user)
            db.session.commit()

            s_profile = Student(
                user_id=s_user.id,
                student_id="STU001",
                department="CSE",
                year=3,
                room_number="A-102"
            )
            db.session.add(s_profile)
            db.session.commit()

            # Retrieve profile checks
            self.assertEqual(w_user.warden_profile.employee_id, "EMP001")
            self.assertEqual(s_user.student_profile.student_id, "STU001")
            self.assertEqual(s_profile.user.name, "Student Alex")

    def test_complaint_creation_flow(self):
        """Test creation and default status of raised complaints."""
        with self.app.app_context():
            s_user = User(name="Student Alex", email="student@test.com", role="student")
            s_user.set_password("student123")
            db.session.add(s_user)
            db.session.commit()

            s_profile = Student(user_id=s_user.id, student_id="STU001", department="CSE", year=3, room_number="A-102")
            db.session.add(s_profile)
            db.session.commit()

            c = Complaint(
                complaint_id="CMP-123456",
                student_id=s_profile.id,
                category="Electrical",
                title="Broken fan",
                description="Fan speed regulator is broken",
                room_number=s_profile.room_number
            )
            db.session.add(c)
            db.session.commit()

            complaint_db = Complaint.query.filter_by(complaint_id="CMP-123456").first()
            self.assertIsNotNone(complaint_db)
            self.assertEqual(complaint_db.status, "Pending")
            self.assertEqual(complaint_db.student.user.name, "Student Alex")

    def test_auth_protected_routes(self):
        """Test that unauthorized user is redirected when requesting dashboard."""
        response = self.client.get('/student/dashboard', follow_redirects=True)
        # Should redirect to login page
        self.assertIn(b"Please login to access the dashboard", response.data)
        self.assertIn(b"Welcome Back", response.data)

if __name__ == '__main__':
    unittest.main()
