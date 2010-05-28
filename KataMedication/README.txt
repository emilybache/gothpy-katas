
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

