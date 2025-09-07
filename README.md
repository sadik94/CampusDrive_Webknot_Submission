# Campus Event Management System

A complete web-based campus event management system, student registration, tracking of attendance, and feedback collection.

## Features

- **Event Management**: Add and manage different events such as Workshop, Hackathon, Fest, Seminar, and Competition.
- **Student Management**: Add and manage students.
- **Registration System**: Allow students to register for events.
- **Attendance Tracking**: Track the attendance of registered students.
- **Feedback Collection**: Collect ratings and comments.
- **Analytics Dashboard**: View event popularity and student participation reports.
- **Top Active Students**: View top active participants.

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Icons**: Font Awesome

## Prerequisites

- Python 3.7 or later
- pip (Python package manager)

## Installation & Setup

### 1. Clone or Download the Project
```bash
# If you have the zip file, unzip it
unzip CampusDrive_Webknot_Submission.zip
cd CampusDrive_Webknot_Submission
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```

### 4. Access Web Interface
Open a web browser and go to:
```
http://localhost:5001
```

## Database Schema

This application uses SQLite, which contains the following tables:

- **events**: Event data, such as title, type, date, and max participants.
- **students**: Student data, like name and email.
- **registrations**: Event registrations that link event_id and student_id.
- **attendance**: Attendance data with registration_id and status.
- **feedback**: Feedback and ratings that include registration_id, rating, and comments.

## Authentication & Portals

### Admin Portal
- Login: `GET/POST /login`
- Logout: `GET /logout`
- After login you are redirected to the dashboard `/`.
- Default admin is auto-created on startup if not present:
  - Email: `admin@campus.edu`
  - Password: `admin123`

### Student Portal
- Login: `GET/POST /student_login`
- Register: `GET/POST /student_register`
- Dashboard: `GET /student_dashboard`
- Logout: `GET /student_logout`
- Demo login uses email as the password (for demo only):
  - Email: `john@college.edu`
  - Password: `john@college.edu`

### Student Dashboard Includes
- Personal stats: total registrations, events attended, attendance rate, avg rating given
- My Events: attendance status and ratings for your events
- Upcoming Events For You: shared college-wide upcoming events
- All College Events: upcoming events across the college

Note: Upcoming events are the same for all students (college-wide). If there are no future events, the app seeds demo upcoming events automatically.

## API Endpoints

### Web Routes
- `GET /` - Dashboard (admin)
- `GET /events` - Events dashboard (admin)
- `GET/POST /login` - Admin login
- `GET /logout` - Admin logout
- `GET/POST /student_login` - Student login
- `GET/POST /student_register` - Student self-registration
- `GET /student_dashboard` - Student dashboard
- `GET /student_logout` - Student logout
- `POST /add_event` - Add new event
- `POST /add_student` - Add new student
- `POST /register` - Register a student for an event
- `POST /mark_attendance` - Mark attendance
- `POST /submit_feedback` - Provide feedback
- `POST /reset_data` - Reset all data

### API Endpoints
- `GET /api/events` - Events list (JSON)
- `GET /api/students` - Students list (JSON)
- `GET /api/reports/events` - Event popularity report (JSON)
- `GET /api/reports/students` - Student participation report (JSON)

## Generated Reports

### 1. Event Popularity Report
- Rank events in terms of number of registrations.
- Shows percentage attendance.
- Shows average rating.

### 2. Student Participation Report
- Ranks students based on the number of events attended.
- Shows registration vs. attendance rate.
- Shows average rating provided.

### 3. Top 3 Most Active Students
- Shows most active participants.
- Shows number of events visited.

## Features

### Dashboard
- Dynamic statistics.
- Quick action buttons.
- Responsive layout.
- Latest UI with Bootstrap 5.

### Event Management
- Add events of different types.
- Set maximum attendants.
- Display event popularity statistics.

### Student Management
- Add students via different emails.
- Display attendance by event.
- Display performance statistics for single student.

### Registration System
- Prevent duplicate registration.
- Display registration timestamps.
- Set limitations on event size.

### Attendance Tracking
- Display students as present or absent.
- Calculate attendance percentages.
- Generate attendance reports.

### Feedback System
- 1-5 star rating system.
- Optional comments.
- Calculate average rating.

## Configuration

The app is run on:
- **Host**: 0.0.0.0 (reachable from any IP)
- **Port**: 5001
- **Debug Mode**: Enabled for development

To modify these settings, modify the last line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Usage

1. **Add Events**: Click the "Add Event" button to add new events.
2. **Add Students**: Click the "Add Student" button to add new students.
3. **View Reports**: All reports are displayed automatically on the dashboard.
4. **Reset Data**: Use reset features to clear all data and start again.

## Sample Data

Sample data is created automatically when run for the first time:
- 5 sample students
- 5 sample events
- Random registrations and attendance
- Sample feedback with ratings
- Default admin account
- Demo upcoming college-wide events (auto-seeded if none exist)

For fixing database issues, delete `events.db` to reset the database.

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py`.
2. **Database errors**: Reset by deleting `events.db`.
3. **Module not found**: Run `pip install -r requirements.txt`.

### Reset Database
To fully reset the database:
1. Delete the `events.db` file.
2. Restart the app.
3. Sample data will be regenerated.

## File Structure

```python
CampusDrive_Webknot_Submission/
└── app.py                  # Main Flask application
└── requirements.txt        # Python dependencies
```
├── README.md             # This file
├── templates/
│   └── index.html                 # Admin dashboard
│   └── login.html                 # Admin login page
│   └── student_login.html         # Student login page
│   └── student_dashboard.html     # Student dashboard
├── static/
│   └── css/               # CSS files (if they exist)
└── events.db              # automatically generated sqlite database

## Contributing

This is for a Campus Drive submission project. For changes:
1. Fork the repository.
2. Update your changes.
3. Test thoroughly.
4. Submit your copy.

## Support

For bugs or questions:
- Check out the troubleshooting section.
- Check code comments.
- Install all dependencies.

## Success!

When you run the application, you should have:
- A clean web dashboard.
- Sample data filled in.
- Reports and analytics up and running.
- Responsive design that is compatible with all devices. 

Happy Event Managing!