# Design Document - Campus Event Management System

## What This System Does
A comprehensive system to manage campus events, track student participation, and generate reports.

## Data We Track
1. **Events** - Title, type, date, max participants
2. **Students** - Name, email, college
3. **Registrations** - Which students registered for which events
4. **Attendance** - Who actually showed up
5. **Feedback** - Student ratings (1-5 stars) and comments

## Database Design

### Tables
```
events
├── id (Primary Key)
├── title
├── event_type (Workshop, Hackathon, Fest, etc.)
├── date
├── max_participants
└── college_id

students
├── id (Primary Key)
├── name
├── email (Unique)
└── college_id

registrations
├── id (Primary Key)
├── event_id (Foreign Key)
├── student_id (Foreign Key)
└── registered_at

attendance
├── id (Primary Key)
├── registration_id (Foreign Key)
└── status (present/absent)

feedback
├── id (Primary Key)
├── registration_id (Foreign Key)
├── rating (1-5)
└── comments
```

## How It Works

1. **Create Event** → Add to events table
2. **Add Student** → Add to students table
3. **Register** → Add to registrations table
4. **Mark Attendance** → Add to attendance table
5. **Submit Feedback** → Add to feedback table
6. **Generate Reports** → Query all tables

## Key Decisions Made

### 1. Technology Choice
- **Python** - Easy to understand and run
- **SQLite** - No setup required, file-based database
- **Single File** - Everything in one `simple_app.py` file

### 2. Database Design
- **Simple Tables** - Only 5 tables, easy to understand
- **Foreign Keys** - Connect related data properly
- **Unique Constraints** - Prevent duplicate registrations

### 3. Multi-College Support
- **college_id** in all tables - Simple way to separate data
- **Default college_id = 1** - Works for single college too

## Reports Generated

### 1. Event Popularity Report
- Events sorted by number of registrations
- Shows attendance percentage
- Shows average rating

### 2. Student Participation Report
- Students sorted by events attended
- Shows registration vs attendance rate
- Shows average rating given

### 3. Top 3 Most Active Students
- Shows the most active students
- Simple bonus feature

## Edge Cases Handled

1. **Duplicate Registrations** - Database constraint prevents this
2. **Missing Attendance** - Shows as not attended
3. **Missing Feedback** - Shows as no rating
4. **Invalid Ratings** - Database constraint (1-5 only)

## Why This Design is Effective

1. **Streamlined Architecture** - Everything in `simple_app.py`
2. **Clear Methods** - Each method does one thing
3. **Direct Interface** - Command line interface
4. **No Dependencies** - Only uses Python standard library
5. **Immediate Results** - Runs and shows reports right away

## Sample Data Included

The system creates realistic sample data:
- 5 students from different colleges
- 5 different types of events
- Random registrations and attendance
- Sample feedback with ratings

## How to Extend

If you want to add more features:
1. **More Event Types** - Add to the events list
2. **More Students** - Add to the students list
3. **Web Interface** - Add Flask or Django
4. **More Reports** - Add new methods
5. **Email Notifications** - Add email sending

## Files in Project

- `simple_app.py` - Main program (run this!)
- `events.db` - Database file (created automatically)
- `SIMPLE_README.md` - How to use
- `SIMPLE_DESIGN.md` - This design document

## Why This Approach Works

1. **Meets Requirements** - Does everything asked for
2. **Easy to Understand** - Clear code and structure
3. **Quick to Run** - No complex setup
4. **Educational** - Shows how databases work
5. **Practical** - Solves the real problem

This design focuses on the core functionality without overcomplicating things. It's perfect for demonstrating the concept and can be easily extended if needed.
