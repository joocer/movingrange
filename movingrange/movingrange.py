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
        # 3.267 = 1 + (3 x sigma) / mean
        # 2.267 = (3 x sigma) / mean
        # mean x 2.267 = 3 x Sigma
        # sigma = (mean x 2.267) / 3
        mr_mean = self.moving_range_mean()
        sigma = (mr_mean * 2.267) / 3
        return sigma

    def moving_range_limits(self):
        sigma = self.moving_range_sigma()
        mr_mean = self.moving_range_mean()
        return  mr_mean - (sigma * 3), mr_mean + (sigma * 3)
        
    def moving_range_describe(self):
        mr_mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        limits = self.moving_range_limits()
        print ("Upper control limit =", limits[1])
        print ("Moving Range mean =", mr_mean)
        print ("Lower control limit  =", limits[0])
        print ("Sigma(mR) =", sigma)
        print ("1 Sigma =", mr_mean + (sigma * 1))
        print ("2 Sigma =", mr_mean + (sigma * 2))
        print ("3 Sigma =", mr_mean + (sigma * 3))

    def individuals_describe(self):
        #d2 = 1.128
        #Upper control limit  = 20.6531760715387
        #Average moving range = 18.583333333333332
        #Lower control limit  = 16.513490595127966
        #Sigma(X) = 0.689947579401789
        #-3 Sigma = 16.513490595127966
        #-2 Sigma = 17.203438174529754
        #-1 Sigma = 17.893385753931543
        #0 Sigma = 18.583333333333332
        #1 Sigma = 19.27328091273512
        #2 Sigma = 19.96322849213691
        #3 Sigma = 20.6531760715387
        return 1

    def individuals_mean(self):
        return sum(self.value_series) / len(self.value_series)

    # 3 = 2.66
    # 2 = 1.77
    # 1 = 1.128

    # it is a statistically derived constant that makes the Natural Process Limits 
    # roughly equivalent to three standard deviations from the Central Line
    def individuals_limits(self):
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
        mr_lcl, mr_ucl = self.moving_range_limits()
        for i in range(len(self.mR_series)):
            if self.mR_series[i] > mr_ucl:
                mr_samples.append(i)
        i_lcl, i_ucl = self.individuals_limits()
        for i in range(len(self.value_series)):
            if sorted((i_lcl, self.value_series[i], i_ucl))[1] != self.value_series[i]:
                i_samples.append(i)
        return i_samples, mr_samples
    
    # Consecutive points the same side of the Central Line. 
    def identify_run(self, samples = 6):
        run_samples = []
        mr_mean = self.moving_range_mean()
        rolling = [0] * samples
        for i in range(len(self.mR_series)):
            side = self.mR_series[i] - mr_mean
            side = side / abs(side)
            rolling.append(side)
            rolling = rolling[1:]
            if abs(sum(rolling)) == samples:
                for index in range(samples):
                    run_samples.append(i - index + 1)
        return list(set(run_samples))

    def plot(self, title="Control Chart", x_label="Period", i_label="Observations", mr_label="mR", file='XmR.svg'):        
        from matplotlib import pyplot as plt

        mr_mean = self.moving_range_mean()
        sample_mean = self.individuals_mean()
        mr_sigma = self.moving_range_sigma()

        mr_lcl, mr_ucl = self.moving_range_limits()
        i_ucl, i_lcl = self.individuals_limits()

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
        plt.xlabel(x_label)
        plt.ylabel(i_label)
        
        # moving range
        ax = plt.subplot(212)
        plt.plot(self.period_series[:-1], self.mR_series, marker='o', markersize=3, color='b')
        plt.axhline(y=mr_mean, color='g')
        plt.axhline(y=mr_mean + (mr_sigma * 1), color='r', linestyle=':')
        plt.axhline(y=mr_mean + (mr_sigma * 2), color='r', linestyle=':')
        plt.axhline(y=mr_mean + (mr_sigma * 3), color='r')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Moving Range")  
        plt.xlabel(x_label)
        plt.ylabel(mr_label)

        plt.savefig(file, format='svg')