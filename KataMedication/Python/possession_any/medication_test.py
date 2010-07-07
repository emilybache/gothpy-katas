import unittest

from datetime import date, timedelta
from mockito import *

from prescription import Prescription
from medication import *

class MedicationTest(unittest.TestCase):
    
    def setUp(self):
        self.medication = Medication("Aspirin")
    
    def test_possession_end_date(self):
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 12, 1), days_supply = 30))
        self.assertEquals(date(2009, 12, 31), self.medication.possession_end_date())
        
    def test_possession_effective_end_date_when_before_today(self):
        self.medication.add_prescription(Prescription(dispense_date = date.today() - timedelta(days=40), days_supply = 30))
        self.assertEquals(date.today() - timedelta(days=10), self.medication.possession_effective_end_date())

    def test_possession_effective_end_date_when_after_today(self):
        self.medication.add_prescription(Prescription(dispense_date = date.today() - timedelta(days=15), days_supply = 30))
        self.assertEquals(date.today(), self.medication.possession_effective_end_date())
        
    def test_initial_dispense_date(self):
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 11, 1), days_supply = 30))
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 11, 30), days_supply = 30))
        self.assertEquals(date(2009, 11, 1), self.medication.initial_dispense_date())
        
    def test_possession_ratio_lower_bound_date(self):
        when(self.medication).possession_effective_end_date().thenReturn(date(2009, 12, 30))
        self.assertEquals(date(2009, 10, 1), self.medication.possession_ratio_lower_bound_date(90))
        
    def test_possession_effective_start_date_when_initial_dispense_date_after_lower_bound(self):
        when(self.medication).possession_ratio_lower_bound_date(90).thenReturn(date(2009, 11, 30))
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 12, 01), days_supply = 30))
        self.assertEquals(self.medication.initial_dispense_date(), self.medication.possession_effective_start_date(90))

    def test_possession_effective_start_date_when_initial_dispense_date_before_lower_bound(self):
        when(self.medication).possession_ratio_lower_bound_date(90).thenReturn(date(2009, 12, 30))
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 12, 01), days_supply = 30))
        self.assertEquals(date(2009, 12, 30), self.medication.possession_effective_start_date(90))

    def test_prescriptions_in_range(self):
        when(self.medication).possession_effective_end_date().thenReturn(date(2009, 12, 15))
        p1 = Prescription(dispense_date = date(2009, 8, 1),  days_supply = 30)
        p2 = Prescription(dispense_date = date(2009, 11, 1), days_supply = 30)
        p3 = Prescription(dispense_date = date(2009, 12, 1), days_supply = 30)
        self.medication.add_prescription(p1)
        self.medication.add_prescription(p2)
        self.medication.add_prescription(p3)
        self.assertEquals([p2, p3], self.medication.prescriptions_in_range(90))
        
    def test_dates_prescribed(self):
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 12, 1), days_supply = 2))
        self.assertEquals([date(2009, 12, 1), date(2009, 12, 2)], self.medication.dates_prescribed(2))
        
    def test_dates_prescribed_when_dates_overlap(self):
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 12, 1), days_supply = 2))
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 12, 2), days_supply = 2))
        self.assertEquals([date(2009, 12, 1), date(2009, 12, 2), date(2009, 12, 3)], self.medication.dates_prescribed(5))
    
    def test_dates_prescribed_in_effective_range(self):
        self.medication.add_prescription(Prescription(dispense_date = date.today() - timedelta(days=2), days_supply = 4))
        self.assertEquals([date.today() - timedelta(days=2), date.today() - timedelta(days=1)], 
                            self.medication.dates_prescribed_in_effective_range(2))
                            
    def test_number_of_days_prescribed(self):
        when(self.medication)._possession_effective_range(90).thenReturn([date(2009, 10, 3) + timedelta(days=i) for i in range(75)])
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 10, 3), days_supply = 30))
        self.medication.add_prescription(Prescription(dispense_date = date(2009, 11, 17), days_supply = 30))
        self.assertEquals(60, self.medication.number_of_days_prescribed(90))
        
        
        
if __name__ == "__main__":
    unittest.main()