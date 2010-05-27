class Medication
  
  attr_reader :name, :prescriptions
  
  def initialize(name)
    @name = name
    @prescriptions = []
  end
  
  def first_prescription
    @first_prescription ||= prescriptions.sort.first
  end

  def last_prescription
    @last_prescription ||= prescriptions.sort.last
  end
  
  def <=>(other)
    if last_prescription.nil? && other.last_prescription.nil?
      name <=> other.name
    else
      compare_by_prescription_then_name(other)
    end
  end

  def compare_by_prescription_then_name(other)
    return -1 if last_prescription.nil?
    return 1 if other.last_prescription.nil?
    prescription_cmp = last_prescription <=> other.last_prescription
    return prescription_cmp if prescription_cmp != 0
    name <=> other.name
  end
  
  def days_supply
    valid_prescriptions? ? last_prescription.days_supply : read_attribute(:days_supply)
  end
  
  def possession_end_date
    most_recent_prescription.completion_date 
  end

  def possession_effective_end_date
    [possession_end_date, Date.today].min
  end

  def possession_ratio_lower_bound_date(day_count)
    possession_effective_end_date - day_count
  end

  def possession_effective_start_date(day_count)
    [possession_ratio_lower_bound_date(day_count), initial_dispense_date].max
  end

  def initial_dispense_date
    first_prescription.dispense_date
  end

  def most_recent_prescription
    prescriptions.sort_by(&:dispense_date).last
  end

  def number_of_days_prescribed(day_count)
    dates_prescribed_in_effective_range(day_count).size
  end

  def number_of_days_in_range(day_count)
    possession_effective_range(day_count).to_a.size
  end

  def prescriptions_in_range(day_count)
    prescriptions.select do |p|
      [p.dispense_date, p.completion_date].any? do |day|
        possession_effective_range(day_count).include?(day)
      end
    end
  end

  def dates_prescribed(day_count)
    prescriptions_in_range(day_count).map do |p|
      (p.dispense_date...p.dispense_date.advance(:days => p.days_supply)).to_a
    end.flatten.uniq
  end

  def dates_prescribed_in_effective_range(day_count)
    dates_prescribed(day_count).select do |d|
      possession_effective_range(day_count).include?(d)
    end
  end

  def possession(day_count)
    return 0 if number_of_days_in_range(day_count).zero?
    number_of_days_prescribed(day_count)
  end

  protected
  
  def possession_effective_range(day_count)
    possession_effective_start_date(day_count)...possession_effective_end_date
  end

end