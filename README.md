# HealthLink - Hospital Management System

This is a project that will help in swift and efficient management of Hospital Data - Doctor and Patient Appointment System and many other features.

---

## 🔧 Assignment-Aligned Features

This project demonstrates a **secure, scalable REST API** with authentication, role-based access control, and a minimal frontend UI to interact with backend APIs, aligned with the Backend Developer Intern assignment.

---

### Backend 

#### Authentication & Authorization
- User registration and login APIs with **secure password hashing**
- **JWT-based authentication** for protected routes
- **Role-Based Access Control (RBAC)** implemented using:
  - `admin`
  - `doctor`
  - `patient`  
  (maps directly to *admin vs user* role requirement)

#### REST API Design
- Versioned REST APIs using `/api/v1/*`
- Proper HTTP status codes and centralized error handling
- Input validation and request sanitization
- Modular, scalable project structure for future feature expansion

#### CRUD Operations 
- **Appointment** entity with full CRUD support:
  - Create appointment
  - Retrieve appointment(s)
  - Update (reschedule) appointment
  - Delete (cancel) appointment
- **Treatment records** as an additional managed resource:
  - Diagnosis
  - Notes
  - Prescriptions

#### Database & Schema Design
- Relational database schema designed using **SQLAlchemy ORM**
- Clear entity relationships between users, appointments, and treatments
- Architecture easily portable to **PostgreSQL / MySQL** for production environments

#### API Documentation
- REST APIs designed to be easily testable via **Postman**
- Endpoint structure compatible with **Swagger / OpenAPI** documentation

---

### Frontend

- Frontend UI built to **interact with backend APIs** using Vue.js
- User workflows implemented:
  - User registration and login
  - Role-based dashboards (Admin / Doctor / Patient)
  - Protected routes requiring JWT authentication
- CRUD interactions with backend APIs:
  - Appointment creation, update, and deletion
- Clear display of API success and error messages

---

### Security & Scalability Considerations

- Secure JWT token handling for authenticated requests
- Password hashing and role validation enforced at API level
- Redis caching implemented for frequently accessed queries
- Asynchronous background processing using **Celery** for:
  - Scheduled reminders
  - Monthly reports
  - CSV exports
- Scalable architecture designed around:
  - Stateless REST APIs
  - Caching layer
  - Background workers
  - Future Docker-based deployment

---

### Advanced Enhancements

- Redis caching for performance optimization
- Celery-based background jobs
- CSV export functionality for reporting
- Scheduling logic for reminders and analytics

---

## 🚀 Technical Stack

This project utilizes the following technologies:

- **Backend**: Flask (lightweight Python framework), Celery, Redis, WSL2
- **Database**: SQLAlchemy (ORM for database management)(SQLite3 DB)
- **Frontend**: Bootstrap CSS (responsive PWA design), Vue.JS, JavaScript
- **Version Control**: Git & GitHub


### 🛠 Tools:
- **IDE**: Visual Studio Code
- **Backend**: WSL2

### 📦 Package Management:
- **Pip**: Install dependencies from `req.txt`

---

## 💻 Setup Instructions

#### 1. **Install Python**
To run this project, you’ll need to have *Python 3.7+* installed on your system.

-n, make sure to check the box to *Add Python to PATH*.

- **Windows**: [Download Python](https://www.python.org/downloads/) and check *Add Python to PATH*.
- **macOS**: `brew install python`
- **Linux**: `sudo apt install python3`
    

  To confirm Python is installed, run this in your terminal:
  ```bash
  python --version
  ```
  
#### 2. **Clone the repository**
```bash
  -git clone https://github.com/KH-Coder865/HealthLink---HMS.git
```
#### 3. **Set Up a Virtual Environment**

A *virtual environment* is recommended to keep project dependencies isolated.

1. *Create a Virtual Environment:*

   In your project’s root directory, run the following command to create the virtual environment:
   
   ```bash
   python -m venv venv
   ```
   

   This will create a venv directory where the isolated Python environment will reside.

2. *Activate the Virtual Environment:*

   - *Windows:*
    ``` bash
     venv\Scripts\activate
    ```
     
   - *macOS/Linux:*
    ``` bash
     source venv/bin/activate
    ```
     
   After activation, your terminal prompt should change to something like:
   ``` bash
   (venv) $
   ```
   
#### 4. **Install Dependencies**

```bash
    -cd backend
    -pip install -r req.txt
```

#### 5. **Run the Project**

```bash
    -cd backend
    -python app.py
```

```bash
    -npm install
    -npm run dev
```

The app should now be running.

---

## ! Issue Log

- Backend Celery Tasks Not working properly
- Frontend/Backend ports clash while using WSL2
- Caching was previously on resources, not working properly then moved to the services. Worked
- Ensuring proper RBAC
- Handling the props and states of a vue SFC

---

## 👤 Author

**Kaushik Harsha** 
- GitHub: [@KH-Coder865](https://github.com/KH-Coder865)

---
