
import sys, datetime
from ConfigParser import ConfigParser


class DateRange(set):
    def __init__(self, start_date, length):
        for i in range(length):
            self.add(start_date + datetime.timedelta(days=i))

class Patient:
    def __init__(self, fileName):
        self.dataParser = ConfigParser()
        self.dataParser.read([ fileName ])

    @staticmethod
    def parseDate(dateStr):
        return datetime.datetime.strptime(dateStr, "%Y-%m-%d").date()

    def getDatesTakingMedication(self, requestedMedicationNames):
        medicationDates = set()
        for medName in self.findMedications(requestedMedicationNames):
            for prescriptionDates in self.getPrescriptionDates(medName):
                medicationDates.update(prescriptionDates)
        return medicationDates

    def getPrescriptionDates(self, medName):
        dates = []
        for prescDateStr in self.dataParser.options(medName):
            days = int(self.dataParser.get(medName, prescDateStr))
            prescDate = self.parseDate(prescDateStr)
            dates.append(DateRange(prescDate, days))
        return dates

    def findMedications(self, requestedMedicationNames):
        return filter(lambda name: name in requestedMedicationNames, self.dataParser.sections())
        

if __name__ == "__main__":
    patient = Patient("patient.txt")
    
    requestedMedicationNames = sys.argv[1].split(",")
    medicationDates = patient.getDatesTakingMedication(requestedMedicationNames)

    days = int(sys.argv[2])
    requestedDates = DateRange(datetime.date.today() - datetime.timedelta(days=days), days) 

    pos = len(requestedDates.intersection(medicationDates))
    print >> sys.stderr, "Possession of the medication in the last", days, "days = ", pos
