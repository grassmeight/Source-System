from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from utility import *
from time import sleep

DATA_PATH = 'Data Sample\\Data Sample Original.xlsx'

class DataWatchdog(object):
    #a simple constructor
    def __init__(self) -> None:
        #setting up the three DataFrames that will be used to store the data (planning, execution, placement)
        self.planData = pd.DataFrame.empty
        self.execData = pd.DataFrame.empty
        self.placementData = pd.DataFrame.empty

        #setting up the two DataFrames that will be used as base for the execution data
        self.jobCodex = pd.DataFrame.empty
        self.targetCodex = pd.DataFrame.empty

        #getting the data for the first time using the constant DATA_PATH
        self.readFiles(DATA_PATH)
    
    #the method used to access and read the data file
    def readFiles(self, path, queue = None):
        #reading both files types with the matching functions
        self.readData(path)
        self.readCodex(path)

        #if there is a queue then pass the data for the queue
        if queue is not None:
            queue.put([self.planData, self.execData, self.placementData, self.jobCodex, self.targetCodex])
    
    #the method that reads the data files from a given path
    def readData(self, path):
        #setting a try/catch block in order to make sure the program won't crash if the files couldn't be loaded
        try:
            #replacing the data with the new data, by reading the Excel data file
            self.planData = pd.read_excel(path, sheet_name = 'סטים')
            self.execData = pd.read_excel(path, sheet_name = 'אדומים כחולים')
            self.placementData = pd.read_excel(path, sheet_name = 'פיזורים')
        except:
            #in the case of an exception, printing an error message
            path(f"Data file doesn't exist in the directory {path}")
    
    #the method that reads the codex files from a given path
    def readCodex(self, path):
        #setting a try/catch block in order to make sure the program won't crash if the files couldn't be loaded
        try:
            #replacing the data with the new data, by reading the Excel data file
            self.targetCodex = pd.read_excel(path, sheet_name = 'מסד יעדים')
            self.jobCodex = pd.read_excel(path, sheet_name = 'מסד מקצועות')
        except:
            #in the case of an exception, printing an error message
            path(f"Codex file doesn't exist in the directory {path}")
    
    #the main loop method where we will set up the watchdog to read changes that happens to our data file directory
    def processUpdate(self, queue):
        #condiguring a logger (running on a seperate thread so that messaged could still be displayed with the watchdog thread lock)
        logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

        #making a path parameter and setting it to the current running directory (I think?)
        path = sys.argv[1] if len(sys.argv) > 1 else '.'

        #setting the event handler for our watchdog.
        #First, making it a pattern matching event handler that will only look at Excel files
        event_handler = PatternMatchingEventHandler(patterns = ["Data*.xlsx"], ignore_patterns = [], ignore_directories = True)

        #Second, replacing the on_created and on_modified methods with readFiles
        #This will make the watchdog try and read the data files everytime an Excel file is created or modified
        event_handler.on_created = self.readFiles(DATA_PATH, queue)
        event_handler.on_modified = self.readFiles(DATA_PATH, queue)

        #setting up the observer (a.k.a the actual watchdog), and passing our event_handler and path to it using schedule
        observer = Observer()
        observer.schedule(event_handler, path, recursive = True)
        observer.daemon = True

        #starting the observer
        observer.start()

        #setting the observer loop to be infinite, except when the user does a KeyboardInterrupt
        #TODO: try setting up a flag instead
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    #a simple method to access the data from other classes
    def getData(self) -> List[pd.DataFrame]:
        return [self.planData, self.execData, self.placementData]
    
    #a simple method to access the codex from other classes
    def getCodex(self) -> List[pd.DataFrame]:
        return [self.jobCodex, self.targetCodex]

#a simple check for the class
if __name__ == "__main__":
    inst = DataWatchdog()