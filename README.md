# timeseries

A Python library for the interpretation and treatment of time-series data.

## What is it?

## Main Features

### Seasonal Adjustment

Decomposing series data into trend, seasonal and residual components.

Rolling Average and Henderson.

Automatic Identification of cycle periods/

### Control Charts

### Helper Methods
~~~~
fillna(series, filler=0)
mean(series)
standard_deviation(series)
variance(series)
matches(series, rule)
~~~~

## Dependencies
- [matplotlib](https://matplotlib.org/)
- [NumPy](https://www.numpy.org)

## License
[Apache-2.0](LICENSE)

## Credits
- Henderson adapted from [Mark Graph's Implementation](https://markthegraph.blogspot.com/2014/06/henderson-moving-average.html) 