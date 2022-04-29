from pandas import DataFrame
from data_watchdog import *
from data_analyst import *
from GUI import *
from multiprocessing import Process, freeze_support

if __name__ == "__main__":
    db = DataFrame({'A': [0, 1, 2, 3, 4],
                   'B': [5, 6, 7, 8, 9],
                   'C': ['a', 'b', 'c--', 'd', 'e']})
    for value in db.values:
        for row in value:
            print(row)