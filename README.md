#Campus Event Management System

A complete web-based campus event management system for student registration, attendance tracking, and feedback collection.

## Features

- **Event Management**: Add and manage events like workshops, hackathons, festivals, seminars, and competitions.
- **Student Management**: Add and manage students.
- **Registration System**: Allow students to register for events.
- **Attendance Tracking**: Monitor attendance for registered students.
- **Feedback Collection**: Collect ratings and comments.
- **Analytics Dashboard**: View event popularity and student participation reports.
- **Top Active Students**: See the most active participants.

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
Open a web browser and navigate to:
```
http://localhost:5001
```

## Database Schema

This application uses SQLite, which includes the following tables:

- **events**: Stores event data, including title, type, date, and maximum participants.
- **students**: Holds student data, such as name and email.
- **registrations**: Connects event_id and student_id for event registrations.
- **attendance**: Links registration_id and status for attendance data.
- **feedback**: Contains registration_id, rating, and comments for feedback and ratings.

## Authentication & Portals

### Admin Portal
- Login: `GET/POST /login`
- Logout: `GET /logout`
- After logging in, you will be redirected to the dashboard `/`.
- The default admin is created automatically on startup if not present:
  - Email: `admin@campus.edu
  - Password: admin123

### Student Portal
- Login: `GET/POST /student_login`
- Register: `GET/POST /student_register`
- Dashboard: `GET /student_dashboard`
- Logout: `GET /student_logout`
- Demo login uses email as the password (for demo only):
  - Email: `john@college.edu
  - Password: `john@college.edu

### Student Dashboard Includes
- Personal stats: total registrations, events attended, attendance rate, average rating given
- My Events: attendance status and ratings for your events
- Upcoming Events For You: shared college-wide upcoming events
- All College Events: upcoming events across the college

Note: Upcoming events are the same for all students (college-wide). If there are no future events, the app adds demo upcoming events automatically.

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
- `POST /add_event` - Add a new event
- `POST /add_student` - Add a new student
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
- Ranks events by the number of registrations.
- Shows percentage attendance.
- Shows average rating.

### 2. Student Participation Report
- Ranks students based on the number of events attended.
- Shows registration versus attendance rate.
- Shows average rating given.

### 3. Top 3 Most Active Students
- Displays the most active participants.
- Shows the number of events attended.

## Features

### Dashboard
- Dynamic statistics.
- Quick action buttons.
- Responsive layout.
- Latest UI with Bootstrap 5.

### Event Management
- Add events of different types.
- Set maximum attendees.
- Show event popularity statistics.

### Student Management
- Add students using different emails.
- Display attendance by event.
- Show performance statistics for individual students.

### Registration System
- Prevent duplicate registration.
- Show registration timestamps.
- Set limitations on event size.

### Attendance Tracking
- Mark students as present or absent.
- Calculate attendance percentages.
- Create attendance reports.

### Feedback System
- Uses a 1-5 star rating system.
- Allows optional comments.
- Calculates average ratings.

## Configuration

The app runs on:
- **Host**: 0.0.0.0 (accessible from any IP)
- **Port**: 5001
- **Debug Mode**: Enabled for development

To change these settings, update the last line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Usage

1. **Add Events**: Click the "Add Event" button to create new events.
2. **Add Students**: Click the "Add Student" button to include new students.
3. **View Reports**: Reports automatically display on the dashboard.
4. **Reset Data**: Use reset features to clear all data and start fresh.

## Sample Data

Sample data is created automatically when the app runs for the first time:
- 5 sample students
- 5 sample events
- Random registrations and attendance
- Sample feedback and ratings
- Default admin account
- Demo upcoming college-wide events (auto-seeded if none exist)

To fix database issues, delete `events.db` to reset the database.

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py`.
2. **Database errors**: Reset by deleting `events.db`.
3. **Module not found**: Run `pip install -r requirements.txt`.

### Reset Database
To completely reset the database:
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
└── events.db              # automatically generated SQLite database

## Contributing

This is a Campus Drive submission project. For contributions:
1. Fork the repository.
2. Implement your changes.
3. Test thoroughly.
4. Submit your copy.

## Support

For bugs or questions:
- Refer to the troubleshooting section.
- Check the code comments.
- Make sure all dependencies are installed.

## Success!

When you run the application, you should see:
- A clean web dashboard.
- Sample data filled in.
- Reports and analytics ready to use.
- A responsive design that works well on all devices.

Happy Event Managing!