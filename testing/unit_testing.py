import pytest

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.patient_service import register_patient, add_patient_log, delete_patient
from services.staff_service import register_staff,delete_staff,add_staff_log,view_patient_history
from services.admin_service import assign_staff_to_patient

@pytest.fixture

def test_patient_services():
    # Register a new patient
    patient = register_patient("123", "pass123", "Test Patient", 30, "Other", "Male", "None")
    assert patient is not None
    assert patient.user_id == "123"

    # Attempt to register the same patient again (should fail)
    patient_dup = register_patient("123", "pass1234", "Test Patient2", 30, "Other", "Flu", "None")
    assert patient_dup is None  # Duplicate registration should fail

    # Assign Test staff to patient
    staff = register_staff("345","staffpassword", "Test speciality","Test Staff")
    assigned = assign_staff_to_patient("123","345")

    # Add a log entry for the patient
    patient = add_patient_log("123", "Happy", 2, "Feeling better")
    #Add_patient_log :user_id, mood=None, pain_level=None, notes=None, sensitive_information=False
    assert len(patient.logs) > 0
    assert patient.logs[0]["mood"] == "Happy"

    # View patient history (should contain the log just added)
    history = view_patient_history("123","345")
    assert len(history["patient_logs"]) > 0
    assert history["patient_logs"][0]["mood"] == "Happy"

    # Delete the patient
    result = delete_patient("123")
    assert result is True

def test_staff_services():
    #Register a new staff
    staff = register_staff("345","staffpassword", "Test speciality","Test Staff")
    assert staff is not None
    assert staff.user_id == "345"

    #Attempt to register same staff again(should fail)
    staff_dup = register_staff("345","diff pass","Test speciality" ,"Test Staff 2")
    #Duplicate registration should fail
    assert staff_dup is None 

    patient = register_patient("123", "pass123", "Test Patient", 30,"Male", "Other", "None")
    #register_patient:user_id, password, name, age, gender, ailment, culture_and_religion
    assigned = assign_staff_to_patient("123","345")
    patient = add_patient_log("123", "Happy", 2, "Feeling better")
    #Add_patient_log :user_id, mood=None, pain_level=None, notes=None, sensitive_information=False
    added_log = add_staff_log("123","Projectile Diarrhea",)
    #staff_id,patient_id= None,patient_symptoms =None,patient_log_timestamp=None,
    # diagnosis = None,prescription = None,notes = None,patient_logs = None


    







