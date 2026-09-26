# 🎓 Student Management System

A Django-based **Student Management System** for managing students, academic results, attendance, subjects, class information, student finances, users, and role-based access.

The project is built around Django's **Model-View-Template (MVT)** architecture and uses class-based generic views, a custom user model, Django authentication, ModelForms, Django Groups and Permissions, SQLite, and Crispy Forms with Tailwind.

Unlike a simple student CRUD application, this project includes several academic-management workflows such as:

* Student registration and profile management
* Student class and roll assignment
* Subject management
* Academic result / CGPA management
* Attendance management
* Total class tracking
* Student financial records
* User and role management
* Group permission management
* Search and filtering
* Role-specific student result and attendance views

---

# ✨ Features

## 👤 User & Role Management

The system uses a custom Django `User` model with the following application roles:

* Student
* Teacher
* Admin
* Manager
* Accounts

The custom user model extends Django's `AbstractUser` and adds a `role` field. Staff status is automatically determined from the user's role, and users are assigned to a Django Group matching their role.

---

## 👨‍🎓 Student Management

Staff users can:

* Create students
* View students
* Search students
* Filter students by class
* View individual student details
* Update student information
* Assign a class
* Generate a roll number
* Delete student records

Student creation and class assignment are implemented using Django ModelForms and class-based generic views.

---

## 🏫 Class & Roll Assignment

When a student is assigned to a class, the system automatically generates a roll number based on:

```text
Current Year + Class + Student Count
```

For example, the logic follows this structure:

```text
2026 + 5 + 3
      ↓
202653
```

The actual implementation calculates the current year, counts students in the selected class, and generates the roll number before saving the `StudentProfile`.

---

## 📚 Subject Management

Staff can manage subjects through the system.

Available operations include:

* Add subject
* View subjects
* Update subject
* Delete subject

Subjects are represented by a dedicated `Subject` model with a unique subject name.

---

## 📊 Student Results

The system provides academic result management.

A result contains:

* Student
* Roll
* Subject
* Semester
* Year
* CGPA

The system prevents duplicate results for the same student, year, semester, and subject through both form validation and a database-level unique constraint.

### Result Management

Staff can:

* Add results
* Update results
* Delete results
* Search results
* Filter by year
* Filter by semester
* Filter by class

Students can view their own results.

Staff users receive a different result template from students.

---

## 📅 Attendance Management

The system includes student attendance tracking.

Attendance statuses are:

```text
Present
Absent
Late
```

Each attendance record stores:

* Student
* Roll
* Subject
* Status
* Date

The database prevents duplicate attendance records for the same student, subject, and date.

### Attendance Workflow

Staff can select:

1. A class
2. A subject
3. Students from that class
4. Attendance status for each student

The system then creates or updates attendance records for the current date.

Students can view their own attendance records, while staff can access the broader attendance list.

---

## 📈 Total Class Tracking

The project contains a `TotalClassCount` model for storing the total number of classes conducted.

Each record contains:

* User
* Class
* Subject
* Total class count
* Creation timestamp

The custom `User` model also exposes a `total_classes_count` property that calculates the total classes associated with the user using Django's `Sum()` aggregation.

---

## 💰 Student Finance

The system also tracks student financial information.

Each financial record contains:

* Student
* Roll
* Semester
* Year
* Total amount
* Payment status
* Creation date

Payment status can be:

```text
Paid
Unpaid
```

The database prevents duplicate financial records for the same student, year, and semester.

Staff can:

* Add financial records
* View financial records
* Update financial records

Students can view their own financial information.

---

# 🔐 Authentication & Authorization

The project uses Django's built-in authentication system together with a custom `User` model.

The custom model is configured as:

```python
AUTH_USER_MODEL = 'accounts.User'
```

The project also configures:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

---

# 👥 Role System

The application defines these roles:

| Role     | Purpose                                     |
| -------- | ------------------------------------------- |
| Student  | Access personal academic information        |
| Teacher  | Staff-level account for academic operations |
| Admin    | Administrative account                      |
| Manager  | Management-level account                    |
| Accounts | Finance/account-related staff               |

The custom `User.save()` method automatically sets `is_staff` for:

```text
Admin
Manager
Accounts
Teacher
```

while regular students are not marked as staff. It also synchronizes the user's Django Group with their selected role.

---

# 🛡️ Staff Access

The project defines a reusable:

```python
StaffRequiredMixin
```

