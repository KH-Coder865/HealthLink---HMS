# HealthLink - Hospital Management System

This is a project that will help in swift and efficient management of Hospital Data - Doctor and Patient Appointment System and many other features.

##  Features
- **Role-based login for Admin, Doctor, and Patient.**
- **Admin dashboard displaying total doctors, patients, and appointments.**
- **Doctor dashboard showing upcoming appointments and patient lists.**
- **Patient dashboard showing available doctors, booking interface, and history.**
- **Doctor availability management for 7 days.**
- **Appointment booking, cancellation, and rescheduling logic.**
- **Treatment recording with diagnosis, notes, and prescriptions.**
- **Redis caching of common queries for speed optimization.**
- **Celery-based scheduled reminders and monthly reports.**
- **CSV export background job for patient treatment history.**



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
  -git clone https://github.com/24f3000211/hospital_management_24f3000211.git
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
- GitHub: [@24f3000211](https://github.com/24f3000211)

---