# 🎓 Student Management System

A simple **Django‑based Student Management System** that provides basic student record management functionality including user authentication and CRUD operations — designed to improve understanding of Django backend and web development.

---

## 🛠️ Features

- 🔐 User authentication (Admin / Users)  
- 👨‍🎓 Manage student records (Create, Read, Update, Delete)  
- 🏫 Structured student database using Django models  
- 🌐 Built with Django views and templates  
- 🧠 Demonstrates fundamental full‑stack web app architecture

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | 🐍 Python + Django |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (default Django) |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x  
- pip  
- Virtual environment (recommended)

---

### 💾 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/OrpanAp/Student‑Management‑System.git
cd Student‑Management‑System
```
---

2. **Create & activate a virtual environment**

---🌟Linux / macOS
```bash
python3 ‑m venv venv
source venv/bin/activate
```

---🌟Windows PowerShell
```bash
venv\Scripts\Activate.ps1
```

---

3. **Install dependencies**
```bash
pip install ‑r requirements.txt
```

---

4. **Apply database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

5. **Run the Django development server**
```bash
python manage.py runserver
```

---

6. **Access the app in browser**
- 📖Open → http://127.0.0.1:8000/

---

```text

🗂 Project Structure

Student‑Management‑System/
├── accounts/                  # Authentication & user/login logic
├── student_management/        # Main app for student CRUD functionality
├── templates/                 # HTML template files
├── static/                    # Static assets (CSS/JS/images)
├── manage.py                  # Django entry point
├── requirements.txt           # Dependencies
└── README.md                 # Project documentation
```
