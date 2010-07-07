
import sys, datetime
from ConfigParser import ConfigParser


class DateRange(set):
    def __init__(self, start_date, length):
        for i in range(length):
            self.add(start_date + datetime.timedelta(days=i))

def parseDate(dateStr):
    return datetime.datetime.strptime(prescDateStr, "%Y-%m-%d").date()

def getDatesTakingMedication(patientDataParser, requestedMedicationNames):
    medicationDates = set()
    for medName in patientDataParser.sections():
        if medName in requestedMedicationNames:
            for prescDateStr in patientDataParser.options(medName):
                days = int(patientDataParser.get(medName, prescDateStr))
                prescDate = parseDate(prescDateStr)
                medicationDates.update(DateRange(prescDate, days))
    return medicationDates

if __name__ == "__main__":
    patientDataParser = ConfigParser()
    patientDataParser.read([ "patient.txt" ])
    
    requestedMedicationNames = sys.argv[1].split(",") 
    medicationDates = getDatesTakingMedication(patientDataParser, requestedMedicationNames)

    days = int(sys.argv[2])
    requestedDates = DateRange(datetime.date.today() - datetime.timedelta(days=days), days) 

    pos = len(requestedDates.intersection(medicationDates))
    print >> sys.stderr, "Possession of the medication in the last", days, "days = ", pos
