import sys
from PySide2 import QtCore, QtWidgets, QtGui

from src.IHM_Qt.mainwindows import ProtocoleWidget

class TabWindows(QtWidgets.QTabWidget):
    compt = 1

    # handles tabs
    def __init__(self):
        super().__init__()
        self.layoutGeneral = QtWidgets.QVBoxLayout()
        self.buttontab = QtWidgets.QPushButton("Add a new tab")
        self.tabWidget=QtWidgets.QTabWidget()
        self.layoutGeneral.addWidget(self.buttontab)
        self.buttontab.clicked.connect(self.inittab())
        self.layoutGeneral.addWidget(self.tabWidget)
        self.setLayout(self.layoutGeneral)
        self.tabWidget.addTab(ProtocoleWidget(),"Protocol1")
        self.tabWidget.addTab(ProtocoleWidget(), "Protocol2")

    def inittab(self):
        pass

# used to test "by hand" the tabs qt applications
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName("Cyclos")
    widget = TabWindows()
    widget.resize(1900, 1000)
    widget.show()

    sys.exit(app.exec_())