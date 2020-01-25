class movingrange: 
    # https://en.wikipedia.org/wiki/Shewhart_individuals_control_chart
    
    # some code comments taken from: 
    # https://www.staceybarr.com/measure-up/build-xmr-chart-kpi/
    
    period_series = []
    value_series = []
    mR_series = []

    def load_from_pandas(self, df, period_column, value_column):
        import pandas
        self.load_from_arrays(df[period_column].tolist(), df[value_column].tolist())

    def load_from_arrays(self, period_series, value_series):
        self.period_series = period_series
        self.value_series = value_series
        self.mR_series = []
        for i in range(len(value_series) - 1):
            mR = abs(value_series[i] - value_series[i + 1])
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

    # puts observations into a bin corresponding to their distance from the mean in standard deviations
    def moving_range_bins(self):
        bins = []
        sigma = self.moving_range_sigma()
        mean = self.moving_range_mean()
        for value in range(len(self.mR_series)):
            distance = (self.mR_series[value] - mean) / sigma
            distance = -((0 - distance) // 1) # math.floor the value
            if distance <= 0:
                distance = distance - 1
            bins.append(distance)
        return bins
        
    def moving_range_describe(self):
        mr_mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        limits = self.moving_range_limits()
        description = 'Moving Range' + '\n'
        description = description + '============' + '\n'
        description = description + 'Upper control limit = ' + str(limits[1]) + '\n'
        description = description + 'Moving Range mean = ' + str(mr_mean) + '\n'
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

    # puts observations into a bin corresponding to their distance from the mean in standard deviations
    def individuals_bins(self):
        bins = []
        sigma = self.individuals_sigma()
        mean = self.individuals_mean()
        for value in range(len(self.value_series)):
            distance = (self.value_series[value] - mean) / sigma
            distance = -((0 - distance) // 1) # math.floor the value
            if distance <= 0:
                distance = distance - 1
            bins.append(distance)
        return bins

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

    def identify_violations(self):
        return []

    def plot(self, title="Control Chart", x_label="Period", i_label="Observations", mr_label="mR", file=''):        
        from matplotlib import pyplot as plt

        plt.figure(figsize=(12, 12))
        plt.title("Title")  
        
        # individual
        ax = plt.subplot(211)
        plt.plot(self.period_series, self.value_series, marker='o', markersize=3, color='b')
        plt.axhline(y=self.individuals_standard_deviation(-3), color='r')
        plt.axhline(y=self.individuals_standard_deviation(-2), color='r', linestyle=':')
        plt.axhline(y=self.individuals_standard_deviation(-1), color='r', linestyle=':')
        plt.axhline(y=self.individuals_standard_deviation( 0), color='g')
        plt.axhline(y=self.individuals_standard_deviation( 1), color='r', linestyle=':')
        plt.axhline(y=self.individuals_standard_deviation( 2), color='r', linestyle=':')
        plt.axhline(y=self.individuals_standard_deviation( 3), color='r')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Individuals")  
        plt.xlabel(x_label)
        plt.ylabel(i_label)
        
        # moving range
        ax = plt.subplot(212)
        plt.plot(self.period_series[:-1], self.mR_series, marker='o', markersize=3, color='b')
        plt.axhline(y=self.moving_range_standard_deviation(-3), color='r')
        plt.axhline(y=self.moving_range_standard_deviation(-2), color='r', linestyle=':')
        plt.axhline(y=self.moving_range_standard_deviation(-1), color='r', linestyle=':')
        plt.axhline(y=self.moving_range_standard_deviation( 0), color='g')
        plt.axhline(y=self.moving_range_standard_deviation( 1), color='r', linestyle=':')
        plt.axhline(y=self.moving_range_standard_deviation( 2), color='r', linestyle=':')
        plt.axhline(y=self.moving_range_standard_deviation( 3), color='r')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Moving Range")  
        plt.xlabel(x_label)
        plt.ylabel(mr_label)

        if (len(file) > 0):
            plt.savefig(file, format='svg')