# DataStraw Assessment

A Flask-based ticketing system with user registration, login, ticket creation, ticket editing, and an admin dashboard for ticket management.

## Project Overview

This project provides:
- User registration and login
- User dashboard for creating and viewing tickets
- Ticket editing and details views
- Admin login and dashboard for all tickets
- Ticket status updates by admin
- SQLite database persistence with SQLAlchemy models

## Key Features

- `User` registration and login
- Create new support tickets
- Edit existing tickets
- View ticket details
- `Admin` access to all tickets
- Admin can update ticket status (`Open`, `In Progress`, `Closed`)
- Auto-seeded admin user on first run

## Getting Started

### Prerequisites

- Python 3.9+ installed
- Recommended to use a virtual environment

### Install dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

The app starts with Uvicorn and listens on `http://0.0.0.0:5000` by default.

### Access the app

- User entry page: `http://localhost:5000/`
- User registration: `http://localhost:5000/register`
- User login: `http://localhost:5000/login`
- Admin login: `http://localhost:5000/admin/login`

## Default Admin Credentials

The app seeds an admin account automatically if none exists:

- Email: `gaurangi@gmail.com`
- Password: `adminpassword`

## Database

- SQLite database file: `instance/data.sqlite3`
- SQLAlchemy models located in `application/models.py`
- Tables: `admins`, `users`, `tickets`, `comments`

## Project Structure

- `app.py` - Flask application factory, ASGI wrapper, and startup logic
- `application/routes.py` - All request routes and view handlers
- `application/models.py` - SQLAlchemy ORM models
- `application/config.py` - Development configuration settings
- `templates/` - HTML templates for user and admin views
- `requirements.txt` - Python dependencies

## Notes

- This project uses `Flask` with `Flask-SQLAlchemy` and `uvicorn` for local development.
- The `SECRET_KEY` and password salts are stored in `application/config.py` for development only. For production, replace them with secure values and enable CSRF protection.
- The ticket status and priority fields are stored as SQLAlchemy Enum types.

## License

This repository does not include a specific license file. Add one if you want to publish or share it publicly.
