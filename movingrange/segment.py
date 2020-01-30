class segment: 
    
    def __init__(self, movingrange, segment_start, segment_end):
        self.mR_series = []
        self.value_series = movingrange.value_series[segment_start:segment_end]
        for i in range(len(self.value_series) - 1):
            mR = abs(self.value_series[i] - self.value_series[i + 1])
            self.mR_series.append(mR)

    def moving_range_mean(self):
        return sum(self.mR_series) / len(self.mR_series)
        
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

    def moving_range_limits(self):
        upper = self.moving_range_standard_deviation(3)
        lower = self.moving_range_standard_deviation(-3)
        return  lower, upper

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

    # returns an array with items of 1 or -1 depending on if the value is more or less than the mean
    def moving_range_sides(self):
        sides = []
        mean = self.moving_range_mean()
        for i in range(len(self.mR_series)):
            displacement = self.mR_series[i] - mean
            side = displacement / abs(displacement)
            sides.append(side)
        return sides

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

    def moving_range_describe(self):
        mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        limits = self.moving_range_limits()
        description = 'Moving Range' + '\n'
        description = description + '============' + '\n'
        description = description + 'Upper control limit = ' + str(limits[1]) + '\n'
        description = description + 'Moving Range mean = ' + str(mean) + '\n'
        description = description + 'Lower control limit = ' + str(limits[0]) + '\n'
        description = description + 'Sigma(mR) = ' + str(sigma) + '\n'
        description = description + '-3 Sigma = ' + str(self.moving_range_standard_deviation(-3)) + '\n'
        description = description + '-2 Sigma = ' + str(self.moving_range_standard_deviation(-2)) + '\n'
        description = description + '-1 Sigma = ' + str(self.moving_range_standard_deviation(-1)) + '\n'
        description = description + ' 0 Sigma = ' + str(self.moving_range_standard_deviation(0)) + '\n'
        description = description + ' 1 Sigma = ' + str(self.moving_range_standard_deviation(1)) + '\n'
        description = description + ' 2 Sigma = ' + str(self.moving_range_standard_deviation(2)) + '\n'
        description = description + ' 3 Sigma = ' + str(self.moving_range_standard_deviation(3)) + '\n'
        print (description)

    def individuals_mean(self):
        return sum(self.value_series) / len(self.value_series)

    def individuals_sigma(self):
        mr_mean = self.moving_range_mean()
        sigma = (2.66 * mr_mean) / 3
        return sigma

    def individuals_standard_deviation(self, number = 1):
        mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        std_dev = mean + (sigma * number)
        return std_dev

    def individuals_limits(self):
        upper = self.individuals_standard_deviation(3)
        lower = self.individuals_standard_deviation(-3)
        return  lower, upper

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

    # returns an array with items of 1 or -1 depending on if the value is more or less than the mean
    def individuals_sides(self):
        sides = []
        mean = self.individuals_mean()
        for i in range(len(self.value_series)):
            displacement = self.value_series[i] - mean
            if displacement == 0:
                side = 0
            else:
                side = displacement / abs(displacement)
            sides.append(side)
        return sides

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

    def individuals_describe(self):
        mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        limits = self.individuals_limits()
        description = 'Individuals' + '\n'
        description = description + '===========' + '\n'
        description = description + 'Upper control limit = ' + str(limits[1]) + '\n'
        description = description + 'Moving Range mean = ' + str(mean) + '\n'
        description = description + 'Lower control limit = ' + str(limits[0]) + '\n'
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