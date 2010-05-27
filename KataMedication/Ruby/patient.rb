class Patient

  attr_reader :medications

  def initialize()
    @medications = []
  end

  def possession(drugs, days)
      return 0 if drugs.empty?
      day_count = Date.today - days
      drugs.map { |drug| drug.dates_prescribed_in_effective_range(day_count) }.flatten.uniq.size
    end

end