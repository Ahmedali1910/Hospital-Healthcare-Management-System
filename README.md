# Hospital Healthcare Management System

A backend REST API for managing healthcare operations, patients, doctors, appointments, medical consultations, follow-ups, surgeries, and departments.

The system is built using **Python, Django, Django REST Framework, SQLite, JWT Authentication, and Django Filter**.

---

## Project Overview

### What does this project do?

The **Hospital Healthcare Management System** provides a centralized backend API for managing the main healthcare operations of a hospital.

The system connects patients, doctors, administrators, appointments, medical, surgeries, follow-ups records in one system.

The main workflow is:

```text
User
 ↓
Patient / Doctor
 ↓
Appointment
 ↓
Medical Consultation
 ↓
Follow-up / Surgery
```

### Problem It Solves

Managing healthcare can be complicated for both patients and healthcare providers when there is no centralized system to organize the entire process.

For patients, keeping track of doctors, appointments, consultations, follow-ups, surgeries, and medical records can become difficult, especially when this information is handled through different systems or manually.

Doctors also need an organized way to manage their appointments, access their assigned patients, and maintain their patients' medical records throughout the treatment process. At the same time, hospital administrators need better control over doctors, patients, departments, and other healthcare operations.

The **Hospital Healthcare Management System** provides a centralized platform that connects patients, doctors, and administrators in one system. It simplifies the healthcare workflow by allowing each user to manage the resources they need according to their role and permissions.

This helps:

* **Patients** easily manage their profiles, find doctors, book appointments, and access their medical records.
* **Doctors** manage their appointments, assigned patients, consultations, follow-ups, and surgeries in an organized way.
* **Administrators** manage the hospital's doctors, patients, departments, appointments, and overall healthcare operations.

The goal is to make healthcare management **more organized, accessible, and easier to manage for everyone involved**.


### Intended Users

The system is designed for three main types of users:

* **Patients** — manage their profile, choose doctors, create appointments, and view their medical, surgery, follow-up records.
* **Doctors** — manage their profile, appointments, assigned patients, and medical, surgery, follow-up records.
* **Administrators** — manage doctors, patients, departments, appointments, and other system resources.

---

# Main Features

## Authentication & Authorization

The system provides:

* Patient registration.
* Doctor registration.
* JWT authentication.
* Access tokens.
* Refresh tokens.
* Role-based authorization.
* Protected API endpoints.
* Custom Django REST Framework permissions.

### Supported Roles

```text
Admin
Doctor
Patient
```

---

## Patient Management

Patients can:

* Register an account.
* Log in using JWT.
* View their profile.
* Update their profile.
* View approved doctors.
* Filter doctors by department.
* Choose a doctor.
* Create appointments.
* View their own appointments.
* Update their appointments.
* Cancel their appointments.
* View their medical consultations.
* View follow-ups.
* View surgeries.

Patients cannot:

* Create medical consultations.
* Modify other patients' information.
* Modify medical records.
* Create appointments for other patients.

---

## Doctor Management

Doctors can:

* Register through the API.
* Wait for administrator approval.
* View their profile.
* Update their profile.
* View their appointments.
* Update their appointments.
* Cancel their appointments.
* View their assigned patients.
* Create medical consultations.
* Update medical consultations.
* Manage follow-ups.
* Manage surgeries.

Only **approved doctors** are available for patients to choose.

---

## Administrator Management

Administrators can manage the main resources of the system, including:

* Doctors.
* Patients.
* Departments.
* Appointments.
* Medical consultations.
* Follow-ups.
* Surgeries.

Administrators can also approve or reject doctor registrations.

---

# Filtering

The project uses **Django Filter** with Django REST Framework.

The API supports filtering resources based on supported fields.

For example, patients can filter doctors by department to find doctors belonging to a specific department.

The filtering backend is configured using:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}
```

---

# Hospital Workflow

## Patient Workflow

```text
Patient Registration
        ↓
Login
        ↓
View Approved Doctors
        ↓
Filter by Department
        ↓
Choose a doctor for ongoing care
        ↓ 
Choose a doctor for examination 
        ↓
Create Appointment
        ↓
Doctor Handles Appointment
        ↓
Medical Consultation
        ↓
Follow-up / Surgery
        ↓
