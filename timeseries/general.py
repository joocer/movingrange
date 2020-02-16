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
    return sum(series) / float(len(series))

# standard deviateion of the series
def standard_deviation(series):
    return variance(series) ** (1.0/2.0)

# statistal variance of the series
def variance(series):
    series_mean = mean(series)
    return sum([(x-series_mean)**2.0 for x in series]) / len(series)

# executes a rule against each item in a series and returns matches, rule should be a lambe
# matches(data, lambda x: x > 2)
def matches(series, rule):
    indices = []
    for i in range(len(series)):
        if rule(series[i]):
            indices.append(i)
    return indices

# applied a function to a series of values, formula should be a lambda
# f_x(data, lambda x: 3x + 2)
def f_x(series, formula):
    r = []
    for i in range(len(series)):
        r.append(formula(series[i]))
    return r