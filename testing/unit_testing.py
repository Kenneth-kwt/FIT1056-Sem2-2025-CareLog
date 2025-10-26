import pytest

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.patient_service import register_patient, add_patient_log, delete_patient
from services.staff_service import register_staff,delete_staff,add_staff_log,view_patient_history, register_staff, add_staff_log, find_patient_logs
from services.admin_service import assign_staff_to_patient
from services.user_service import delete_user, login, add_user

@pytest.fixture
def test_add_user():
    user = add_user("123", "pass123", "patient");
    assert user is not None
    assert user.user_id == "123"

    user_dup = add_user("123", "pass123", "admin");
    assert user_dup is None  # Duplicate user ID should not be allowed

    user_invalid_role = add_user("1234", "pass1234", "worker");
    assert user_invalid_role is None  # Invalid role should not be allowed

def test_delete_user():
    # Delete the user
    user = add_user("123", "pass123", "patient");
    result = delete_user("123")
    assert result is True

    result_nonexistent = delete_user("999")
    assert result_nonexistent is False  # Non-existent user deletion should return False

def test_register_patient():
    # Register a new patient
    patient = register_patient("123", "pass123", "Test Patient", 30, "Male", "Flu", "None")
    assert patient is not None
    assert patient.user_id == "123"

    # Attempt to register the same patient again (should fail)
    patient_dup = register_patient("123", "pass1234", "Test Patient2", 30, "Other", "Flu", "None")
    assert patient_dup is None  # Duplicate registration should fail

    # Assign Test staff to patient
    staff = register_staff("345","staffpassword", "Test speciality","Test Staff")
    assigned = assign_staff_to_patient("123","345")

    user_invalid = login("123", "wrongpass")
    assert user_invalid is None  # Invalid credentials should return None

    user_nonexistent = login("999", "nopass")
    assert user_nonexistent is None  # Non-existent user should return None

def test_add_patient_log():
    # Add a log entry for the patient
    patient = add_patient_log("123", "Happy", 2, "Feeling better")
    #Add_patient_log :user_id, mood=None, pain_level=None, notes=None, sensitive_information=False
    assert len(patient.logs) > 0
    assert patient.logs[0]["mood"] == "Happy"


def test_register_staff():
    # Register a new staff member
    staff = register_staff("200", "staffpass", "General", "Dr. Smith")
    assert staff is not None
    assert staff.user_id == "200"

def test_assign_staff_to_patient():
    # Assign staff to patient
    result = assign_staff_to_patient("123", "200")
    assert result is True

def test_view_patient_history():
    patient = register_patient("456", "pass123", "Test Patient", 30, "Other", "Male", "None")
    add_patient_log("456", "Happy", 2, "Feeling better")
    # View patient history (should contain the log just added)
    bool, history = view_patient_history("456", "200")
    assert bool is False
    
    bool, history = view_patient_history("123", "200")
    assert bool is True
    assert len(history["patient_logs"]) > 0
    assert history["patient_logs"][0]["mood"] == "Happy"

def test_add_staff_log():
    # Register a new patient
    patient = register_patient("555", "pass123", "Test Patient", 30, "Other", "Male", "None")
    # Add a log entry for the staff member regarding a patient
    staff = add_staff_log(
        staff_id="200",
        patient_id="555",
        patient_symptoms="Cough, Fever",
        diagnosis="Flu",
        prescription="Rest, Hydration",
        notes="Patient should recover in a week."
    )
    assert staff is None

    staff = add_staff_log(
        staff_id="200",
        patient_id="123",
        patient_symptoms="Cough",
        diagnosis="Flu",
        prescription="Rest, Hydration",
        notes="Patient should recover in a week."
    )
    assert staff is not None
    assert len(staff.logs) > 0
    assert staff.logs[0]["diagnosis"] == "Flu"
