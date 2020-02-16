
from .general import *

def linear_regression(X, Y): 
    mean_x = mean(X)
    mean_y = mean(Y)
    n = len(X)
    numer = 0
    denom = 0
    for i in range(n):
        numer += (X[i] - mean_x) * (Y[i] - mean_y)
        denom += (X[i] - mean_x) ** 2.0
    m = numer / denom
    c = mean_y - (m * mean_x)
    return m, c