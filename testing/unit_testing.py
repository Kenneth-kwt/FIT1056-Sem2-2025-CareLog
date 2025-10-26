import pytest

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.patient_service import register_patient, add_patient_log, delete_patient
from services.staff_service import view_patient_history, register_staff, add_staff_log, find_patient_logs
from services.admin_service import assign_staff_to_patient
from services.user_service import delete_user, login

@pytest.fixture
# def test_patient_services():
def test_register_patient():
    # Register a new patient
    patient = register_patient("123", "pass123", "Test Patient", 30, "Other", "Male", "None")
    assert patient is not None
    assert patient.user_id == "123"

    # Attempt to register the same patient again (should fail)
    patient_dup = register_patient("123", "pass1234", "Test Patient2", 30, "Other", "Flu", "None")
    assert patient_dup is None  # Duplicate registration should fail

def test_login():
    user = login("123", "pass123")
    assert user is not None
    assert user.user_id == "123"

def test_add_patient_log():
    # Add a log entry for the patient
    patient = add_patient_log("123", "Happy", 2, "Feeling better")
    assert len(patient.logs) > 0
    assert patient.logs[0]["mood"] == "Happy"


def test_delete_user():
    # Delete the patient
    result = delete_user("123")
    assert result is True

def test_register_staff():
    # Register a new staff member
    staff = register_staff("200", "staffpass", "General", "Dr. Smith")
    assert staff is not None
    assert staff.user_id == "200"

def test_assign_staff_to_patient():
    # Register a new staff member
    staff = register_staff("200", "staffpass", "General", "Dr. Smith")

    # Register a new patient
    patient = register_patient("300", "patientpass", "Patient X", 40, "Female", "Diabetes", "None")

    # Assign staff to patient
    result = assign_staff_to_patient("300", "200")
    assert result is True

def test_view_patient_history():
    patient = register_patient("456", "pass123", "Test Patient", 30, "Other", "Male", "None")
    add_patient_log("456", "Happy", 2, "Feeling better")
    # View patient history (should contain the log just added)
    bool, history = view_patient_history("456", "200")
    assert bool is False
    
    assign_staff_to_patient("456", "200")
    bool, history = view_patient_history("456", "200")
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

    assign_staff_to_patient("555", "200")
    staff = add_staff_log(
        staff_id="200",
        patient_id="555",
        patient_symptoms="Cough, Fever",
        diagnosis="Flu",
        prescription="Rest, Hydration",
        notes="Patient should recover in a week."
    )
    assert staff is not None
    assert len(staff.logs) > 0
    assert staff.logs[0]["diagnosis"] == "Flu"
