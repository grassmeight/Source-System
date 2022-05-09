from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg 
from PyQt5 import uic
from data_analyst import *
from data_watchdog import *

Ui_MainWindow, baseClass = uic.loadUiType('Uis\\jobs_window.ui')

class MainWindow(qtw.QMainWindow):
    def __init__(self, data = pd.DataFrame(), *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.createTable(data)
        self.createGraph(data)

        self.show()
    
    def createGraph(self, data):
        figure = sumBar("שלב", "כמות", data, ["תכנון","ביצוע","פיזור"])
        figure.tight_layout()
        self.canvas = FigureCanvasQTAgg(figure)
        self.ui.NigLayout.addWidget(self.canvas)

    def createTable(self, data):
        self.model = PandasModel(data)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)

        self.ui.levelComboBox.addItem("")
        self.ui.jobComboBox.addItem("")

        self.ui.levelComboBox.addItems(self.model.returnColumn("שלב").unique())
        self.ui.jobComboBox.addItems(self.model.returnColumn("מקצוע").astype(str).unique())

class PandasModel(qtc.QAbstractTableModel):
    def __init__(self, data, parent = None) -> None:
        super().__init__(parent)
        self.dataFrame = data
    
    def rowCount(self, parent = None) -> int:
        return len(self.dataFrame.values)

    def columnCount(self, parent = None) -> int:
        return self.dataFrame.columns.size
    
    def returnColumn(self, column):
        if type(column) == str:
            return self.dataFrame[column]
    
    def returnRow(self, row):
        if type(row) == int:
            return self.dataFrame.iloc[row]
    
    def data(self, index, role = qtc.Qt.DisplayRole):
        if (index.isValid()):
            if (role == qtc.Qt.DisplayRole):
                return qtc.QVariant(str(self.dataFrame.iloc[index.row()][index.column()]))
            if (role == qtc.Qt.TextAlignmentRole):
                return qtc.QVariant(qtc.Qt.AlignHCenter + qtc.Qt.AlignVCenter)
            if (role == qtc.Qt.FontRole):
                font = qtg.QFont()
                font.setWeight(qtg.QFont.DemiBold)
                return font
        return qtc.QVariant()
    
    def headerData(self, section, orientation, role = qtc.Qt.DisplayRole):
        if (orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole):
            return self.dataFrame.columns[section]
        if (orientation == qtc.Qt.Horizontal and role == qtc.Qt.TextAlignmentRole):
            return qtc.QVariant(qtc.Qt.AlignHCenter + qtc.Qt.AlignVCenter)
        if (orientation == qtc.Qt.Horizontal and role == qtc.Qt.FontRole):
            font = qtg.QFont()
            font.setWeight(qtg.QFont.ExtraBold)
            return font
        return None

if __name__ == "__main__":
    watchdog = DataWatchdog()
    analyst = DataAnalyst(watchdog.getData()[0], watchdog.getData()[1], watchdog.getData()[2], watchdog.getCodex()[0], watchdog.getCodex()[1])
    app = qtw.QApplication(sys.argv)
    mw = MainWindow(analyst.getDataLong()[0])
    sys.exit(app.exec())