Patient Views Medical Records
```

## Doctor Workflow

```text
Doctor Registration
        ↓
Pending Approval
        ↓
Admin Approval
        ↓
Doctor Becomes Available
        ↓
Patients Can Choose Doctor
        ↓
Doctor Views Appointments
        ↓
Medical Consultation
        ↓
Follow-up / Surgery
```

## Admin Workflow

```text
Admin Login
        ↓
Manage Doctors
        ↓
Approve / Reject Doctors
        ↓
Manage Patients
        ↓
Manage Departments
        ↓
Manage Appointments
        ↓
Manage Medical Records
```

---

# Technologies Used

The project is built using:

* **Python**
* **Django**
* **Django REST Framework (DRF)**
* **SQLite**
* **Django Filter**
* **Django REST Framework Simple JWT**
* **Git & GitHub**
* **Apidog** for API testing and documentation
* **Lucidchart** for database/ERD design

---

# Project Structure

A simplified project structure:

```text
Backend-Workshop-Final-Projects/
│
├── System/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── user/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
│
├── hospital/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
│
├── manage.py
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
```

---

# Database Design

The system contains the following main entities:

* User
* Patient
* Doctor
* Department
* Appointment
* Medical Consultation
* Follow Up
* Surgery

## Main Relationships

### User → Patient

Each Patient is associated with one User.

```text
User 1 ───── 1 Patient
```

### User → Doctor

Each Doctor is associated with one User.

```text
User 1 ───── 1 Doctor
```

### Department → Doctor

A Department can have multiple Doctors.

```text
Department 1 ───── N Doctor
```

### Doctor → Patient

A Patient can choose a main Doctor.

```text
Doctor 1 ───── N Patient
```

The relationship is optional because a patient may register before choosing a doctor.

### Patient → Appointment

A Patient can have multiple appointments.

```text
Patient 1 ───── N Appointment
```

### Doctor → Appointment

A Doctor can have multiple appointments.

```text
Doctor 1 ───── N Appointment
```

### Appointment → Medical Consultation

An appointment can have zero or one medical consultation.

```text
Appointment 1 ───── 0..1 Medical Consultation
```

### Medical Consultation → Follow Up

A Medical Consultation can have multiple follow-ups.

```text
Medical Consultation 1 ───── N Follow Up
```

### Medical Consultation → Surgery

A Medical Consultation can have multiple surgeries.

```text
Medical Consultation 1 ───── N Surgery
```

---

# ERD / Database Design

The database design was created using **Lucidchart**.

The final ERD represents the relationships between users, patients, doctors, departments, appointments, and medical records.

### ERD Link

```text
https://lucid.app/lucidchart/217df6f3-fd5a-4dd7-a50c-47fd736a2e14/edit?invitationId=inv_b23a6804-909b-4830-8ceb-4b0d6a07ddcd&page=0_0#
```

### Database Design Notes

The database avoids unnecessary duplicated relationships.

For example, a `Medical Consultation` is connected to an `Appointment`.

The `Appointment` already contains:

* Patient
* Doctor
* Date
* Time
* Status

Therefore, the `Medical Consultation` does not need separate `patient` and `doctor` foreign keys.

The medical record structure is:

```text
Appointment
      ↓
Medical Consultation
      ↓
 ┌────┴────┐
 ↓         ↓
Follow Up  Surgery
```

This keeps the database normalized and reduces redundant data.

---

# API Documentation

The APIs were tested and documented using **Apidog**.

### Apidog Documentation

```text
https://p2ecdyxrpp.apidog.io
```

The Apidog documentation contains:

* API endpoints.
* HTTP methods.
* Authentication requirements.
* Request bodies.
* Query parameters.
* Response examples.
* Error responses.

---

# Installation

## 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/Backend-Committee/Backend-Workshop-Final-Projects.git
```

Navigate to the project directory:

```bash
cd Backend-Workshop-Final-Projects
```

---

## 2. Create a Virtual Environment

 

### Create a Python virtual environment

```bash
uv init
uv venv
```

---

## 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

If the project is managed using `uv`, the project environment can be used to run Django commands:

```bash
uv run manage.py <command>
```

---

# Environment Variables

The project uses environment variables for configuration and sensitive values.

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

### Required Variables

