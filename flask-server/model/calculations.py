from model.get_data import get_data
from pydataset import data
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class Calculations:

    @classmethod
    def laps(position, data, min, max):

        laps = []
        for row in data:
            if row[3] != None:
                for laptime in row[3]:
                    if laptime >= min and laptime <= max:
                        laps.append(laptime)
        print(laps)
        return laps

    @classmethod
    def average(position, data, min, max):

        sum = 0
        i = 0
        average = 0
        for row in data:
            if row[3] != None:
                for laptime in row[3]:
                    if laptime >= min and laptime <= max:
                        sum += laptime
                        i += 1
        average = round((sum/i), 1)
        print(average)
        return average

    @classmethod
    def high(position, data, Max):
        laps = []
        for row in data:
            for laptimes in row[3]:
                if laptimes <= Max:
                    laps.append(laptimes)

        print(max(laps))
        return (max(laps))

    @classmethod
    def low(position, data, low):
        laps = []
        for row in data:
            for laptimes in row[3]:
                if laptimes >= low:
                    laps.append(laptimes)

        print(str(min(laps)))
        return (min(laps))