which is used throughout many student-management views.

Views using this mixin include operations for:

* User management
* Student management
* Student results
* Attendance management
* Finance management
* Subject management
* Group permission management

> **Implementation note:** the current `StaffRequiredMixin` checks authentication and staff status with an `and` condition. As written, an authenticated non-staff user can pass that particular condition. If the intention is strict staff-only protection, this condition should be reviewed before production deployment.

---

# 👤 User Management

Staff users can manage application users.

Available functionality includes:

* User listing
* Search
* User creation
* User details
* User update
* User deletion

The user list supports searching by:

* First name
* Last name
* Email
* Role

Superusers are excluded from the normal user-management queryset.

---

# 🔎 Student Search & Filtering

The student list supports searching by:

* First name
* Last name
* Email
* Class
* Roll number

It also supports filtering by class.

The view uses Django's `Q` objects to combine multiple search conditions.

Example:

```text
/accounts/students/?search=alex
```

Class filtering is handled through:

```text
/accounts/students/?class=5
```

---

# 🔎 Result Search & Filtering

Student results support multiple filters.

### Year

```text
?year=2026
```

### Semester

```text
?semester=1
```

### Class

```text
?class=5
```

### Search

```text
?search=Alex
```

The result view combines these filters with Django ORM queries and orders the results by year and semester.

---

# 📊 Result Grouping

The result list does more than simply display database records.

The view groups results using:

```text
Year
  └── Semester
        ├── Subject Result
        ├── Subject Result
        └── Subject Result
```

The grouped structure is passed to the template as:

```python
grouped_results
```

This allows the frontend to organize academic results by year and semester.

---

# 🧩 Database Models

The core data model is located in:

```text
accounts/models.py
```

The main models are:

```text
User
Subject
StudentProfile
StudentResult
StudentAttendance
TotalClassCount
StudentFinance
```

---

# 🔗 Database Relationships

The main relationships can be represented as:

```text
                         User
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
       StudentProfile   Results      Attendance
             │            │             │
             │            └──────┬──────┘
             │                   │
             │                Subject
             │
             └─────────────┐
                           │
                           ▼
                     StudentFinance
```

There is also:

```text
User
 │
 └── TotalClassCount
```

where a user can have multiple total-class records.

---

# 🧱 Model Details

## User

```python
class User(AbstractUser):
    first_name
    last_name
    email
    role
```

The email field is unique.

---

## StudentProfile

```python
class StudentProfile(models.Model):
    user
    class_list
    roll
```

The class choices currently range from:

```text
0 → 10
```

and the profile is connected to the user through a one-to-one relationship.

---

## Subject

```python
class Subject(models.Model):
    subject
```

The subject name is unique.

---

## StudentResult

```python
class StudentResult(models.Model):
    user
    roll
    subject
    semester
    year
    cgpa
```

Unique constraint:

```text
user + year + semester + subject
```

---

## StudentAttendance

```python
class StudentAttendance(models.Model):
    user
    roll
    subject
    status
    created_at
```

Unique constraint:

```text
roll + subject + created_at
```

---

## TotalClassCount

```python
class TotalClassCount(models.Model):
    user
    at_class
    subject
    total_class_count
    created_at
```

---

## StudentFinance

```python
class StudentFinance(models.Model):
    user
    roll
    semester
    year
    total
    paid
    created_at
```

Unique constraint:

```text
user + year + semester
```

---

# 📝 Forms

The application uses Django ModelForms extensively.

The forms include:

```text
UserCreateForm
StudentCreateForm
StudentClassAssignForm
UpdateAccountForm
StudentUpdateClassAssignForm
StudentAddResult
StudentAddAttandance
StudentResultUpdate
SubjectAssign
StudentFinacial
GroupPermissionForm
```

There is also a custom:

```text
AttendanceSelectionForm
```

for selecting a class and subject before entering attendance.

---

# 🛡️ Result Validation

Before saving a result, `StudentAddResult` checks whether the same student already has a result for the selected:

```text
Year
Semester
Subject
```

If a duplicate exists, the form raises a validation error:

```text
This subject already exists for this student in this semester and year.
```

The database also contains a corresponding unique constraint, providing a second level of protection.

---

# 📅 Attendance Logic

Attendance is handled as a class-level workflow.

```text
Staff
 │
 ▼
Select Class
 │
 ▼
Select Subject
 │
 ▼
Load Students
 │
 ▼
Choose Status
 │
 ├── Present
 ├── Absent
 └── Late
 │
 ▼
Save Attendance
```

