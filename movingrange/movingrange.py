from rulesets import rulesets
from segment import segment

class movingrange: 
    # https://en.wikipedia.org/wiki/Shewhart_individuals_control_chart
    
    def __init__(self, baseline_sample_size = 8):
        self.period_series = []
        self.value_series = []
        self.segments = []
        self.rules = rulesets(self)
        self.baseline_sample_size = baseline_sample_size

    def load_from_pandas(self, df, period_column, value_column):
        import pandas
        self.load_from_arrays(df[period_column].tolist(), df[value_column].tolist())

    def load_from_arrays(self, period_series, value_series):
        self.period_series = period_series
        self.value_series = value_series
        self.segments = self.segment_data()

    # when 8 samples fall the same side of the mean, recalculate the 
    # mean and standard deviations
    def segment_data(self):
        # not big enough to have more than one segment
        if (len(self.value_series) < (2 * self.baseline_sample_size)):
            pass

        boundaries = []
        last_boundary = 0

        current_mean = calculate_mean(self.value_series[0:self.baseline_sample_size])
        for start in range(len(self.value_series) - self.baseline_sample_size + 1):
            # don't start a new segment close to the last
            if (start - self.baseline_sample_size) > last_boundary:
                cummulative_sum = 0
                for index in range(self.baseline_sample_size):
                    delta = self.value_series[start + index] - current_mean
                    # avoid divide by 0
                    if delta == 0:
                        side = 0
                    else:
                        side = delta / abs(delta)
                    cummulative_sum = cummulative_sum + side
                if abs(cummulative_sum) == self.baseline_sample_size:
                    boundaries.append((last_boundary, start))
                    last_boundary = start
                    current_mean = calculate_mean(self.value_series[start + 1:(start + self.baseline_sample_size)])
        # add everything else to the last segment
        boundaries.append((last_boundary, len(self.value_series)))

        segments = []
        for boundary in boundaries:
            start, end = boundary
            segments.append(segment(self, start, end, self.baseline_sample_size))

        return segments

    def describe(self):
        description = 'Population' + '\n'
        description = description + '===========' + '\n'
        description = description + 'Number of Samples = ' + str(len(self.value_series)) + '\n'
        description = description + 'Population Mean = ' + str(calculate_mean(self.value_series)) + '\n'
        description = description + 'Population Maximum = ' + str(max(self.value_series)) + '\n'
        description = description + 'Population Minimum = ' + str(min(self.value_series)) + '\n'
        description = description + 'Number of Segments = ' + str(len(self.segments)) + '\n'

        print (description)

    def individuals_bins(self):
        bins = []
        for segment in self.segments:
            bins = bins + segment.individuals_bins()
        return bins

    def individuals_direction(self):
        directions = []
        for segment in self.segments:
            directions = directions + segment.individuals_direction()
        return directions

    def plot(self, title="Control Chart", x_label="Period", i_label="Observations", mr_label="mR", file=''):        
        from matplotlib import pyplot as plt

        plt.figure(figsize=(12, 12))
        plt.title("Title")  
        
        sigma_m3 = []
        sigma_m2 = []
        sigma_m1 = []
        sigma_0 = []
        sigma_1 = []
        sigma_2 = []
        sigma_3 = []
        for segment in self.segments:
            sigma_m3 = sigma_m3 + segment.individuals_sigma_line(-3)
            sigma_m2 = sigma_m2 + segment.individuals_sigma_line(-2)
            sigma_m1 = sigma_m1 + segment.individuals_sigma_line(-1)
            sigma_0 = sigma_0 + segment.individuals_sigma_line(0)
            sigma_1 = sigma_1 + segment.individuals_sigma_line(1)
            sigma_2 = sigma_2 + segment.individuals_sigma_line(2)
            sigma_3 = sigma_3 + segment.individuals_sigma_line(3)

        # individual
        ax = plt.subplot(211)
        plt.plot(self.period_series, self.value_series, marker='o', markersize=3, color='b')

        plt.plot(self.period_series, sigma_m3, color='r')
        plt.plot(self.period_series, sigma_m2, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_m1, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_0, color='g')
        plt.plot(self.period_series, sigma_1, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_2, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_3, color='r')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Individuals")  
        plt.xlabel(x_label)
        plt.ylabel(i_label)
        
        sigma_m3 = []
        sigma_m2 = []
        sigma_m1 = []
        sigma_0 = []
        sigma_1 = []
        sigma_2 = []
        sigma_3 = []
        mr = []
        for segment in self.segments:
            sigma_m3 = sigma_m3 + segment.moving_range_sigma_line(-3)
            sigma_m2 = sigma_m2 + segment.moving_range_sigma_line(-2)
            sigma_m1 = sigma_m1 + segment.moving_range_sigma_line(-1)
            sigma_0 = sigma_0 + segment.moving_range_sigma_line(0)
            sigma_1 = sigma_1 + segment.moving_range_sigma_line(1)
            sigma_2 = sigma_2 + segment.moving_range_sigma_line(2)
            sigma_3 = sigma_3 + segment.moving_range_sigma_line(3)
            mr = mr + segment.mR_series
            mr.append(segment.mR_series[-1])

        # moving range
        ax = plt.subplot(212)

        plt.plot(self.period_series[:-1], mr[:-1], marker='o', markersize=3, color='b')
        plt.plot(self.period_series, sigma_m3, color='r')
        plt.plot(self.period_series, sigma_m2, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_m1, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_0, color='g')
        plt.plot(self.period_series, sigma_1, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_2, color='r', linestyle=':')
        plt.plot(self.period_series, sigma_3, color='r')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Moving Range")  
        plt.xlabel(x_label)
        plt.ylabel(mr_label)

        if (len(file) > 0):
            plt.savefig(file, format='svg')

def calculate_mean(series):
        return sum(series) / len(series)