# Sahaaya AI – Student Mental Wellness & Academic Risk Prediction System

## Project Overview

Sahaaya AI is a full-stack web application developed to monitor student wellbeing, predict academic risk, and improve communication between students, faculty, and administrators. The system combines academic performance, wellbeing information, AI-generated insights, and an intelligent chatbot to provide early intervention and support.

---

## Technologies Used

### Frontend
- Angular
- TypeScript
- HTML
- CSS
- Bootstrap
- Font Awesome

### Backend
- Django
- Django REST Framework (DRF)
- JWT Authentication

### Database
- SQLite

### AI Integration
- Groq API
- Llama 3.3 70B Versatile

---

## Python Version

```
Python 3.13
```

---

## Angular Version

```
Angular 20
```


---

## Backend Setup


### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Environment File

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
```

### 6. Run Backend

```bash
python manage.py runserver
```

Backend URL

```
http://127.0.0.1:8000/
```

---

## Frontend Setup

Navigate to frontend folder

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run Angular

```bash
ng serve
```

Frontend URL

```
http://localhost:4200/
```

---

## Features

### Student Module

- Student Registration
- Student Login (JWT Authentication)
- Dashboard
- Academic Performance
- Wellbeing Form
- AI Risk Prediction
- Student Profile
- AI Assistant Chatbot
- Logout

---

### Faculty Module

- Faculty Registration
- Faculty Login
- Dashboard
- Student List
- Student Academic Update
- Student Insights
- Counselling Messages
- Logout

---

### Admin Module

- Admin Login
- Dashboard
- Manage Students
- Manage Faculties
- AI Alerts
- Delete Students
- Delete Faculties
- Logout

---

### AI Features

- Academic Risk Prediction
- AI Recommendations
- Mental Wellbeing Analysis
- AI Assistant Chatbot using Groq Llama 3.3

---

---

## Default Login/register Credentials

### Admin example

```
Username: admin
Password: password

```
### Student example

```
Username: name
Register number: ST202206
email:example@gmail.com
Password: password

```


## API Authentication

JWT Authentication is used for secure access.

Login returns:

- Access Token
- Refresh Token

The frontend stores the access token in Local Storage and sends it using:

```
Authorization: Bearer <access_token>
```


## Future Enhancements

- Email Notifications
- Attendance API Integration
- PDF Report Generation
- AI-Based Emotion Detection
- Mobile Application
- Cloud Deployment