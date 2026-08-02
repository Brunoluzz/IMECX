# IMECX

A Django-based web platform for managing applications, participants, tasks, and internal operations of the IMECX engineering program.

## Overview

IMECX is a web application designed to streamline the recruitment and management process of the IMECX engineering program.

The platform is organized around annual editions, each with its own application period, participant cohort, tasks, and internal activities. Prospective members can submit applications during the recruitment phase of a specific edition, while administrators can manage the entire lifecycle of that edition through a centralized dashboard.

Once accepted, participants receive an email to set their account password and gain access to a dedicated area where they can receive and submit tasks.

The system was developed with a strong focus on usability, maintainability, providing a reliable solution for participant onboarding and internal project coordination.

## Features

### Application Management

* Online application submission
* CV upload support
* Application review workflow
* Application status tracking
* Automated participant onboarding

### Participant Management

* Participant registration and activation
* Edition-based participation management
* Engineering area assignment
* Permission-controlled access

### Task Management

* Task assignment and tracking
* File submission system
* Submission status management
* Administrative feedback workflow
* Revision and approval process

### Notifications

* Internal notification system
* Read/unread notification tracking
* Automatic notification updates

### Email Integration

* Account activation emails
* Automated communication workflows
* Brevo API integration

### Administration

* Django Admin integration
* Application review tools
* Participant management
* Task and submission oversight

## Security Features

* HTTPS enforcement
* CSRF protection
* Secure session cookies
* Secure authentication cookies
* HSTS configuration
* Brute-force protection with Django Axes
* Authentication and permission-based access control
* Protected administrative functionality
* File upload validation
* Environment variable management for sensitive credentials

## Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* SQLite (Development)
* PostgreSQL-compatible deployment environments

### Services

* Brevo Email API

### Deployment

* PythonAnywhere

### Development Tools

* Git
* GitHub

## Project Structure

| Application   | Purpose                                    |
| ------------- | ------------------------------------------ |
| Applications  | Candidate applications and onboarding      |
| Tasks         | Task assignment, submissions, and feedback |
| Editions      | Edition lifecycle management               |
| Accounts      | Authentication and user management         |
| Notifications | Internal notification system               |

## Screenshots

### Homepage

<img width="1861" height="955" alt="image" src="https://github.com/user-attachments/assets/f5a03617-9d69-4b46-80d2-8d97392b8b86" />

### Application Form

<img width="1860" height="955" alt="image" src="https://github.com/user-attachments/assets/e4955982-1d31-4b83-9378-8138029de722" />

### Participant Dashboard

<img width="1861" height="954" alt="image" src="https://github.com/user-attachments/assets/50482f8d-5680-45a9-910d-fa4aa57cd8b7" />

### Task Submission

<img width="1861" height="954" alt="image" src="https://github.com/user-attachments/assets/7222caf6-8064-4bc6-9bc6-f7238b807d69" />

<img width="1862" height="955" alt="image" src="https://github.com/user-attachments/assets/ea5dea9d-cbf5-46c5-aad1-e14fb27b19b0" />

## Installation

### Clone the repository

```bash
git clone https://github.com/Brunoluzz/IMECX.git
cd IMECX
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=False

BREVO_API_KEY=your_brevo_api_key

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
```

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## Project Status

The platform is currently deployed and actively used within the IMECX project.
https://brunnohsaidegh.pythonanywhere.com

Development is ongoing, with continuous improvements focused on:

* Security
* Maintainability
* User experience
* Workflow automation

## Author

**Bruno Luz**

Software Engineering Student

GitHub: https://github.com/Brunoluzz

## License

This project is provided for educational and organizational purposes. Licensing terms may be updated in future releases.
