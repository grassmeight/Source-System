from utility import *
from data_watchdog import *
from data_analyst import *

if __name__ == "__main__":
    watchdog = DataWatchdog()
    analyst = DataAnalyst(watchdog.getData()[0], watchdog.getData()[1], watchdog.getData()[2], watchdog.getCodex()[0], watchdog.getCodex()[1])
    sumBar("שלב", "כמות", analyst.getDataLong()[0], ["תכנון","ביצוע","פיזור"])
    plt.show()