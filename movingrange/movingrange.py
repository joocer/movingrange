class movingrange:
    
    # https://en.wikipedia.org/wiki/Shewhart_individuals_control_chart
    
    # some code comments taken from: 
    # https://www.staceybarr.com/measure-up/build-xmr-chart-kpi/
    
    period_series = []
    value_series = []
    mR_series = []

    def load_from_pandas(self, df, periodcolumn, valuecolumn):
        import pandas
        self.load_from_arrays(df[periodcolumn].tolist(), df[valuecolumn].tolist())

    def load_from_arrays(self, period_series, value_series):
        self.period_series = period_series
        self.value_series = value_series
        self.mR_series = []
        for i in range(len(value_series) - 1):
            mR = abs(value_series[i] - value_series[i + 1])
            self.mR_series.append(mR)

    def moving_range_mean(self):
        return sum(self.mR_series) / len(self.mR_series)
        
    # 3.267 is a magic number
    def moving_range_control_limit(self):
        mr_mean = self.moving_range_mean()
        return 3.267 * mr_mean
        
    def individuals_mean(self):
        return sum(self.value_series) / len(self.value_series)

    # 2.66 is a magic number
    # it is a statistically derived constant that makes the Natural Process Limits 
    # roughly equivalent to three standard deviations from the Central Line
    def individuals_control_limits(self):
        
        individuals_mean = self.individuals_mean()
        mr_mean = self.moving_range_mean()
        ucl = individuals_mean + 2.66 * mr_mean
        lcl = individuals_mean - 2.66 * mr_mean
        if lcl < 0:
            lcl = 0
        return lcl, ucl
    
    # A point outside the Natural Process Limits indicates something unusual happened. 
    # Just find out what it was, don’t try to fix it unless it’s a real problem.
    def indentify_special_cases(self):
        mr_samples = []
        i_samples = []
        mr_ucl = self.moving_range_control_limit()
        for i in range(len(self.mR_series)):
            if self.mR_series[i] > mr_ucl:
                mr_samples.append(i)
        i_lcl, i_ucl = self.individuals_control_limits()
        for i in range(len(self.value_series)):
            if sorted((i_lcl, self.value_series[i], i_ucl))[1] != self.value_series[i]:
                i_samples.append(i)
        return i_samples, mr_samples
    
    # At least 3 out of 4 consecutive points closer to the same Natural Process Limit 
    # than to the Central Line. 
    def identify_short_run(self, sample_size = 4, sample = 3):
        print('identify_short_run: not implemented')
        rolling = [0] * sample_size
        for i in range(len(self.mR_series)):
            rolling.append(self.mR_series[i])
            rolling = rolling[1:]
        samples = []
        return samples
    
    # At least 8 consecutive points running on one side of the Central Line indicates 
    # a change. Find out the cause – it might be an initiative you implemented that 
    # worked, or something else. 
    # Use the points in the long run to recalculate the Central Line and 
    # Natural Process Limits.
    def identify_long_run(self, sample_size = 8):
        print('identify_long_run: not implemented')
        return 1
    
    def plot(self, title="Control Chart", xlabel="Period", ylabel="mR", file='XmR.svg'):        
        from matplotlib import pyplot as plt

        mr_mean = self.moving_range_mean()
        sample_mean = self.individuals_mean()

        mr_ucl = self.moving_range_control_limit()
        i_ucl, i_lcl = self.individuals_control_limits()

        plt.figure(figsize=(12, 12))
        plt.title("Title")  
        
        # individual
        ax = plt.subplot(211)
        plt.plot(self.period_series, self.value_series, marker='o', markersize=3, color='b')
        plt.axhline(y=sample_mean, color='g')
        plt.axhline(y=i_ucl, color='r')
        plt.axhline(y=i_lcl, color='r')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Individuals")  
        plt.xlabel(xlabel)
        plt.ylabel("Observation")
        
        # moving range
        ax = plt.subplot(212)
        plt.plot(self.period_series[:-1], self.mR_series, marker='o', markersize=3, color='b')
        plt.axhline(y=mr_mean, color='g')
        plt.axhline(y=mr_ucl, color='r')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Moving Range")  
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.savefig(file, format='svg')