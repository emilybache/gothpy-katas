import unittest
from datetime import date, timedelta

from patient import *
from medication import Medication
from prescription import Prescription

class PatientTest(unittest.TestCase):
    
    def setUp(self):
        self.patient = Patient()
        self.medication = Medication("Aspirin")
        self.patient.add_medication(self.medication)
    
    def test_possession_when_full(self):
        self.medication.add_prescription(Prescription(dispense_date=(date.today() - timedelta(days=30)), days_supply=30))
        self.medication.add_prescription(Prescription(dispense_date=(date.today() - timedelta(days=60)), days_supply=30))
        self.medication.add_prescription(Prescription(dispense_date=(date.today() - timedelta(days=90)), days_supply=30))
        self.assertEquals(90, self.patient.possession([self.medication], 90))

    def test_possession_when_partial(self):
        self.medication.add_prescription(Prescription(dispense_date=(date.today() - timedelta(days=30)), days_supply=30))
        self.medication.add_prescription(Prescription(dispense_date=(date.today() - timedelta(days=60)), days_supply=30))
        self.assertEquals(60, self.patient.possession([self.medication], 90))
    
    
if __name__ == "__main__":
    unittest.main()