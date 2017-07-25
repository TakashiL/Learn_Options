import scipy
import numpy as np
from math import log, sqrt, exp
from scipy.stats import norm
from scipy.optimize import brentq

# calculate the price of a European call/put option by Black-Scholes Option Pricing Model
def call_option_pricer(spot, strike, maturity, r, vol):
    d1 = (log(spot/strike) + (r + vol*vol*0.5) * maturity) / (vol * sqrt(maturity))
    d2 = d1 - vol * sqrt(maturity)
    call_price = spot * norm.cdf(d1) - strike * exp(-r*maturity) * norm.cdf(d2)
    return call_price


def put_option_pricer(spot, strike, maturity, r, vol):
    d1 = (log(spot / strike) + (r + vol * vol * 0.5) * maturity) / (vol * sqrt(maturity))
    d2 = d1 - vol * sqrt(maturity)
    put_price = strike * exp(-r*maturity) * norm.cdf(-d2) - spot * norm.cdf(-d1)
    return put_price

# calculate the price of a European call/put option by Monte Carlo Method
def call_option_pricer_monte_carlo(spot, strike, maturity, r, vol, numOfPath = 5000):
    random_series = scipy.random.randn(numOfPath)
    s_t = spot * np.exp((r - 0.5*vol*vol) * maturity + random_series * vol * sqrt(maturity))
    s_t_mean = np.maximum(s_t - strike, 0).mean()
    call_price = exp(-r*maturity) * s_t_mean

    return call_price

# used to calculate implied volatility
class cost_function:
    def __init__(self, target):
        self.targetValue = target

    def __call__(self, x):
        return call_option_pricer(spot, strike, maturity, r, x) - self.targetValue

# parameter
spot = 2.45      # spot price S0
strike = 2.5     # strike price K
maturity = 0.25  # option period T
r = 0.05         # continuous compounding interest rates r
vol = 0.25       # volatility sigma


target = call_option_pricer(spot, strike, maturity, r, vol)
cost_sampel = cost_function(target)

impliedVol = brentq(cost_sampel, 0.0001, 1)

print 'real vol: %.2f' % (vol * 100,) + '%'
print 'implied vol: %.2f' % (impliedVol*100,) + '%'

'''
# output
print 'Price of the call option : %.4f\n' % call_option_pricer(spot, strike, maturity, r, vol)
print 'Price of the put option : %.4f\n' % put_option_pricer(spot, strike, maturity, r, vol)
print 'Price of call option by monte carlo: %.4f\n' % call_option_pricer_monte_carlo(spot, strike, maturity, r, vol, 10000)
'''