The implementation uses:

```python
update_or_create()
```

with:

```text
student
subject
current date
```

This allows the same attendance operation to update an existing record instead of creating a duplicate.

---

# 💰 Finance Logic

Financial records are protected against duplicates at the database level.

The combination:

```text
User
Year
Semester
```

must be unique.

The creation view also catches `IntegrityError` and converts the database error into a user-friendly form error.

---

# 🔑 Group & Permission Management

The project includes a dedicated permission-management form.

Staff can select:

```text
Group
+
Permissions
```

and assign the selected permissions to that Django Group.

The form uses Django's:

```python
Group
Permission
FilteredSelectMultiple
```

components.

The permission-management view updates the group using:

```python
group.permissions.set(permissions)
```

---

# 🌐 URL Structure

The main project routes are:

| URL             | Purpose                      |
| --------------- | ---------------------------- |
| `/`             | Home                         |
| `/feature/`     | Feature page                 |
| `/login/`       | Login                        |
| `/logout/`      | Logout                       |
| `/admin/`       | Django Admin                 |
| `/accounts/...` | User and academic management |

---

# 👤 Account URLs

The account application uses the namespace:

```text
accounts
```

Main routes include:

```text
/accounts/users/register/
/accounts/users/
/accounts/users/user_detail/<id>/
/accounts/users/user_update/<id>/
/accounts/users/user_delete/<id>/
```

Student routes include:

```text
/accounts/students/
/accounts/students/create/
/accounts/students/create/class/<id>/
/accounts/students/student_detail/<id>/
/accounts/students/student_update_user/<id>/
/accounts/students/student_update_class/<id>/
/accounts/students/student_delete/<id>/
```

---

# 📊 Result URLs

The project provides:

```text
/accounts/students/student_add_result/
/accounts/students/student_result_list/
/accounts/students/student_result_update/<id>/
/accounts/students/student_result_delete/<id>/
```

---

# 📅 Attendance URLs

Attendance functionality is exposed through:

```text
/accounts/students/student_add_attendance/
/accounts/students/student_attendance_list/
/accounts/students/student_attendance_update/<id>/
```

---

# 📚 Subject URLs

Subject management includes:

```text
/accounts/stuffs/subject/assign_subject/
/accounts/stuffs/subject/subject_list/
```

Additional subject update/delete routes are defined in the account URL configuration.

---

# 🏗️ Project Structure

```text
Student-Management-System/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── mixins.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── student_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   └── ...
│
├── templates/
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md
```

The repository's root structure contains the `accounts`, `static`, `student_management`, and `templates` directories along with `manage.py` and `requirements.txt`.

---

# 🛠️ Technology Stack

| Technology                      | Usage                        |
| ------------------------------- | ---------------------------- |
| **Python**                      | Backend programming language |
| **Django 6.0.2**                | Web framework                |
| **SQLite**                      | Database                     |
| **Django ORM**                  | Database interaction         |
| **Django Authentication**       | Login/session authentication |
| **Django Groups & Permissions** | Role/permission management   |
| **Django Generic Views**        | Application logic            |
| **Django ModelForms**           | Form handling and validation |
| **Crispy Forms 2.5**            | Form rendering               |
| **Crispy Tailwind 1.0.3**       | Tailwind form templates      |
| **HTML/CSS/JavaScript**         | Frontend                     |

The dependency versions are taken directly from the repository's `requirements.txt`.

---

# 🎨 Frontend

The project uses Django's server-rendered template system rather than a separate React/Vue frontend.

The Django settings configure the project-level template directory:

```python
DIRS = [BASE_DIR / 'templates']
```

and enable application template discovery through:

```python
APP_DIRS = True
```

Static assets are configured through:

```python
STATIC_URL = 'static/'
STATIC_ROOT = 'static_root'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
```

---

# 🎨 Crispy Forms + Tailwind

The project uses:

```text
django-crispy-forms
crispy-tailwind
```

and configures:

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
```

This allows Django forms to be rendered using the Tailwind template pack.

---

# 🗄️ Database

The project currently uses SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

SQLite makes the project easy to run locally without installing a separate database server.

---

# 🔄 Application Architecture

A typical request follows:

```text
Browser
   │
   ▼
Django URL
   │
   ▼
Class-Based View
   │
   ▼
ModelForm
   │
   ▼
Django ORM
   │
   ▼
