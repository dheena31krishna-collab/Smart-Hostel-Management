# Smart Hostel Management System

A complete, professional, modern, and responsive web application for college/university hostel administration. Built with **Python Flask**, **Flask-SQLAlchemy**, **MySQL** (with SQLite dynamic fallback), **Bootstrap 5**, and native browser JavaScript.

---

## 🌟 Key Features

### 🎓 Student Portal
1. **Interactive Dashboard**: View attendance rates, active outing gate passes, pending maintenance tickets, notifications, and warden notice boards.
2. **Profile Management**: Update contact details (phone, name) and change passwords with verified credentials.
3. **QR Attendance check-in**: Scan Warden-generated attendance session QR codes in real-time utilizing the browser camera, or enter the session code manually as a fallback.
4. **Complaint Ticket box**: Submit maintenance issues with categories (Electrical, Plumbing, Internet, Cleaning, Security, etc.) and track progress (Pending &rarr; In Progress &rarr; Resolved).
5. **Outing Pass Manager**: Apply for leaves, track approval states, and view returned/overdue statuses.

### 🛡️ Warden Administrative Portal
1. **Roster Metrics Dashboard**: Monitor real-time KPIs: registered students count, attendance session status (Present/Absent rates), pending tickets, active outing passes, and overdue alerts.
2. **Student Directory**: A searchable database of student records, filterable by Year and Department.
3. **QR Code Session Generator**: Start timed attendance sessions with customized start/expiry windows and display dynamic QR codes on-screen.
4. **Outing Pass Dispatcher**: Review student outing requests and approve or reject them with reasons.
5. **Campus Leave tracking**: Track students currently outside campus bounds and flag overdue returns in **Red Alert** pills. Log student returns manually with the click of a button.
6. **Notice Board Announcements**: Publish general announcements that trigger dashboard notifications across all student screens.
7. **Reports & Interactive charts**: View analytics on complaint categories (pie chart), ticket statuses (bar chart), check-out ratios (doughnut chart), and weekly attendance trends (line chart) using **Chart.js**.
8. **Structured Data Export**: Download report records (Attendance sheets, Complaint logs, and Outing pass histories) directly to **CSV files**.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask, Flask-SQLAlchemy, Werkzeug (Password hashing)
- **Database**: MySQL / SQLite (dynamic fallback)
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API, Chart.js, HTML5-QRCode scanner, QRCode.js generator)
- **Design Framework**: Bootstrap 5, Font Awesome Icons, Inter Google Font

---

## 📋 Installation and Setup

### 1. Clone or Extract the Project
Navigate to the project root directory:
```bash
cd "Smart Hostel Management System"
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and configure your credentials:
```bash
# On Windows Command Prompt:
copy .env.example .env
# On Windows PowerShell:
cp .env.example .env
# On Linux/macOS:
cp .env.example .env
```

Open `.env` and set your variables. By default, the application is pre-configured to use **SQLite** (`DB_TYPE=sqlite`) which runs out-of-the-box in a local database file `smart_hostel.db` without setting up external servers.
To switch to **MySQL**, modify `.env` as follows:
```env
DB_TYPE=mysql
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=smart_hostel_db
```
*(Make sure to create the database `smart_hostel_db` in your MySQL database server before running the app).*

---

## 🚀 Running the Application

### Step 1: Initialize and Seed the Database
Run the seed script to create all tables and populate them with structured demo records:
```bash
python seed.py
```

### Step 2: Run the Tests
Verify the database models and route controllers are operational by running the automated unit test suite:
```bash
python test_app.py
```

### Step 3: Start the Flask Web Server
```bash
python wsgi.py
```
Open your web browser and navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Demo Account Credentials

Use the following seeded accounts to immediately test the Student and Warden workflows:

### 🛡️ Warden Administrative Account
- **Email**: `warden@smarthostel.com`
- **Password**: `admin123`

### 🎓 Student Accounts
1. **Alex Mercer** (CSE - Room A-102)
   - **Email**: `student@smarthostel.com`
   - **Password**: `student123`
2. **Jane Doe** (ME - Room B-205)
   - **Email**: `jane@smarthostel.com`
   - **Password**: `student123`
3. **John Smith** (EE - Room C-301)
   - **Email**: `john@smarthostel.com`
   - **Password**: `student123`

---

## 📁 Directory Structure Summary

- `config.py`: Handles application configuration (secret key, DB URI resolver).
- `models/`: Database models package containing SQLAlchemy mappings for users, students, wardens, complaints, outings, attendance, and notifications.
- `routes/`: Blueprint controllers matching roles (auth, student portal, warden portal, async JSON API).
- `static/`: Frontend visual assets (dashboard CSS layout system, landing page styles).
- `templates/`: HTML templates containing reusable views (layout wrapper `base.html`, landing page, auth templates, error pages, student dashboard, and warden manager pages).
