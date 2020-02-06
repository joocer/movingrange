from .general import *

def rolling_average(series, window):
    import math
    roller = []
    for i in range(math.floor(window / 2) + 1):
        roller.append(math.nan)
    for i in range(len(series) - window + 1):
        roller.append (mean(series[i:i+window]))
    for i in range(math.ceil(window / 2)):
        roller.append(math.nan)
    return roller[1:len(series) + 1]

def identify_cycle(series, window):
    pattern = []
    series_mean = mean(series)
    cycle_sum = [0] * window
    cycle_count = [0] * window
    for i in range(len(series)):
        cycle_sum[i % window] = cycle_sum[i % window] + series[i]
        cycle_count[i % window] = cycle_count[i % window] + 1
    for i in range(window):
        cycle_mean = cycle_sum[i] / cycle_count[i]
        pattern.append(series_mean / cycle_mean)
    return pattern

def cyclic_trend(series, window):
    cycle = identify_cycle(series,window)
    apogee = max(cycle)
    series_max = max(series)
    pattern = []
    for i in range(len(series)):
        pattern.append((1 - (cycle[i % window] / apogee)) * series_max)
    return pattern

class decomposed_seasonal_data:

    def __init__(self, source, residual, seasonal, rolling, cycle_size):
        self.source = source
        self.residual = residual
        self.seasonal = seasonal
        self.trend = rolling
        self.cycle_size = cycle_size

    # plot()