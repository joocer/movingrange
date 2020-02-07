# replaces nan items from a series with a given value
def fillna(series, filler=0):
    import math
    result = []
    for i in series:
        if math.isnan(i):
            result.append(filler)
        else:
            result.append(i)
    return result

# average of the series
def mean(series):
    return sum(series) / len(series)

# standard deviateion of the series
def standard_deviation(series):
    return variance(series) ** (1.0/2.0)

# statistal variance of the series
def variance(series):
    series_mean = mean(series)
    cumulate = []
    for i in series:
        cumulate.append((i - series_mean) ** 2.0)
    cumulate_mean = mean(cumulate)
    return cumulate_mean    

# executes a rule against each item in a series and returns matches
def matches(series, rule):
    indices = []
    for i in range(len(series)):
        if rule(series[i]):
            indices.append(i)
    return indices