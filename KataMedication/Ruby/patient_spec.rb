require "active_support"
require "patient"
require "medication"
require "prescription"

describe Patient do
  describe "#possession" do
      before do
      @patient = Patient.new
      @medication = Medication.new(:name => "Codeine")
    end

    context "full possession" do
      before do
        @medication.prescriptions << Prescription.new(:dispense_date => 30.days.ago.to_date, :days_supply => 30)
        @medication.prescriptions << Prescription.new(:dispense_date => 60.days.ago.to_date, :days_supply => 30)
        @medication.prescriptions << Prescription.new(:dispense_date => 90.days.ago.to_date, :days_supply => 30)
        @patient.medications << @medication
      end

      it "returns all the days" do
        subject.possession([@medication], 90).should == 90
      end
    end

    context "partial possession" do
      before do
        @medication.prescriptions << Prescription.new(:dispense_date => 30.days.ago.to_date, :days_supply => 30)
        @medication.prescriptions << Prescription.new(:dispense_date => 60.days.ago.to_date, :days_supply => 30)
        @patient.medications << @medication
      end

      it "returns two thirds of the days" do
        subject.possession([@medication], 90).should == 60
      end
    end

  end
end
