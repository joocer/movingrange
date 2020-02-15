# timeseries

A Python library for the interpretation and treatment of time-series data.

## What is it?

A set of methods to process timeseries data.

## Main Features

### Trending
~~~~
timeseries.linear_regression (x, y)
timeseries.Henderson (series, window)
timeseries.rolling_average (series, window)
// loess
~~~~

### Seasonal Adjustment
~~~~
timeseries.seasonal_pattern (series, period)
timeseries.seasonal_pattern (series, [periods])

timeseries.series_frequencies (series)
timeseries.cycle_periods (series) <- estimate sesonal periods
~~~~

### Control Charts
~~~~
cc = timeseries.control_chart(series, samples=8)
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