SQLite
   │
   ▼
Template
   │
   ▼
Browser
```

For example, adding a student follows:

```text
Staff
  │
  ▼
Student Create Page
  │
  ▼
StudentCreateForm
  │
  ▼
User Model
  │
  ├── role = Student
  ├── username generated
  └── password generated
  │
  ▼
StudentClassAssignForm
  │
  ▼
StudentProfile
  │
  ├── class
  └── roll
```

The actual implementation creates the student user first and then redirects to the class-assignment workflow.

---

# 🔄 Academic Workflow

The academic flow can be represented as:

```text
                    Student
                       │
              ┌────────┼─────────┐
              │        │         │
              ▼        ▼         ▼
            Class    Results   Attendance
              │        │         │
              │        │         │
              └────────┼─────────┘
                       │
                       ▼
                   Subjects
```

A student can have:

* One student profile
* Multiple result records
* Multiple attendance records
* Multiple financial records
* Multiple total-class records

The model relationships and constraints are defined in `accounts/models.py`.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/OrpanAp/Student-Management-System.git
cd Student-Management-System
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The repository currently specifies:

```text
Django==6.0.2
django-crispy-forms==2.5
crispy-tailwind==1.0.3
asgiref==3.11.1
sqlparse==0.5.5
tzdata==2025.3
```

and also contains `pi==0.1.2` in the requirements file.

---

## 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

For an existing clone containing migrations, `migrate` is the important command for creating/updating the database.

---

## 5. Create a superuser

```bash
python manage.py createsuperuser
```

Follow Django's prompts.

The superuser is automatically assigned the `Admin` role by the custom `User.save()` implementation.

---

## 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

The project's root URL serves the home page, while authentication and account-management functionality are exposed through their configured routes.

---

# 👨‍💻 Typical Usage

## Administrator / Staff

A staff user can generally work through the following flow:

```text
Login
  │
  ▼
User Management
  │
  ├── Create Users
  ├── Manage Students
  └── Manage Roles
          │
          ▼
       Students
          │
          ├── Assign Class
          ├── Manage Results
          ├── Manage Attendance
          ├── Manage Subjects
          └── Manage Finance
```

The available operations are implemented through Django class-based views under the `accounts` application.

---

# 👨‍🎓 Student

A student account is restricted to personal academic information in the result, attendance, and finance querysets.

For example, the result view applies:

```python
queryset = queryset.filter(
    user=self.request.user
)
```

when the logged-in user's role is `Student`.

The same pattern is used for attendance and finance records.

Therefore:

```text
Student
   │
   ├── Own Results
   ├── Own Attendance
   └── Own Finance