| Variable     | Description                           |
| ------------ | ------------------------------------- |
| `SECRET_KEY` | Django secret key                     |
| `DEBUG`      | Enables or disables Django debug mode |

### Important

Do not add real secret values to the README or GitHub repository.

The `.env` file should be included in `.gitignore`:

```gitignore
.env
```

---

# Database Setup

The project currently uses **SQLite** for local development.

The database is configured in Django as:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

The database file is:

```text
db.sqlite3
```

No external database server is required to run the project locally.

---

# Database Migration

Run the following command to create migrations:

```bash
python manage.py makemigrations
```

Then apply the migrations:

```bash
python manage.py migrate
```

If using `uv`:

```bash
uv run manage.py makemigrations
```

```bash
uv run manage.py migrate
```

---

# Create an Administrator

Create a Django superuser:

```bash
uv run manage.py createsuperuser
```

Follow the prompts to provide the administrator credentials.

---

# Run the Project Locally

Start the Django development server:

```bash
python manage.py runserver
```

Or using `uv`:

```bash
uv run manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

---

# JWT Authentication

The project uses **Django REST Framework Simple JWT** for authentication.

JWT authentication is configured as:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

### Authentication Flow

```text
Login
   ↓
Access Token + Refresh Token
   ↓
Send Access Token
   ↓
Access Protected Endpoints
```

The access token should be sent in the request header:

```http
Authorization: Bearer <access_token>
```

When the access token expires, the refresh token can be used to obtain a new access token.

---

# API Endpoints

The project provides endpoints for authentication and hospital resources.

## Authentication

```text
/user/register/patients/
/user/register/doctors/
/user/login/
/user/token/refresh/
```

## Hospital Resources

```text
/hospital/patients/
/hospital/patients/me/
/hospital/doctors/
/hospital/doctors/me/
/hospital/doctors/pending_doctors/
/hospital/appointments/
/hospital/appointments/cancel/
/hospital/appointments/complete/
/hospital/follow-ups/
/hospital/surgeries/
/hospital/medical-consultation/
/hospital/department/
/hospital/doctors-admin/
```

The exact HTTP methods, request bodies, query parameters, permissions, and responses are available in the Apidog documentation.

---

# Permissions & Access Control

The project uses custom Django REST Framework permissions to control access according to the user's role.

Examples include:

* `IsAdminRole`
* `IsDoctorRole` 
* `IsDoctor`
* `IsPatientRole`
* `CanViewPatientRecords`
* `CanViewUpdateRecords`

Permissions are applied according to the API action and the authenticated user's role.

### Access Overview

```text
Admin
 └── Full system management

Doctor
 ├── Own profile
 ├── Own appointments
 ├── Assigned patients
 └── Medical records

Patient
 ├── Own profile
 ├── Own appointments
 └── Own medical records
```

Object-level permissions are also used to prevent users from accessing resources belonging to other users.

---

# API Request Flow

The project follows the standard Django REST Framework architecture:

```text
Client
   ↓
URL / Router
   ↓
ViewSet
   ↓
Authentication
   ↓
Permissions
   ↓
Serializer
   ↓
Model
   ↓
SQLite
   ↓
Response
```

For example, when a patient creates an appointment:

```text
Patient
   ↓
POST /hospital/appointment/
   ↓
JWT Authentication
   ↓
Patient Permission
   ↓
AppointmentSerializer
   ↓
Appointment Model
   ↓
SQLite
   ↓
Response
```

The patient's identity is obtained from the authenticated user instead of requiring the frontend to submit the patient's ID manually.

---

# Security

The project includes several security mechanisms:

* JWT authentication.
* Role-based authorization.
* Object-level permissions.
* Protected endpoints.
* Password hashing through Django.
* Environment variables for sensitive configuration.
* Separation between authenticated and public endpoints.

Sensitive information such as passwords, secret keys, and credentials should never be committed to the repository.

---

# Future Improvements

Possible future improvements include:

* Email verification.
* Forgot password functionality.
* Reset password functionality.
* Change password endpoint.
* Doctor availability schedules.
* Appointment notifications.
* More advanced appointment scheduling.
* Automated API tests.
* Pagination improvements.
* Docker support.
* Production deployment.
* Migration from SQLite to PostgreSQL for production use.
* More advanced reporting and analytics.

---

# License

This project is intended for educational and development purposes.
