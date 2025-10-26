import json
import sys
sys.path.append("app")
from staff import StaffUser
import datetime as dt

class StaffManager: 
    def __init__(self, data_path = "data/careLog.json"):
        self.data_path =data_path
        self.staff = []
        self.patient_records = []
        self.next_staff_id = 1