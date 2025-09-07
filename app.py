#!/usr/bin/env python3
"""
Campus Event Management System - Flask Web Application
A web-based system for managing events, registrations, and attendance.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import sqlite3
import json
from datetime import datetime
import os
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'campus_event_management_2024'

class EventManager:
    def __init__(self, db_name='events.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Create the database tables."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                event_type TEXT NOT NULL,
                date TEXT NOT NULL,
                max_participants INTEGER,
                college_id INTEGER DEFAULT 1
            )
        ''')
        
        # Students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                college_id INTEGER DEFAULT 1
            )
        ''')
        
        # Registrations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY,
                event_id INTEGER,
                student_id INTEGER,
                registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (student_id) REFERENCES students(id),
                UNIQUE(event_id, student_id)
            )
        ''')
        
        # Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                registration_id INTEGER,
                status TEXT DEFAULT 'present',
                FOREIGN KEY (registration_id) REFERENCES registrations(id)
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                registration_id INTEGER,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                comments TEXT,
                FOREIGN KEY (registration_id) REFERENCES registrations(id)
            )
        ''')
        
        # Users table for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT DEFAULT 'admin',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def clear_all_data(self):
        """Clear all data from tables."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM feedback')
        cursor.execute('DELETE FROM attendance')
        cursor.execute('DELETE FROM registrations')
        cursor.execute('DELETE FROM students')
        cursor.execute('DELETE FROM events')
        
        try:
            cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("events", "students", "registrations", "attendance", "feedback")')
        except sqlite3.OperationalError:
            pass
        
        conn.commit()
        conn.close()
    
    def create_event(self, title, event_type, date, max_participants=None):
        """Create a new event."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (title, event_type, date, max_participants)
            VALUES (?, ?, ?, ?)
        ''', (title, event_type, date, max_participants))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return event_id
    
    def add_student(self, name, email):
        """Add a new student."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO students (name, email)
                VALUES (?, ?)
            ''', (name, email))
            
            student_id = cursor.lastrowid
            conn.commit()
            return student_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def register_student(self, event_id, student_id):
        """Register a student for an event."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO registrations (event_id, student_id)
                VALUES (?, ?)
            ''', (event_id, student_id))
            
            registration_id = cursor.lastrowid
            conn.commit()
            return registration_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def mark_attendance(self, registration_id, status='present'):
        """Mark attendance for a registration."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attendance (registration_id, status)
            VALUES (?, ?)
        ''', (registration_id, status))
        
        conn.commit()
        conn.close()
    
    def submit_feedback(self, registration_id, rating, comments=""):
        """Submit feedback for an event."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (registration_id, rating, comments)
            VALUES (?, ?, ?)
        ''', (registration_id, rating, comments))
        
        conn.commit()
        conn.close()
    
    def get_events(self):
        """Get all events."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM events ORDER BY date')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_students(self):
        """Get all students."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM students ORDER BY name')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_event_popularity_report(self):
        """Get events sorted by number of registrations."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.title, e.event_type, e.date,
                   COUNT(r.id) as registrations,
                   COUNT(a.id) as attendance,
                   ROUND(COUNT(a.id) * 100.0 / COUNT(r.id), 1) as attendance_rate,
                   AVG(f.rating) as avg_rating
            FROM events e
            LEFT JOIN registrations r ON e.id = r.event_id
            LEFT JOIN attendance a ON r.id = a.registration_id AND a.status = 'present'
            LEFT JOIN feedback f ON r.id = f.registration_id
            GROUP BY e.id
            ORDER BY registrations DESC
            LIMIT 30
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_student_participation_report(self):
        """Get students sorted by number of events attended."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.name, s.email,
                   COUNT(r.id) as total_registrations,
                   COUNT(a.id) as events_attended,
                   ROUND(COUNT(a.id) * 100.0 / COUNT(r.id), 1) as attendance_rate,
                   AVG(f.rating) as avg_rating_given
            FROM students s
            LEFT JOIN registrations r ON s.id = r.student_id
            LEFT JOIN attendance a ON r.id = a.registration_id AND a.status = 'present'
            LEFT JOIN feedback f ON r.id = f.registration_id
            GROUP BY s.id
            ORDER BY events_attended DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_top_3_active_students(self):
        """Get top 3 most active students."""
        return self.get_student_participation_report()[:3]
    
    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email, password, name, role='admin'):
        """Create a new user."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, role)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, name, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, email, password):
        """Authenticate a user."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, email, name, role FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        return user
    
    def authenticate_student(self, email, password):
        """Authenticate a student using their email as password."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # For students, we'll use a simple password system
        # In a real system, you'd have proper student passwords
        cursor.execute('''
            SELECT id, name, email FROM students 
            WHERE email = ? AND email = ?
        ''', (email, password))  # Using email as password for demo
        
        student = cursor.fetchone()
        conn.close()
        
        return student
    
    def get_student_events(self, student_id):
        """Get all events for a specific student."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.title, e.event_type, e.date, e.max_participants,
                   r.registered_at, a.status, f.rating, f.comments
            FROM events e
            JOIN registrations r ON e.id = r.event_id
            LEFT JOIN attendance a ON r.id = a.registration_id
            LEFT JOIN feedback f ON r.id = f.registration_id
            WHERE r.student_id = ?
            ORDER BY e.date DESC
        ''', (student_id,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_student_stats(self, student_id):
        """Get student statistics."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(r.id) as total_registrations,
                COUNT(a.id) as events_attended,
                ROUND(COUNT(a.id) * 100.0 / COUNT(r.id), 1) as attendance_rate,
                AVG(f.rating) as avg_rating_given
            FROM registrations r
            LEFT JOIN attendance a ON r.id = a.registration_id AND a.status = 'present'
            LEFT JOIN feedback f ON r.id = f.registration_id
            WHERE r.student_id = ?
        ''', (student_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_upcoming_events(self, student_id=None):
        """Get upcoming events."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        if student_id:
            # Get upcoming events for a specific student
            cursor.execute('''
                SELECT e.id, e.title, e.event_type, e.date, e.max_participants,
                       r.registered_at, a.status
                FROM events e
                LEFT JOIN registrations r ON e.id = r.event_id AND r.student_id = ?
                LEFT JOIN attendance a ON r.id = a.registration_id
                WHERE e.date >= ?
                ORDER BY e.date ASC
            ''', (student_id, today))
        else:
            # Get all upcoming events
            cursor.execute('''
                SELECT e.id, e.title, e.event_type, e.date, e.max_participants,
                       COUNT(r.id) as registrations
                FROM events e
                LEFT JOIN registrations r ON e.id = r.event_id
                WHERE e.date >= ?
                GROUP BY e.id
                ORDER BY e.date ASC
            ''', (today,))
        
        results = cursor.fetchall()
        conn.close()
        return results

    def get_student_registered_event_ids(self, student_id):
        """Return a set of event_ids for which the student is registered."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT event_id FROM registrations WHERE student_id = ?', (student_id,))
        rows = cursor.fetchall()
        conn.close()
        return {row[0] for row in rows}

    def has_upcoming_events(self) -> bool:
        """Return True if there are any college-wide upcoming events from today onward."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(1) FROM events WHERE date >= ?', (today,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def ensure_demo_upcoming_events(self):
        """Seed a few future-dated events for demo if none exist.

        This guarantees that every student's profile shows the same upcoming events
        because they are college-wide events.
        """
        if self.has_upcoming_events():
            return
        base_date = datetime.now()
        demo_events = [
            ("Career Fair", "Seminar", (base_date).strftime('%Y-%m-%d'), 300),
            ("AI & ML Meetup", "Workshop", (base_date.replace() + __import__('datetime').timedelta(days=7)).strftime('%Y-%m-%d'), 120),
            ("Hackathon Sprint", "Hackathon", (base_date.replace() + __import__('datetime').timedelta(days=14)).strftime('%Y-%m-%d'), 200),
            ("Startup Pitch Night", "Fest", (base_date.replace() + __import__('datetime').timedelta(days=21)).strftime('%Y-%m-%d'), 250),
            ("Coding Challenge League", "Competition", (base_date.replace() + __import__('datetime').timedelta(days=28)).strftime('%Y-%m-%d'), 150),
        ]
        for title, etype, date_str, cap in demo_events:
            try:
                self.create_event(title, etype, date_str, cap)
            except Exception:
                # Best-effort seeding; ignore individual failures
                pass

    def ensure_default_admin(self):
        """Ensure a default admin user exists for first-time login."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', ('admin@campus.edu',))
        exists = cursor.fetchone()
        if not exists:
            # Create default admin user
            password_hash = self.hash_password('admin123')
            cursor.execute('''
                INSERT INTO users (email, password_hash, name, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin@campus.edu', password_hash, 'System Administrator', 'admin'))
            conn.commit()
        conn.close()

# Initialize EventManager
em = EventManager()

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = em.authenticate_user(email, password)
        if user:
            session['user_id'] = user[0]
            session['user_email'] = user[1]
            session['user_name'] = user[2]
            session['user_role'] = user[3]
            flash(f'Welcome back, {user[2]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    """Student login page and authentication."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        student = em.authenticate_student(email, password)
        if student:
            session['student_id'] = student[0]
            session['student_name'] = student[1]
            session['student_email'] = student[2]
            session['user_type'] = 'student'
            flash(f'Welcome, {student[1]}!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    students = em.get_students()
    return render_template('student_login.html', students=students)

@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    """Student self-registration page."""
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        if not name or not email:
            flash('Name and email are required.', 'error')
            return redirect(url_for('student_register'))
        student_id = em.add_student(name, email)
        if student_id:
            flash('Registration successful! Use your email as the password to log in.', 'success')
            return redirect(url_for('student_login'))
        else:
            flash('A student with this email already exists.', 'error')
            return redirect(url_for('student_register'))
    return render_template('student_register.html')

@app.route('/student_dashboard')
def student_dashboard():
    """Student dashboard showing their events and stats."""
    if 'student_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    # Ensure shared upcoming events exist for the college (demo)
    em.ensure_demo_upcoming_events()
    student_events = em.get_student_events(student_id)
    student_stats = em.get_student_stats(student_id)
    # Show the same upcoming events for every student (college-wide)
    upcoming_events = em.get_upcoming_events()
    all_upcoming_events = upcoming_events
    registered_event_ids = em.get_student_registered_event_ids(student_id)
    
    return render_template('student_dashboard.html',
                         student_events=student_events,
                         student_stats=student_stats,
                         upcoming_events=upcoming_events,
                         all_upcoming_events=all_upcoming_events,
                         registered_event_ids=registered_event_ids)

@app.route('/student_register_event', methods=['POST'])
def student_register_event():
    """Allow a logged-in student to register for an event."""
    if 'student_id' not in session:
        flash('Please log in to register for events.', 'error')
        return redirect(url_for('student_login'))
    event_id = request.form.get('event_id')
    if not event_id:
        flash('Invalid request.', 'error')
        return redirect(url_for('student_dashboard'))
    try:
        reg_id = em.register_student(int(event_id), int(session['student_id']))
        if reg_id:
            flash('Registered successfully!', 'success')
        else:
            flash('You are already registered for this event.', 'info')
    except Exception as e:
        flash('Could not register for the event.', 'error')
    return redirect(url_for('student_dashboard'))

@app.route('/student_logout')
def student_logout():
    """Student logout and clear session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('student_login'))

@app.route('/')
@login_required
def index():
    """Home page with dashboard."""
    events = em.get_events()
    students = em.get_students()
    event_report = em.get_event_popularity_report()
    student_report = em.get_student_participation_report()
    top_students = em.get_top_3_active_students()
    
    return render_template('index.html', 
                         events=events, 
                         students=students,
                         event_report=event_report,
                         student_report=student_report,
                         top_students=top_students)

@app.route('/events')
@login_required
def events():
    """Events page - focuses on adding and viewing events."""
    events = em.get_events()
    students = em.get_students()
    event_report = em.get_event_popularity_report()
    student_report = em.get_student_participation_report()
    top_students = em.get_top_3_active_students()
    
    return render_template('index.html', 
                         events=events, 
                         students=students,
                         event_report=event_report,
                         student_report=student_report,
                         top_students=top_students)

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    """Add a new event."""
    title = request.form['title']
    event_type = request.form['event_type']
    date = request.form['date']
    max_participants = request.form.get('max_participants', None)
    
    if max_participants:
        max_participants = int(max_participants)
    
    event_id = em.create_event(title, event_type, date, max_participants)
    flash(f'Event "{title}" created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    """Add a new student."""
    name = request.form['name']
    email = request.form['email']
    
    student_id = em.add_student(name, email)
    if student_id:
        flash(f'Student "{name}" added successfully!', 'success')
    else:
        flash(f'Student with email "{email}" already exists!', 'error')
    
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
@login_required
def register_student():
    """Register a student for an event."""
    event_id = request.form['event_id']
    student_id = request.form['student_id']
    
    registration_id = em.register_student(int(event_id), int(student_id))
    if registration_id:
        flash('Student registered successfully!', 'success')
    else:
        flash('Student already registered for this event!', 'error')
    
    return redirect(url_for('index'))

@app.route('/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    """Mark attendance for a registration."""
    registration_id = request.form['registration_id']
    status = request.form['status']
    
    em.mark_attendance(int(registration_id), status)
    flash(f'Attendance marked as {status}!', 'success')
    return redirect(url_for('index'))

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    """Submit feedback for an event."""
    registration_id = request.form['registration_id']
    rating = int(request.form['rating'])
    comments = request.form.get('comments', '')
    
    em.submit_feedback(int(registration_id), rating, comments)
    flash(f'Feedback submitted: {rating}/5 stars!', 'success')
    return redirect(url_for('index'))

@app.route('/reset_data', methods=['POST'])
@login_required
def reset_data():
    """Reset all data."""
    em.clear_all_data()
    flash('All data has been reset!', 'info')
    return redirect(url_for('index'))

@app.route('/api/events')
@login_required
def api_events():
    """API endpoint for events."""
    events = em.get_events()
    return jsonify(events)

@app.route('/api/students')
@login_required
def api_students():
    """API endpoint for students."""
    students = em.get_students()
    return jsonify(students)

@app.route('/api/reports/events')
@login_required
def api_event_report():
    """API endpoint for event popularity report."""
    report = em.get_event_popularity_report()
    return jsonify(report)

@app.route('/api/reports/students')
@login_required
def api_student_report():
    """API endpoint for student participation report."""
    report = em.get_student_participation_report()
    return jsonify(report)

if __name__ == '__main__':
    # Always ensure default admin exists
    em.ensure_default_admin()

    # Create sample data on first run
    if not os.path.exists('events.db') or len(em.get_events()) == 0:
        print("Creating sample data...")
        em.clear_all_data()
        
        # Ensure admin again post-reset
        em.ensure_default_admin()
        
        # Add sample students
        students = [
            ("John Doe", "john@college.edu"),
            ("Jane Smith", "jane@college.edu"),
            ("Bob Johnson", "bob@college.edu"),
            ("Alice Brown", "alice@college.edu"),
            ("Charlie Wilson", "charlie@college.edu")
        ]
        
        print("Demo student credentials: john@college.edu / john@college.edu")
        
        student_ids = []
        for name, email in students:
            student_id = em.add_student(name, email)
            if student_id:
                student_ids.append(student_id)
        
        # Create sample events
        events = [
            ("Python Workshop", "Workshop", "2024-10-15", 50),
            ("Hackathon 2024", "Hackathon", "2024-10-20", 100),
            ("Tech Fest", "Fest", "2024-10-25", 200),
            ("AI Seminar", "Seminar", "2024-11-01", 80),
            ("Coding Competition", "Competition", "2024-11-05", 60)
        ]
        
        event_ids = []
        for title, event_type, date, max_participants in events:
            event_id = em.create_event(title, event_type, date, max_participants)
            event_ids.append(event_id)
        
        # Register students for events
        registrations = []
        for event_id in event_ids[:3]:
            for student_id in student_ids:
                reg_id = em.register_student(event_id, student_id)
                if reg_id:
                    registrations.append(reg_id)
        
        for event_id in event_ids[3:]:
            for student_id in student_ids[:3]:
                reg_id = em.register_student(event_id, student_id)
                if reg_id:
                    registrations.append(reg_id)
        
        # Mark attendance and submit feedback
        import random
        for reg_id in registrations:
            if random.random() < 0.8:
                em.mark_attendance(reg_id, 'present')
            else:
                em.mark_attendance(reg_id, 'absent')
            
            if random.random() < 0.7:
                rating = random.randint(1, 5)
                comments = ["Great event!", "Good experience", "Could be better", "Excellent!", "Not bad"][rating-1]
                em.submit_feedback(reg_id, rating, comments)
        
        print("Sample data created successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
