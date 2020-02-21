# timeseries

A Python library for the interpretation and treatment of time-series data.

## What is it?

A set of methods to process timeseries data.

## Main Features

Seasonal Decomposition
-> trend
-> detrend
-> seasonal
-> residual
-> plot()

### Seasonal Adjustment
~~~~
timeseries.seasonal_pattern (series, period)
timeseries.series_frequencies (series)
timeseries.cycle_periods (series) <- estimate
~~~~

### Trending
~~~~
timeseries.linear_regression (x, y)
timeseries.henderson (series, window)
timeseries.rolling_average (series, window)
~~~~

Methods for identifying and describing trends in data.


### Control Charts
~~~~
cc = timeseries.control_chart(series, samples=8)
~~~~

### Predict
~~~~
// predict (cycles)
~~~~

### Helper Methods
~~~~
timeseries.fillna (series, filler=0)
timeseries.mean (series)
timeseries.standard_deviation (series)
timeseries.variance (series)
timeseries.matches (series, rule)
timeseries.f_x (series, function)
~~~~

## Dependencies
- [matplotlib](https://matplotlib.org/)
- [NumPy](https://www.numpy.org)

## License
[Apache-2.0](LICENSE)

## Credits
- Henderson adapted from [Mark Graph's Implementation](https://markthegraph.blogspot.com/2014/06/henderson-moving-average.html) 
