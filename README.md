# CareLog System

CareLog is a Streamlit-based web application designed for managing patient records, staff logs, and billing information in a healthcare setting. It provides role-based access for **admins**, **staff**, and **patients**, ensuring sensitive patient information is handled responsibly.

## Features

### Admin
- Register new patients and staff members
- Delete user accounts
- View all patients’ information
- Assign staff to patients
- View patient history (with sensitive log warnings)
- View billing/payment history

### Staff
- Add patient logs (symptoms, diagnosis, prescription)
- View patient history
- Sensitive logs are clearly marked for discretion

### Patient
- Add personal mood/pain logs
- View own logs
- Pay medical bills

### Security & Privacy
- Sensitive logs are marked and shown with warnings to authorized viewers
- Role-based access control prevents unauthorized data access

## Installation

1. **Clone the repository**  
`git clone https://github.com/Kenneth-kwt/FIT1056-Sem2-2025-CareLog`  
`cd FIT1056-Sem2-2025-CareLog`

2. **Set up a Python virtual environment (optional)**   
`python -m venv venv`  
`source venv/bin/activate`  (Linux/Mac)  
`venv\Scripts\activate`     (Windows CMD)  
`venv\Scripts\Activate.ps1` (Windows PowerShell)


3. **Install dependencies**  
`pip install -r requirements.txt`

4. **Run the application**  
`streamlit run main.py`

## Usage

1. Open the web interface in your browser (Streamlit will show a local URL, usually `http://localhost:8501`).  
2. Login with an existing user or register a new account.  
3. Navigate through the sidebar based on your role.  
4. Add/view logs, assign staff, or manage billing information as appropriate.

## Project Structure

FIT1056-Sem2-2025-CareLog/
│
├─ app/
│ ├─ patient.py
│ ├─ staff.py
│ ├─ admin.py
│ └─ user.py
│
├─ services/
│ ├─ patient_service.py
│ ├─ staff_service.py
│ ├─ user_service.py
│ └─ admin_service.py
│
├─ gui/
│ ├─ main_dashboard.py
│ ├─ login.py
│ ├─ config_patient.py
│ ├─ config_staff.py
│ └─ config_general.py
│
├─ testing/
│ └─unit_testing.py
│
├─ utils/
│ └─ storage.py
│
├─ data/
│ └─ careLog.json
│
├─ main.py
├─ requirements.txt
└─ README.md


## Roles & Permissions

| Role   | Permissions                                                                            |
|--------|----------------------------------------------------------------------------------------|
| Admin  | Full access: register/delete users, assign staff, view all patient history and billing |
| Staff  | Add and view patient logs for assigned patients, view patient history                  |
| Patient| Add/view own logs, pay bills                                                           |

Sensitive information is marked in logs and only visible to authorized staff/admins with a warning.

## Data Storage

- All data is stored in **`data/careLog.json`** using a JSON structure.  
- Users, patients, staff, and logs are persisted between sessions.  
- The system maintains `next_user_id` for automatic incremental ID assignment.

## Future Enhancements

- Implement authentication via hashed passwords for security  
- Add role-based dashboards with analytics  
- Integrate email notifications for billing and staff updates  
- Improve logging history visualization (charts/timelines)  

## License

This project is for academic purposes and may not be redistributed without permission.
