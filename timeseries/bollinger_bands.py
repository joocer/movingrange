

def bollinger_bands(series, length=20, sigmas=2):
    import pandas as pd
    import numpy as np
    
    """ returns average, upper band, and lower band"""
    ave = series.rolling(window=length, center=False).mean()
    sd = series.rolling(window=length,center=False).std() 
    
    upband = ave + (sd * sigmas)
    dnband = ave - (sd * sigmas)
    return np.round(ave,3), np.round(upband,3), np.round(dnband,3)


def plot_bollinger_bands(series, length=20, sigmas=2):
    from matplotlib import pyplot as plt
    plt.figure(figsize=(20, 6))
    a, u, l = bollinger_bands(series, length=24, sigmas=2)
    plt.plot(series)
    plt.plot(a)
    plt.plot(u)
    plt.plot(l)
