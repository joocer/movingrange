from .general import *
from .henderson import *

# split timeseries into trend, season * trend and residual
def decompose(series):
    periods = cycle_periods(series)
    n = max(periods)
    if n % 2 == 0:
        n = n + 1
    trend = Henderson(series, n)
    seasonal = product_series(series, periods, trend)
    residual = difference_series(series, seasonal)
    return decomposed_seasonal_data(series, trend, seasonal, residual)

# unweighted rolling average
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

# fourier transform to identify frequencies
def cycle_periods(series):
    import numpy as np
    # to remove the DC (usually a 0 peak) subtract the mean of the set from each value
    readings= []
    series_mean = mean(series)
    for i in series:
        readings.append(i - series_mean)
    fourierTransform = np.fft.rfft(readings)
    signal_mean = mean(abs(fourierTransform))
    sigma = standard_deviation(abs(fourierTransform))    
    peaks = matches(abs(fourierTransform), lambda t: t > signal_mean + (3 * sigma))
    # 1 is the sample frequency, it's not meaningful
    if 1 in peaks:
        peaks.remove(1)
    return peaks

# identify cyclic pattern of series data for period
def seasonal_pattern(series, period):
    pattern = []
    series_mean = mean(series)
    cycle_sum = [0] * period
    cycle_count = [0] * period
    for i in range(len(series)):
        cycle_sum[i % period] = cycle_sum[i % period] + series[i]
        cycle_count[i % period] = cycle_count[i % period] + 1
    for i in range(period):
        cycle_mean = cycle_sum[i] / cycle_count[i]
        pattern.append(series_mean / cycle_mean)
    return pattern

# apply the seasonal patterns to the trend data
def product_series(series, cycles, trend):
    if not isinstance(cycles, list): 
        cycles = [cycles]
    base = trend.copy()
    for cycle in cycles:
        pattern = seasonal_pattern(series,cycle)
        for i in range(len(series)):
            base[i] = base[i] / pattern[i % cycle]
    return base

# subtract one series frrom another
def difference_series(seriesA, seriesB):
    diff = []
    for i in range(len(seriesA)):
        diff.append(seriesA[i] - seriesB[i])
    return diff

class decomposed_seasonal_data:

    def __init__(self, source, trend, seasonal, residual):
        self.source = source
        self.trend = trend
        self.seasonal = seasonal
        self.residual = residual
        self.record = len(self.source)

    def plot(self):
        from matplotlib import pyplot as plt
        plt.figure(figsize=(12, 12))

        # raw
        ax = plt.subplot(411)
        plt.ylabel('Source Data')
        ax.axhline(y=mean(self.source), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.source, color='#3333AA')
        # moving average
        ax = plt.subplot(412)
        plt.ylabel('Moving Average')
        ax.axhline(y=mean(self.trend), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.trend, color='#3333AA')
        # seasonal pattern
        ax = plt.subplot(413)
        plt.ylabel('Seasonal')
        ax.axhline(y=mean(self.seasonal), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.seasonal, color='#3333AA')
        # residual
        ax = plt.subplot(414)
        plt.ylabel('Residual')
        ax.axhline(y=mean(self.residual), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.residual, color='#3333AA')
        ax.axhline(y=0, color='r', linestyle=':')