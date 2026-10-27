import os
from datetime import datetime, date, time, timedelta
from app import create_app
from models import db
from models.user import User
from models.student import Student
from models.warden import Warden
from models.complaint import Complaint
from models.attendance import AttendanceSession, Attendance
from models.outing import OutingRequest
from models.notification import Notification, Announcement

def seed_database():
    app = create_app()
    with app.app_context():
        print("Recreating database tables...")
        db.drop_all()
        db.create_all()

        print("Seeding database...")

        # 1. Create Users
        # Warden
        warden_user = User(
            name="Dr. Charles Xavier",
            email="warden@smarthostel.com",
            role="warden",
            phone="+919876543210"
        )
        warden_user.set_password("admin123")
        db.session.add(warden_user)

        # Student 1
        student_user1 = User(
            name="Alex Mercer",
            email="student@smarthostel.com",
            role="student",
            phone="+919876543211"
        )
        student_user1.set_password("student123")
        db.session.add(student_user1)

        # Student 2
        student_user2 = User(
            name="Jane Doe",
            email="jane@smarthostel.com",
            role="student",
            phone="+919876543212"
        )
        student_user2.set_password("student123")
        db.session.add(student_user2)

        # Student 3
        student_user3 = User(
            name="John Smith",
            email="john@smarthostel.com",
            role="student",
            phone="+919876543213"
        )
        student_user3.set_password("student123")
        db.session.add(student_user3)

        db.session.commit()

        # 2. Create Warden & Student Profiles
        warden_profile = Warden(
            user_id=warden_user.id,
            employee_id="EMP2026001"
        )
        db.session.add(warden_profile)

        student_profile1 = Student(
            user_id=student_user1.id,
            student_id="STU2026001",
            department="Computer Science",
            year=3,
            room_number="A-102"
        )
        db.session.add(student_profile1)

        student_profile2 = Student(
            user_id=student_user2.id,
            student_id="STU2026002",
            department="Mechanical Engineering",
            year=2,
            room_number="B-205"
        )
        db.session.add(student_profile2)

        student_profile3 = Student(
            user_id=student_user3.id,
            student_id="STU2026003",
            department="Electrical Engineering",
            year=4,
            room_number="C-301"
        )
        db.session.add(student_profile3)

        db.session.commit()

        # 3. Create Sample Complaints
        complaints = [
            Complaint(
                complaint_id="CMP-1001",
                student_id=student_profile1.id,
                category="Electrical",
                title="Broken Ceiling Fan speed regulator",
                description="The ceiling fan in room A-102 is stuck at maximum speed. The regulator does not work at all and it is causing issues sleeping.",
                room_number="A-102",
                status="Pending"
            ),
            Complaint(
                complaint_id="CMP-1002",
                student_id=student_profile1.id,
                category="Plumbing",
                title="Leaky bathroom tap",
                description="The tap in the attached bathroom has a constant leak, wasting a lot of water. It needs washers replaced.",
                room_number="A-102",
                status="In Progress",
                assigned_to="QuickFix Plumbing Services",
                warden_remarks="Plumber scheduled to visit A block tomorrow morning."
            ),
            Complaint(
                complaint_id="CMP-1003",
                student_id=student_profile2.id,
                category="Internet",
                title="WiFi router red light / no connection",
                description="The floor corridor WiFi router for B-2xx rooms is showing a red internet status light. No devices are able to connect to the internet.",
                room_number="B-205",
                status="Resolved",
                assigned_to="Campus IT Support",
                warden_remarks="IT Support replaced the faulty LAN cable in the corridor switchboard.",
                resolved_at=datetime.utcnow() - timedelta(days=1)
            ),
            Complaint(
                complaint_id="CMP-1004",
                student_id=student_profile3.id,
                category="Cleaning",
                title="Garbage bin in common room not cleared",
                description="The main garbage container in the C-floor common lounge has not been cleared for three days. It is starting to smell bad.",
                room_number="C-301",
                status="Pending"
            )
        ]
        for c in complaints:
            db.session.add(c)

        db.session.commit()

        # 4. Create Sample Attendance Sessions & Scans
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)

        # Yesterday's Session (Expired)
        yesterday_session = AttendanceSession(
            session_code="YEST-ATT-SESSION",
            created_by=warden_profile.id,
            session_date=yesterday_date,
            start_time=time(20, 0), # 8:00 PM
            expiry_time=time(21, 30), # 9:30 PM
            is_active=False
        )
        db.session.add(yesterday_session)
        db.session.commit()

        # Yesterday's Attendance Logs (Student 1 and 2 present, Student 3 absent)
        att1 = Attendance(
            session_id=yesterday_session.id,
            student_id=student_profile1.id,
            date=yesterday_date,
            time=time(20, 15),
            status="Present"
        )
        att2 = Attendance(
            session_id=yesterday_session.id,
            student_id=student_profile2.id,
            date=yesterday_date,
            time=time(20, 45),
            status="Present"
        )
        # Student 3 has no record (meaning Absent)
        db.session.add(att1)
        db.session.add(att2)

        # Today's active session
        today_session = AttendanceSession(
            session_code="TODAY-ATT-SESSION",
            created_by=warden_profile.id,
            session_date=today_date,
            start_time=time(19, 0), # 7:00 PM
            expiry_time=time(22, 0), # 10:00 PM
            is_active=True
        )
        db.session.add(today_session)
        db.session.commit()

        # Alex Mercer (Student 1) checked in today
        att_today = Attendance(
            session_id=today_session.id,
            student_id=student_profile1.id,
            date=today_date,
            time=time(19, 30),
            status="Present"
        )
        db.session.add(att_today)
        db.session.commit()

        # 5. Create Outing Requests
        # Outing 1: Returned
        out1 = OutingRequest(
            request_id="OUT-1001",
            student_id=student_profile1.id,
            destination="Phoenix Marketcity Mall",
            purpose="Buying shoes and basic toiletries.",
            outing_date=yesterday_date,
            departure_time=time(15, 0),
            expected_return_time=time(18, 0),
            actual_return_time=time(17, 45),
            status="Returned",
            warden_remarks="Granted. Make sure to return before dark."
        )
        db.session.add(out1)

        # Outing 2: Approved / Currently Outside
        out2 = OutingRequest(
            request_id="OUT-1002",
            student_id=student_profile2.id,
            destination="Local Stationary Shop",
            purpose="Purchasing chart papers and drawing instruments for engineering drawing project.",
            outing_date=today_date,
            departure_time=time(16, 0),
            expected_return_time=time(21, 0), # Return expected soon or later
            status="Outside",
            warden_remarks="Approved. Do not wander outside campus gates after 8 PM."
        )
        db.session.add(out2)

        # Outing 3: Overdue (expected return time was yesterday)
        out3 = OutingRequest(
            request_id="OUT-1003",
            student_id=student_profile3.id,
            destination="Grand Cinema Theatre",
            purpose="Watching a late night movie with friends.",
            outing_date=yesterday_date,
            departure_time=time(18, 0),
            expected_return_time=time(21, 0), # Overdue return
            status="Overdue",
            warden_remarks="Approved on the condition of strict 9 PM return. Overdue recorded.",
            rejection_reason=None
        )
        db.session.add(out3)

        # Outing 4: Pending
        out4 = OutingRequest(
            request_id="OUT-1004",
            student_id=student_profile1.id,
            destination="Railway Station",
            purpose="Going home for weekend holiday. Ticket attached.",
            outing_date=today_date + timedelta(days=2),
            departure_time=time(9, 0),
            expected_return_time=time(18, 0),
            status="Pending"
        )
        db.session.add(out4)

        db.session.commit()

        # 6. Create Notifications
        notifications = [
            Notification(
                user_id=student_user1.id,
                title="Welcome to Smart Hostel!",
                message="Your student profile has been set up successfully. You can manage your attendance, complaints, and outings here.",
                type="info",
                is_read=False
            ),
            Notification(
                user_id=student_user1.id,
                title="Complaint status updated",
                message="Your complaint CMP-1002 (Leaky bathroom tap) has been set to In Progress. Warden remarks: 'Plumber scheduled to visit A block tomorrow morning.'",
                type="complaint",
                is_read=True
            ),
            Notification(
                user_id=student_user2.id,
                title="Outing Request Approved",
                message="Your outing request OUT-1002 to Local Stationary Shop has been approved by the warden.",
                type="outing",
                is_read=False
            ),
            Notification(
                user_id=student_user3.id,
                title="Outing Status: Overdue Warning",
                message="Your outing request OUT-1003 has been flagged as OVERDUE. Please check in with the warden immediately.",
                type="outing",
                is_read=False
            )
        ]
        for n in notifications:
            db.session.add(n)

        # 7. Create Announcements
        announcements = [
            Announcement(
                warden_id=warden_profile.id,
                title="Maintenance Power Outage Notice",
                message="Please note that there will be a scheduled power outage for maintenance on Sunday (28th August) from 10:00 AM to 01:00 PM. High-power appliances should not be operated."
            ),
            Announcement(
                warden_id=warden_profile.id,
                title="Hostel Fest Outing Rules",
                message="All students must submit outing requests at least 24 hours in advance for the upcoming weekend during the college fest. On-the-spot gate passes will not be approved."
            )
        ]
        for a in announcements:
            db.session.add(a)

        db.session.commit()
        print("Database seeded successfully with test records!")

if __name__ == '__main__':
    seed_database()
