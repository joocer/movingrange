class segment: 
    
    def __init__(self, movingrange, segment_start, segment_end, samples = 8):
        self.mR_series = []
        self.samples = samples
        self.value_series = movingrange.value_series[segment_start:segment_end]
        for i in range(len(self.value_series) - 1):
            mR = abs(self.value_series[i] - self.value_series[i + 1])
            self.mR_series.append(mR)

    def moving_range_mean(self):
        return sum(self.mR_series[0:self.samples]) / len(self.mR_series[0:self.samples])

    def moving_range_sigma(self):
        # mean x 3.267 = mean + 3 x sigma
        mr_mean = self.moving_range_mean()
        sigma = (mr_mean * 2.267) / 3
        return sigma

    def moving_range_standard_deviation(self, number = 1):
        mr_mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        std_dev = mr_mean + (sigma * number)
        if std_dev < 0:
            std_dev = 0
        return std_dev

    # puts mRs into a bin corresponding to their displacement from the mean in standard deviations
    def moving_range_bins(self):
        bins = []
        mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        for value in range(len(self.mR_series)):
            displacement = (self.mR_series[value] - mean) / sigma
            displacement = -((0 - displacement) // 1) # math.floor the value without math
            if displacement <= 0:
                displacement = displacement - 1
            bins.append(displacement)
        return bins

    # returns an array with items of 1 (increase), 0 (stable) or -1 (reduction)
    def moving_range_direction(self):
        directions = []
        for i in range(len(self.mR_series) - 1):
            delta = self.mR_series[i + 1] - self.mR_series[i]
            if delta == 0:
                direction = 0
            else:
                direction = delta / abs(delta)
            directions.append(direction)
        return directions

    def moving_range_sigma_line(self, number = 1):
        value = self.moving_range_standard_deviation(number)
        return [value] * len(self.value_series)

    def individuals_mean(self):
        return sum(self.value_series[0:self.samples]) / len(self.value_series[0:self.samples])

    def individuals_sigma(self):
        mr_mean = self.moving_range_mean()
        sigma = (2.66 * mr_mean) / 3
        return sigma

    def individuals_standard_deviation(self, number = 1):
        mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        std_dev = mean + (sigma * number)
        return std_dev

    # puts observations into a bin corresponding to their displacement from the mean in standard deviations
    def individuals_bins(self):
        bins = []
        mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        for value in range(len(self.value_series)):
            displacement = (self.value_series[value] - mean) / sigma
            displacement = -((0 - displacement) // 1) # math.floor the value without math
            if displacement <= 0:
                displacement = displacement - 1
            bins.append(displacement)
        return bins

    # returns an array with items of 1 (increase), 0 (stable) or -1 (reduction)
    def individuals_direction(self):
        directions = []
        for i in range(len(self.value_series) - 1):
            delta = self.value_series[i + 1] - self.value_series[i]
            if delta == 0:
                direction = 0
            else:
                direction = delta / abs(delta)
            directions.append(direction)
        return directions

    def describe(self):
        mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        description = 'Segment' + '\n'
        description = description + '===========' + '\n'
        # samples
        description = description + 'Segment Mean = ' + str(mean) + '\n'
        # range min, range max 
        description = description + 'Sigma(mR) = ' + str(sigma) + '\n'
        description = description + '-3 Sigma = ' + str(self.individuals_standard_deviation(-3)) + '\n'
        description = description + '-2 Sigma = ' + str(self.individuals_standard_deviation(-2)) + '\n'
        description = description + '-1 Sigma = ' + str(self.individuals_standard_deviation(-1)) + '\n'
        description = description + ' 0 Sigma = ' + str(self.individuals_standard_deviation(0)) + '\n'
        description = description + ' 1 Sigma = ' + str(self.individuals_standard_deviation(1)) + '\n'
        description = description + ' 2 Sigma = ' + str(self.individuals_standard_deviation(2)) + '\n'
        description = description + ' 3 Sigma = ' + str(self.individuals_standard_deviation(3)) + '\n'
        print (description)

    def individuals_sigma_line(self, number = 1):
        value = self.individuals_standard_deviation(number)
        return [value] * len(self.value_series)