require "active_support"
require "mocha"
require "patient"
require "medication"
require "prescription"

describe Medication do
  describe "#possession_end_date" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.prescriptions << Prescription.new(:dispense_date => Date.parse('12/01/2009'), :days_supply => 30)
      end
    end
  
    it "returns the sum of the most recent prescription's dispense date and its days supply" do
      medication.possession_end_date.should == Date.parse('12/31/2009')
    end
  end
  
  describe "#possession_effective_end_date" do
    context "when ending before today's date" do
      let(:medication) do
        Medication.new("Aspirin").tap do |m|
          m.prescriptions << Prescription.new(:dispense_date => 40.days.ago.to_date, :days_supply => 30)
        end
      end
  
      it "returns the end date" do
        medication.possession_effective_end_date.should == medication.possession_end_date
      end
    end
    context "when in theory it would end after today's date" do
      let(:medication) do
        Medication.new("Aspirin").tap do |m|
          m.prescriptions << Prescription.new(:dispense_date => 15.days.ago.to_date, :days_supply => 30)
        end
      end
  
      it "returns today's date" do
        medication.possession_effective_end_date.should == Date.today
      end
    end
  end
  
  describe "#initial_dispense_date" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.prescriptions << Prescription.new(:dispense_date => Date.parse('11/01/2009'), :days_supply => 30)
        m.prescriptions << Prescription.new(:dispense_date => Date.parse('11/30/2009'), :days_supply => 30)
      end
    end
  
    it "returns the first prescriptions dispense date" do
      medication.initial_dispense_date.should == Date.parse('11/01/2009')
    end
  end
  
  describe "#possession_ratio_lower_bound_date" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.stubs(:possession_effective_end_date).returns(Date.parse('12/30/2009'))
      end
    end
    it "is the difference of effective end date and the day count" do
      medication.possession_ratio_lower_bound_date(90).should == Date.parse('10/01/2009')
    end
  end
  
  describe "#possession_effective_start_date" do
    context "when the initial dispense date is after the lower bound date" do
      let(:medication) do
        Medication.new("Aspirin").tap do |m|
          m.prescriptions << Prescription.new(:dispense_date => Date.parse('12/01/2009'), :days_supply => 30)
          m.stubs(:possession_ratio_lower_bound_date).returns(Date.parse('11/30/2009'))
        end
      end
      it "returns the initial dispense date" do
        medication.possession_effective_start_date(90).should == medication.initial_dispense_date
      end
    end
    context "when the initial dispense date is before the lower bound date" do
      let(:medication) do
        Medication.new("Aspirin").tap do |m|
          m.prescriptions << Prescription.new(:dispense_date => Date.parse('12/01/2009'), :days_supply => 30)
          m.stubs(:possession_ratio_lower_bound_date).returns(Date.parse('12/30/2009'))
        end
      end
      it "returns the lower bound date" do
        medication.possession_effective_start_date(90).should == Date.parse('12/30/2009')
      end
    end
  end
  
  describe "#prescriptions_in_range" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.prescriptions << @prescription1 = Prescription.new(:dispense_date => Date.parse('08/01/2009'), :days_supply => 30)
        m.prescriptions << @prescription2 = Prescription.new(:dispense_date => Date.parse('11/01/2009'), :days_supply => 30)
        m.prescriptions << @prescription3 = Prescription.new(:dispense_date => Date.parse('12/01/2009'), :days_supply => 30)
        m.stubs(:possession_effective_end_date).returns(Date.parse('12/15/2009'))
      end
    end
    it "returns prescriptions dispensed during the effective range" do
      medication.prescriptions_in_range(90).should == [@prescription2,@prescription3]
    end
  end
  
  describe "#dates_prescribed" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.prescriptions << Prescription.new(:dispense_date => Date.parse('12/01/2009'), :days_supply => 2)
      end
    end
    it "returns the Dates a medication was prescribed for" do
      medication.dates_prescribed(2).should == [Date.parse('12/01/2009'), Date.parse('12/02/2009')]
    end
  
    context "when there is a date overlap between two prescriptions" do
      let(:medication) do
        Medication.new("Aspirin").tap do |m|
          m.prescriptions << Prescription.new(:dispense_date => Date.parse('12/01/2009'), :days_supply => 2)
          m.prescriptions << Prescription.new(:dispense_date => Date.parse('12/02/2009'), :days_supply => 2)
        end
      end
      it "removes duplicates" do
        medication.dates_prescribed(5).should == [Date.parse('12/01/2009'), Date.parse('12/02/2009'), Date.parse('12/03/2009')]
      end
    end
  end

  describe "#dates_prescribed_in_effective_range" do
      let(:medication) do
        Medication.new("Aspirin").tap do |m|
          m.prescriptions << Prescription.new(:dispense_date => 2.days.ago.to_date, :days_supply => 4)
        end
      end
    it "returns the Dates a medication was prescribed that fall in the effective possession range" do
      medication.dates_prescribed_in_effective_range(2).should == [2.days.ago.to_date, 1.day.ago.to_date]
    end
  end


  describe "#number_of_days_prescribed(90)" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.stubs(:possession_effective_range).returns(Date.parse('10/03/2009')..Date.parse('12/17/2009'))
        m.prescriptions << Prescription.new(:dispense_date => Date.parse('10/03/2009'), :days_supply => 30)
        m.prescriptions << Prescription.new(:dispense_date => Date.parse('11/17/2009'), :days_supply => 30)
      end
    end
    it "returns a count of the days that a medication was prescribed that fall in the effective possession range" do
      medication.number_of_days_prescribed(90).should == 60
    end
  end
  
  describe "#most_recent_prescription" do
    let(:medication) do
      Medication.new("Aspirin").tap do |m|
        m.prescriptions << Prescription.new(:dispense_date => 90.days.ago.to_date)
        m.prescriptions << Prescription.new(:dispense_date => 60.days.ago.to_date)
        m.prescriptions << most_recent_prescription
      end
    end
  
    let(:most_recent_prescription) { Prescription.new(:dispense_date => 30.days.ago.to_date) }
  
    it "returns the last prescription by dispense date" do
      medication.most_recent_prescription.should == most_recent_prescription
    end
  end
  describe "#possession_ratio" do
    before do
      @patient = Patient.make
      @medication = Medication.new
      @patient.medications << @medication
    end

    subject do
      @medication.possession_ratio(90)
    end

    context "received 105, 75, 45, and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 105.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 75.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 45.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago)
      end

      it { should == 1 }
    end

    context "received 105, 60, and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 105.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 60.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago)
      end

      it { should == Rational(2, 3) }
    end

    context "received 45 and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 45.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago)
      end
      it { should == 1 }
    end

    context "received 60 and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 60.days.ago)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago)
      end
      it { should == Rational(3, 4) }
    end

    context "received 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago)
      end
      it { should be_nan }
    end

    context "received never" do
      it { should be_nan }
    end

    context "received 120, 90 and 60 days ago" do
      it { should be_nan }
    end
  end

  describe "#possession" do
    before do
      @patient = Patient.new
      @medication = Medication.new("Aspirin")
      @patient.medications << @medication
    end

    subject do
      @medication.possession(90)
    end

    context "received 105, 75, 45, and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 105.days.ago.to_date.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 75.days.ago.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 45.days.ago.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago.to_date)
      end

      it { should == 90 }
    end

    context "received 105, 60, and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 105.days.ago.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 60.days.ago.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago.to_date)
      end

      it { should == 60 }
    end

    context "received 45 and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 45.days.ago.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago.to_date)
      end
      it { should == 45 }
    end

    context "received 60 and 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 60.days.ago.to_date)
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago.to_date)
      end
      it { should == 45 }
    end

    context "received 15 days ago" do
      before do
        @medication.prescriptions << Prescription.new(:days_supply => 30, :dispense_date => 15.days.ago.to_date)
      end
      it { should == 15 }
    end
  end

end