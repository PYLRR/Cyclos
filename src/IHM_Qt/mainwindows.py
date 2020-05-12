import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QGridLayout, QVBoxLayout

from src.modules.parser import parseFromFile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
from src.modules.nXHandler import getnxFromDependencies,savenxGraph

# handles the qt application
class ProtocoleWidget(QtWidgets.QWidget):
    # sets the window
    def __init__(self):
        super().__init__()
        self.chemin = QtWidgets.QLineEdit()
        text = QtWidgets.QLabel("Chemin du fichier du protocole à ouvrir :")
        button = QtWidgets.QPushButton("Generate graph and give acyclicity")
        button.clicked.connect(self.graph_generation)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(text)
        layout.addWidget(self.chemin)
        layout.addWidget(button)
        layout.setAlignment(QtCore.Qt.AlignTop)

        self.protocol=QtWidgets.QListView()
        self.protocol.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.protocol.setWindowTitle('Protocol')
        #self.protocol.setMinimumSize(600, 400)
        # Create an empty model for the list's data
        self.model = QtGui.QStandardItemModel(self.protocol)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.resize(600, 400)

        layoutProtocolGraph=QtWidgets.QHBoxLayout()
        layoutProtocolGraph.addWidget(self.protocol)
        layoutProtocolGraph.addWidget(self.canvas)
        layoutGeneral = QtWidgets.QVBoxLayout()
        layoutGeneral.addLayout(layout)
        layoutGeneral.addLayout(layoutProtocolGraph)

        self.setLayout(layoutGeneral)

    # draws graph and protocol on the window
    def graph_generation(self): #tester avec ../tests/parser/protocolForTests
        self.model.removeRows(0,self.model.rowCount())
        print(self.chemin.text())
        protocol = parseFromFile(self.chemin.text())
        self.ficherEnregistrementProtocol = open(protocol.name+" parsé.txt", "w")

        print("\n\nVARIABLES FOUND :")
        for var in protocol.listVar:
            if(not(var.isDeclaredOnTheFly())):
                print(var)
                self.ficherEnregistrementProtocol.write(var.toStringOnVarDeclaration()+"\n")
                item = QtGui.QStandardItem(var.toStringOnVarDeclaration())
                self.model.appendRow(item)
        self.ficherEnregistrementProtocol.write("\n\n")
        self.model.appendRow("")
        self.model.appendRow("")
        print("\n\nTRANSACTIONS FOUND :")
        for trans in protocol.listTransactions:
            self.ficherEnregistrementProtocol.write(trans.label + "\n")
            print(trans.label)
            item = QtGui.QStandardItem(trans.label)
            self.model.appendRow(item)
            for action in trans.actions:
                act=action.__str__()
                print("-" + act)
                self.ficherEnregistrementProtocol.write(act + "\n")
                item = QtGui.QStandardItem(act)
                self.model.appendRow(item)
            self.ficherEnregistrementProtocol.write("\n")
            self.model.appendRow("")
        # Apply the model to the list view
        self.protocol.setModel(self.model)
        print("\n\nTYPES FOUND :")
        for type in protocol.listTypes:
            print(type)
        self.ficherEnregistrementProtocol.close()
        nxgraph = getnxFromDependencies(protocol, protocol.build_dependencies())
        self.figure.clf()
        self.canvas.draw_idle()
        savenxGraph(nxgraph, self.chemin.text()+"-graph.png")
        protocol.reset()

# used to test "by hand" qt windows
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationDisplayName("Cyclos")
    widget = ProtocoleWidget()
    widget.resize(1900, 1000)
    widget.show()

    sys.exit(app.exec_())