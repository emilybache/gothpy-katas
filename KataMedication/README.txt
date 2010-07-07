
This is a little exercise in understanding what simple, well-tested code looks like. The exercise is available in both Ruby and Python.

(note: to run the python version you need to have python 2.6, and also mockito installed (http://code.google.com/p/mockito/wiki/MockitoForPython))
(note: to run the ruby version you need to install rails)

This is a description of the code:
- given these domain classes: Patient, Medication, Prescription
- a Prescription has a dispense date and a days supply
- a Medication has a name
- Patients have many Medications and Medications have many Prescriptions
- there is a method "possession" on Patient which returns how many of the last n days s/he has taken any of a list of Medications

Take a look at the code. Does the code match the description? Spend 30 minutes looking for discrepancies and fixing those you find.

Now you have looked at the code for a bit, answer these questions:
	- is the code well tested?
	- is the code simple?

Re-write the code from scratch.

How does your re-write compare with the original code? How long did it take you?

What have you learnt from this exercise about simple, well-tested code?

med_possession_ratio(name, days)
  Returns the medication possession ratio for the drug provided,
  given the supplied number of days to search back from the last
  medical claim. It is used with an operator to find the patient population that matches.

  For example, a patient with a 30 day prescription for Lipitor
  has claims indicating they filled the prescription 15, 60, and 105
  days ago would have a medication possession ratio of 0.67
  med_possession_ratio("Lipitor", 30) < 0.67


possession(names, days_back)
    Returns a number of days that a patient has been taking a medication, given the supplied time frame
    names - one or more names that can be either a drug name, a drug category or a drug ingredient
    days_back - determines how far back to go in checking prescription dispense dates using days.ago syntax.
    possession("oxycodone", 365.days.ago) > 84
    possession("oxycodone", hydrocodone", 90.days.ago) < 36