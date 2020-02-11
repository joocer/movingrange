from .general import *
from .henderson import *

# split timeseries into trend, season * trend and residual
def decompose(series, periods=[]):
    # if periods aren't set, try to work it out
    if len(periods) == 0:
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
def series_frequencies(series):
    import numpy as np
    # to remove the DC (usually a 0 peak) subtract the mean of the set from each value
    readings= []
    series_mean = mean(series)
    for i in series:
        readings.append(i - series_mean)
    fourierTransform = np.fft.rfft(readings)
    return fourierTransform

# fourier transform to identify frequencies
def cycle_periods(series):
    fourierTransform = abs(series_frequencies(series))
    signal_mean = mean(fourierTransform)
    sigma = standard_deviation(fourierTransform)
    for s in range(10,0,-1):
        peaks = matches(fourierTransform, lambda t: t > signal_mean + (s * sigma))
        # 1 is the sample frequency, it's not meaningful
        if 1 in peaks:
            peaks.remove(1)
        if len(peaks) > 0:
            return peaks
    raise TypeError('No cycle identified')
    
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
        plt.ylabel('Source')
        ax.axhline(y=mean(self.source), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.source, color='#6666AA')
        # moving average
        ax = plt.subplot(412)
        plt.ylabel('Trend')
        ax.axhline(y=mean(self.trend), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.trend, color='#6666AA')
        # seasonal pattern
        ax = plt.subplot(413)
        plt.ylabel('Seasonal')
        ax.axhline(y=mean(self.seasonal), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.seasonal, color='#6666AA')
        # residual
        ax = plt.subplot(414)
        plt.ylabel('Residual')
        ax.axhline(y=mean(self.residual), color='#AAAAAA', linestyle=':')
        plt.plot(range(self.record), self.residual, color='#6666AA')
        ax.axhline(y=0, color='#AA6666')