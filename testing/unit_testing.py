import pytest

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.patient_service import register_patient, add_patient_log, delete_patient
from services.staff_service import view_patient_history

@pytest.fixture

def test_patient_services():
    # Register a new patient
    patient = register_patient("123", "pass123", "Test Patient", 30, "Other", "Male", "None")
    assert patient is not None
    assert patient.user_id == "123"

    # Attempt to register the same patient again (should fail)
    patient_dup = register_patient("123", "pass1234", "Test Patient2", 30, "Other", "Flu", "None")
    assert patient_dup is None  # Duplicate registration should fail

    # Add a log entry for the patient
    patient = add_patient_log("123", "Happy", 2, "Feeling better")
    assert len(patient.logs) > 0
    assert patient.logs[0]["mood"] == "Happy"

    # View patient history (should contain the log just added)
    history = view_patient_history("123")
    assert len(history["patient_logs"]) > 0
    assert history["patient_logs"][0]["mood"] == "Happy"

    # Delete the patient
    result = delete_patient("123")
    assert result is True


