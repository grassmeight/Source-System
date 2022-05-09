from typing import List, Dict, Tuple
from queue import Queue
import sys
import os
import logging
import matplotlib
import pandas as pd
import numpy as np
import seaborn as sb
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

def sumBar(x, y, data, order):
    plot = sb.catplot(x = x, y = y, data = data, kind = 'bar', estimator = sum, ci = None, order = order)

    for i, bar in enumerate(plot.ax.patches):
        h = bar.get_height()
        plot.ax.text(i, h + 10, '{}'.format(int(h)), ha = 'center', va = 'center', fontweight = 'bold', size = 14)
    
    return plot.figure
