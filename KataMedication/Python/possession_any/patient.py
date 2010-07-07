
class Patient:
    
    def __init__(self, medications = []):
        self.medications = medications
    
    def add_medication(self, medication):
        self.medications.append(medication)
    
    def possession(self, medications, days):
        if not medications:
            return 0
        dates = set()
        for medication in medications:
            dates = dates.union(set(medication.dates_prescribed_in_effective_range(days)))
        return len(dates)
