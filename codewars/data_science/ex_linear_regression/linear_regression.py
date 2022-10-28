# https://www.codewars.com/kata/5515395b9cd40b2c3e00116c/train/python
# Task:
# The function that you have to write accepts two list/array, xxx and yyy, representing the coordinates of the points to regress (so that, for example, the first point has coordinates (x[0], y[0])).
# Your function should return a tuple (in Python) or an array (any other language) of two elements: a (intercept) and b (slope) in this order.
# You must round your result to the first 4 decimal digits

# Working:
# x = [25,30,35,40,45,50]
# y = [78,70,65,58,48,42]
# 1. In other words we have a sample of 6 on arbitrary measures of a predictor (x) and criterion/target (y)
# 2. The goal is to be able to predict the arbitary criterion y. To do so, we need use OLS(Linear) regression:
# Note: It's called OLS regression because it minimises the residual sum of squares (that is those that fall outwith the estimation) by fitting a line [of best fit] across the data points
# Y = iYj + bXj, where j is a single case; OR
# y = a + bx
# So if i know the regression coeffiecent/slope and the y-intercept/constant then i can predict y | x
# b = Pearson's r * Sum-of-Squares-y/Sum-of-Squares-x
# Sum-of-Squares-y/x = For j in sample((y/x - Mean-y/x)**2)
# a = Mean-y - b * Mean-x
# Guide - Linear Regress: https://www.youtube.com/watch?v=GhrxgbQnEEU
# Guide - Pearson's R: https://www.youtube.com/watch?v=2SCg8Kuh0tE 

from math import sqrt
import numpy
# import rpy2 # requires an installation of R
# from rpy2 import robjects

# Numpy solution
def regressionLine(x, y):
    """ Return the a (intercept)
        and b (slope) of Regression Line 
        (Y on X).
    """
    # 1. Get Pearson's r
    x = numpy.array(x)
    y = numpy.array(y)
    r = numpy.corrcoef(x,y)
    r = r[0][1]
    print(r)

    n = len(x) # To bullet-proof this solution, we would need to match the data entries case by case so that missing data can be excluded
    df = n-1

    meany = numpy.mean(y)
    meanx = numpy.mean(x)
    print(meany,meanx)
    sy = sqrt(sum([(yj-meany)**2 for yj in y])/(df))
    sx = sqrt(sum([(xj-meanx)**2 for xj in x])/(df))
   
    b = r*(sy/sx)
    a = meany - b * meanx

    return (round(a,4),round(b,4))

regressionLine([25,30,35,40,45,50], [78,70,65,58,48,42])
# Yt ex: regressionLine([17,13,12,15,16,14,16,16,18,19], [94,73,59,80,93,85,66,79,77,91])

# Hand-calculation solution


# R solution
# Help: https://www.askpython.com/python/examples/r-in-python
# https://www.stats.bris.ac.uk/R/index.html 