```

rather than displaying all students' records.

---

# 🔐 Security Considerations

The project uses several Django security mechanisms:

* Django session authentication
* CSRF middleware
* Django password hashing
* Django password validators
* Authentication mixins
* Role-based user information
* Staff-oriented management views
* Database-level unique constraints

The settings enable Django's standard security, session, CSRF, authentication, message, and X-Frame-Options middleware.

---

# ⚠️ Production Configuration

The current project is configured for development.

The settings currently contain:

```python
DEBUG = True
```

and a secret key directly inside `settings.py`. `ALLOWED_HOSTS` is also currently empty.

Before production deployment, these should be changed.

Recommended improvements:

* Move `SECRET_KEY` to environment variables
* Set `DEBUG = False`
* Configure `ALLOWED_HOSTS`
* Use a production database such as PostgreSQL
* Configure static files properly
* Enable HTTPS
* Review authentication and authorization logic
* Add automated tests
* Review staff permission enforcement
* Protect sensitive student and financial data

---

# ⚠️ Important Implementation Notes

### Role default

The `User` model defines role choices with capitalized values:

```text
Student
Teacher
Admin
Manager
Accounts
```

but the model's default is currently:

```python
default='student'
```

which does not exactly match the declared choices. This should be normalized before treating the project as production-ready.

### Staff access mixin

The current `StaffRequiredMixin` contains:

```python
if not request.user.is_authenticated and not request.user.is_staff:
```

Because the conditions are joined with `and`, an authenticated non-staff user does not satisfy the redirect condition. This means the mixin should be reviewed if its purpose is to strictly enforce staff-only access.

These are **implementation observations**, not claims that the application is unusable.

---

# 📚 Django Concepts Demonstrated

This project provides practical examples of:

### Django Fundamentals

* Django project/app structure
* Settings
* URL routing
* Views
* Templates
* Static files
* Migrations
* Django ORM

### Authentication

* Custom user model
* `AbstractUser`
* Login
* Logout
* Sessions
* Password validation
* User roles

### Database

* One-to-one relationships
* Foreign keys
* Unique constraints
* QuerySets
* `select_related()`
* `prefetch_related()`
* Aggregation with `Sum()`
* `update_or_create()`

### Views

* `ListView`
* `DetailView`
* `CreateView`
* `UpdateView`
* `DeleteView`
* `TemplateView`
* `FormView`
* Authentication mixins
* Custom access mixins

### Forms

* `ModelForm`
* `UserCreationForm`
* Custom validation
* `ModelChoiceField`
* `ModelMultipleChoiceField`
* Dynamic form querysets

### Authorization

* Django Groups
* Django Permissions
* Role-based behavior
* Staff access control

---

# 📁 Core Files

| File                             | Responsibility                                          |
| -------------------------------- | ------------------------------------------------------- |
| `manage.py`                      | Django command-line entry point                         |
| `student_management/settings.py` | Project configuration                                   |
| `student_management/urls.py`     | Root URL routing                                        |
| `student_management/views.py`    | Home and login-related views                            |
| `accounts/models.py`             | Users, students, results, attendance, finance, subjects |
| `accounts/forms.py`              | Application forms and validation                        |
| `accounts/views.py`              | Main application logic                                  |
| `accounts/urls.py`               | Account/student/academic routes                         |
| `accounts/mixins.py`             | Custom access-control mixin                             |
| `accounts/admin.py`              | Django admin configuration                              |
| `templates/`                     | HTML templates                                          |
| `static/`                        | CSS, JavaScript and other static assets                 |
| `requirements.txt`               | Python dependencies                                     |

The repository structure and Django entry points confirm this separation between the project configuration and the `accounts` application.

---

# 🧠 Project Architecture Summary

```text
Student Management System
│
├── Authentication
│      └── Custom User
│
├── User Management
│      ├── Students
│      ├── Teachers
│      ├── Admins
│      ├── Managers
│      └── Accounts
│
├── Academic Management
│      ├── Classes
│      ├── Subjects
│      ├── Results
│      └── CGPA
│
├── Attendance
│      ├── Present
│      ├── Absent
│      └── Late
│
├── Finance
│      ├── Total
│      └── Paid / Unpaid
│
└── Permissions
       ├── Groups
       └── Permissions
```

---

# 🎯 Project Purpose

The primary purpose of this project is to provide a practical Django implementation for managing student and academic information.

It goes beyond basic student CRUD by connecting:

```text
Users
  ↓
Student Profiles
  ↓
Classes
  ↓
Subjects
  ↓
Results
  ↓
Attendance
  ↓
Finance
```

while using Django's authentication, ORM, ModelForms, generic class-based views, Groups, and Permissions to organize the application's functionality.

---

# 🚧 Potential Future Improvements

Possible future improvements include:

* 📊 Admin dashboard with statistics
* 📈 Attendance percentage calculation
* 🎓 Automatic GPA/CGPA calculation
* 🧮 Grade calculation from marks
* 📅 Academic calendar
* 📝 Assignment/exam management
* 📧 Email notifications
* 📱 REST API
* ⚛️ React frontend
* 🔍 Advanced reporting
* 📄 PDF result generation
* 📊 Financial reports
* 🔐 More granular permission enforcement
* 🧪 Automated unit and integration tests
* 🐘 PostgreSQL support
* 🌐 Production deployment configuration

These are potential extensions and are **not currently presented as implemented features**.

---

# 📄 License

No explicit license file is currently visible in the repository.

If this project is intended for public reuse, an appropriate open-source license should be added.

---

# 👨‍💻 Author

**OrpanAp**

GitHub: [OrpanAp](https://github.com/OrpanAp)

---

## ⭐ Summary

**Student Management System** is a Django 6 application that combines student administration with academic and financial management.

Its core workflow is:

```text
                  ┌───────────────┐
                  │     Users     │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │    Students   │
                  └───────┬───────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
         Subjects      Results      Attendance
            │             │             │
            │             │             │
            └─────────────┼─────────────┘
                          │
                          ▼
                       Finance
```

The project demonstrates how Django can be used to build a multi-role academic management system with relational data, validation, access control, CRUD operations, filtering, and server-rendered interfaces.
