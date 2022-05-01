from typing import List, Dict, Tuple
from queue import Queue
import sys
import os
import logging
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

def sumBar(x, y, data):
    plot = sb.catplot(x = x, y = y, data = data, kind = 'bar', estimator = sum, ci = None)

    for i, bar in enumerate(plot.ax.patches):
        h = bar.get_height()
        plot.ax.text(i, h + 10, '{}'.format(int(h)), ha = 'center', va = 'center', fontweight = 'bold', size = 14)
    
    return plt.gcf()

def sumBar(x, y, data, order):
    plot = sb.catplot(x = x, y = y, data = data, kind = 'bar', estimator = sum, ci = None, order = order)  

    for i, bar in enumerate(plot.ax.patches):
        h = bar.get_height()
        plot.ax.text(i, h + 10, '{}'.format(int(h)), ha = 'center', va = 'center', fontweight = 'bold', size = 14)