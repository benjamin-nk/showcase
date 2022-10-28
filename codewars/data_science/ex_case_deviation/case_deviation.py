# https://www.codewars.com/kata/568ff914fc7a40a18500005c/train/python
import statistics

def distances_from_average(test_list):
    mn = statistics.mean(test_list)

    return [round(mn - x,2) for x in test_list]