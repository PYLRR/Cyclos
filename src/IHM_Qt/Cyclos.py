# -*- coding: utf-8 -*-

import os
import sys

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Qt, QRect
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QTabWidget, \
    QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from networkx import MultiDiGraph

from src.modules import nXHandler
from src.modules.nXHandler import nxHandler, getnxFromDependencies
from src.modules.parser import parseFromFile
from src.protocole.Protocol import Protocol
from src.protocole.protocolError import ProtocolError


# class used to handle refining on/off button
class MyRefiningSwitch(QtWidgets.QPushButton):
    # sets basic properties of the switch
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(120)
        self.setMinimumHeight(22)
        self.check = False

    # qt base event to update the widget
    def paintEvent(self, event):
        label = "Refining ON" if self.check else "Refining OFF"
        bg_color = Qt.green if self.check else Qt.red

        radius = 10
        width = 60
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(0, 0, 0))

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.check:
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)


# main widget containing everything
class ProtocoleWidget(QtWidgets.QWidget):
    # creates all components
    def __init__(self, toolbars, num):
        super().__init__()
        text = QtWidgets.QLabel("Protocol file path :")
        self.chemin = QtWidgets.QLineEdit()
        self.inputFileButton = QtWidgets.QPushButton("...")
        self.inputFileButton.clicked.connect(self.onInputFileButtonSelect)
        self.refiningswitchbutton = MyRefiningSwitch()
        button = QtWidgets.QPushButton("Generate graph and test acyclicity")
        button.clicked.connect(self.graph_generation)
        layoutPath = QtWidgets.QHBoxLayout()
        layoutPath.addWidget(text)
        layoutPath.addWidget(self.chemin)
        layoutPath.addWidget(self.inputFileButton)
        # layoutPath.addWidget(QtWidgets.QLabel("refining ?"))
        layoutPath.addWidget(self.refiningswitchbutton)
        layoutPath.addWidget(button)
        self.errortext = QtWidgets.QLabel("")  # Zone d'affichage du message d'erreur
        self.errortext.setStyleSheet('color: red')
        self.errortext.setMinimumHeight(40)
        self.errortext.setMaximumHeight(40)
        self.protocolListView = QtWidgets.QListView()
        self.protocolListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.protocolListView.setWindowTitle('Protocol')
        self.protocolListView.setMinimumWidth(400)
        self.protocolListView.setMaximumWidth(1000)
        self.protocole = Protocol()
        # Create an empty model for the list's data
        self.model = QtGui.QStandardItemModel(self.protocolListView)
        self.toolbars = toolbars
        self.nxgraph = nxHandler(MultiDiGraph())
        figure = self.nxgraph.draw()
        self.canvas = FigureCanvas(figure)
        self.splitterCanvas = QtWidgets.QSplitter()
        self.splitterCanvas.setOrientation(Qt.Vertical)
        self.splitterCanvas.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.qtoolbar = QtWidgets.QWidget()
        self.qtoolbar.setMinimumHeight(35)
        self.qtoolbar.setMaximumHeight(35)
        self.toolbar.setParent(self.qtoolbar)
        self.toolbars.add_canvas(self.canvas, self.toolbar)
        self.canvas.draw_idle()
        self.generated = False
        self.refiningswitchbutton.clicked.connect(self.refining)
        self.num = num
        self.layoutAcyclicity = QtWidgets.QHBoxLayout()
        checkbox = QtWidgets.QWidget()
        checkbox.setFixedHeight(60)
        self.seq = QtWidgets.QCheckBox('Sequence dependances', checkbox)
        self.seq.toggle()
        self.seq.stateChanged.connect(self.seqDep)
        self.seq.setStyleSheet('color: green')
        self.data = QtWidgets.QCheckBox('Data dependances', checkbox)
        self.data.move(0, 20)
        self.data.toggle()
        self.data.stateChanged.connect(self.dataDep)
        self.data.setStyleSheet('color: red')
        self.key = QtWidgets.QCheckBox('Key Dependances', checkbox)
        self.key.move(0, 40)
        self.key.toggle()
        self.key.stateChanged.connect(self.keyDep)
        self.key.setStyleSheet('color: purple')
        self.layoutAcyclicity.addWidget(checkbox)
        self.layoutAcyclicity2 = QtWidgets.QHBoxLayout()
        self.acyclicity = QtWidgets.QLabel("Cyclic graph?")
        self.acyclicity.setStyleSheet('font:20pt;font-weight: bold;')
        self.layoutAcyclicity2.addWidget(self.acyclicity)
        self.layoutAcyclicity.addLayout(self.layoutAcyclicity2)
        self.layoutCycles = QtWidgets.QVBoxLayout()
        self.cycle = QtWidgets.QCheckBox("Show cycles")
        self.cycle.stateChanged.connect(self.showCycles)
        self.cycle.setStyleSheet('color: black')
        self.previouscyclebutton = QtWidgets.QPushButton("Previous cycle")
        self.previouscyclebutton.clicked.connect(self.previousCycle)
        self.numberCycles = QtWidgets.QLabel("")
        self.nextcyclebutton = QtWidgets.QPushButton("Next cycle")
        self.nextcyclebutton.clicked.connect(self.nextCycle)
        self.layoutAcyclicity.setAlignment(Qt.AlignBottom)
        self.layoutGraph = QtWidgets.QVBoxLayout()
        self.layoutGraph.addWidget(self.splitterCanvas)
        self.layoutGraph.addLayout(self.layoutAcyclicity)
        graph = QtWidgets.QWidget()
        graph.setLayout(self.layoutGraph)
        spliterH = QtWidgets.QSplitter()
        spliterH.setOrientation(Qt.Horizontal)
        spliterH.addWidget(self.protocolListView)
        spliterH.addWidget(graph)
        # self.splitterGeneral = QtWidgets.QSplitter()
        # self.splitterGeneral.setOrientation(Qt.Vertical)
        # self.splitterGeneral.addWidget(self.errortext)
        # self.splitterGeneral.addWidget(spliterH)
        # self.splitterGeneral.setChildrenCollapsible(False)
        self.layoutGeneral = QtWidgets.QVBoxLayout()
        self.layoutGeneral.addLayout(layoutPath)
        self.layoutGeneral.addWidget(self.errortext)
        self.errortext.hide()
        self.layoutGeneral.addWidget(spliterH)
        self.setLayout(self.layoutGeneral)

    # trigered when the user wants to browse to find the input file
    def onInputFileButtonSelect(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                                 caption='Select protocol description file',
                                                                 dir='.',
                                                                 filter='textFile(*.txt);;allFiles(*)')

        if filename:
            self.chemin.setText(str(filename))

    # the refining button is switched (on->off or off->on)
    def refining(self):
        self.refiningswitchbutton.check = not self.refiningswitchbutton.check
        self.model.removeRows(0, self.model.rowCount())
        self.errortext.setText("")
        self.graphReset()

    # the sequence dependencies display button is switched (on->off or off->on)
    def seqDep(self):
        if self.seq.isChecked():
            print("Sequence selected")
            self.nxgraph.drawSeq = True
        else:
            print("Sequence deselected")
            self.nxgraph.drawSeq = False
        self.drawGraph()

    # the data dependencies display button is switched (on->off or off->on)
    def dataDep(self):
        if self.data.isChecked():
            print("data selected")
            self.nxgraph.drawData = True
        else:
            print("Sequence deselected")
            self.nxgraph.drawData = False
        self.drawGraph()

    # the key dependencies display button is switched (on->off or off->on)
    def keyDep(self):
        if self.key.isChecked():
            print("Key selected")
            self.nxgraph.drawKey = True
        else:
            print("Key deselected")
            self.nxgraph.drawKey = False
        self.drawGraph()

    # changes the "highlighted" cycle to the previous one
    def previousCycle(self):
        self.nxgraph.previousCycle()
        self.__showCyclesPosition()  # prints for ex. 1/3
        self.drawGraph()

    # changes the "highlighted" cycle to the next one
    def nextCycle(self):
        self.nxgraph.nextCycle()
        self.__showCyclesPosition()  # prints for ex. 1/3
        self.drawGraph()

    # the cycles highlighted option button is switched (on->off or off->on), it displays or not the next/previous button
    # (no need of them if there is no cycle)
    def showCycles(self):
        if self.cycle.isChecked():
            print("Cycle selected")
            self.nxgraph.drawCycles = True
            self.layoutAcyclicity.addLayout(self.layoutCycles)
            if not self.nxgraph.getCyclesNumber() == 1:
                self.layoutCycles.addWidget(self.previouscyclebutton)
            self.layoutCycles.addWidget(self.numberCycles)
            if not self.nxgraph.getCyclesNumber() == 1:
                self.layoutCycles.addWidget(self.nextcyclebutton)
            self.numberCycles.setAlignment(Qt.AlignCenter)
        else:
            print("Cycle deselected")
            self.nxgraph.drawCycles = False
            self.nextcyclebutton.setParent(None)
            self.numberCycles.setParent(None)
            self.previouscyclebutton.setParent(None)
            self.layoutCycles.setParent(None)
        self.drawGraph()

    # simply draws the graph according to options and updates the file name for when we will save it
    def drawGraph(self):
        if self.canvas != None:
            self.qtoolbar.setParent(None)
            self.canvas.setParent(None)
        figure = self.nxgraph.draw()
        self.canvas.figure = figure
        name = os.path.splitext(self.chemin.text())[0] + ('', ' Sequences')[self.nxgraph.drawSeq] \
               + ('', ' Data')[self.nxgraph.drawData] \
               + ('', ' Key')[self.nxgraph.drawKey] \
               + ('', ' refined')[self.refiningswitchbutton.check]
        self.canvas.get_default_filename = lambda: '{0} graph.png'.format(name)
        self.canvas.draw_idle()
        self.splitterCanvas.addWidget(self.canvas)
        self.splitterCanvas.addWidget(self.qtoolbar)
        self.toolbar.setVisible(True)

    # saves the characteristics of the graph and reset them
    def graphReset(self):
        self.errortext.hide()
        self.acyclicity.setText("Cyclic graph ?")
        self.oldgraph = self.nxgraph
        self.nxgraph = nxHandler(MultiDiGraph())
        self.nxgraph.setOldAttributesDraw(self.oldgraph)
        if self.generated:
            self.protocole.reset()
            self.drawGraph()
            self.acyclicity.setText("Cyclic graph ?")
            self.cycle.setParent(None)
            if self.cycle.isChecked():
                self.cycle.toggle()
            self.nextcyclebutton.setParent(None)
            self.previouscyclebutton.setParent(None)
            self.numberCycles.setParent(None)
            self.generated = False

    # using the input file, creates the graph and displays it
    def graph_generation(self):  # tester avec ../tests/parser/protocolForTests
        self.errortext.hide()
        print(self.chemin.text())
        self.model.removeRows(0, self.model.rowCount())
        self.protocole = Protocol()
        self.errortext.setText("")
        self.graphReset()
        try:
            # parse protocol file
            self.protocole = parseFromFile(self.chemin.text())
            # save the parse protocol in files and print in the list
            self.ficherEnregistrementProtocol = open(os.path.splitext(self.chemin.text())[0] + " parsed.txt", "w",
                                                     encoding="utf-8",
                                                     errors='ignore')
            # Public variables
            self.model.appendRow(QtGui.QStandardItem("public:"))
            self.ficherEnregistrementProtocol.write("public:\n")
            for var in self.protocole.listVar:
                if not var.isDeclaredOnTheFly() and var.public:
                    self.ficherEnregistrementProtocol.write(var.toStringOnVarDeclaration() + "\n")
                    item = QtGui.QStandardItem(var.toStringOnVarDeclaration())
                    self.model.appendRow(item)
            self.ficherEnregistrementProtocol.write("\n\n")
            self.model.appendRow("")

            # Private variables
            self.model.appendRow(QtGui.QStandardItem("private:"))
            self.ficherEnregistrementProtocol.write("private:\n")
            for var in self.protocole.listVar:
                if not var.isDeclaredOnTheFly() and not var.public:
                    self.ficherEnregistrementProtocol.write(var.toStringOnVarDeclaration() + "\n")
                    item = QtGui.QStandardItem(var.toStringOnVarDeclaration())
                    self.model.appendRow(item)
            self.ficherEnregistrementProtocol.write("\n\n")
            self.model.appendRow("")

            # Transactions
            for trans in self.protocole.listTransactions:
                self.model.appendRow("")
                for action in trans.actions:
                    act = action.__str__()
                    self.ficherEnregistrementProtocol.write(act + "\n")
                    item = QtGui.QStandardItem(act)
                    self.model.appendRow(item)
                self.ficherEnregistrementProtocol.write("\n")

            # Apply the model to the list view
            self.protocolListView.setModel(self.model)
            self.ficherEnregistrementProtocol.close()
            # Test typeCompliance
            # self.protocole.testTypeCompliance()
            if self.refiningswitchbutton.check:
                print("Refining ON")
            else:
                print("Refining OFF")
            # Display of the graph
            self.oldgraph = self.nxgraph
            if self.refiningswitchbutton.check:
                self.nxgraph = getnxFromDependencies(self.protocole, self.protocole.refining())
            else:
                self.nxgraph = getnxFromDependencies(self.protocole, self.protocole.build_dependencies())
            self.nxgraph.setOldAttributesDraw(self.oldgraph)
            self.drawGraph()
            if self.nxgraph.isAcyclic():
                self.acyclicity.setText("The dependency graph is acyclic")
            else:
                self.acyclicity.setText("The dependency graph is cyclic")

                self.__showCyclesPosition()  # prints for ex. 1/3

                self.layoutAcyclicity.addWidget(self.cycle)
            # self.nxgraph.saveGraph(os.path.splitext(self.chemin.text())[0]
            #                       + ('', ' Sequences')[self.nxgraph.drawSeq]
            #                       + ('', ' Data')[self.nxgraph.drawData]
            #                       + ('', ' Key')[self.nxgraph.drawKey]
            #                       + ('', ' refined')[self.refiningswitchbutton.check] + " graph.png")
            self.generated = True
        except FileNotFoundError as err:
            print(err)
            self.graphReset()
            self.errortext.setText("Protocole file Not found: {0}".format(err))
            self.errortext.show()
        except ProtocolError as err:
            print(err)
            self.graphReset()
            self.errortext.setText("Error in the protocole description: {0}".format(err))
            self.errortext.show()

    # show the nb of cycles there are and the position of the one we're curently looking (e.g. 1/3)
    def __showCyclesPosition(self):
        #  nb of cycles in the graph, maxed by nXHandler.maxCycles
        cyclesNumber = self.nxgraph.getCyclesNumber()
        # we have less cycles than the max nb of cycles
        if cyclesNumber < nXHandler.maxCycles:
            self.numberCycles.setText(
                "{0}/{1}".format(str(self.nxgraph.numCycleToDraw + 1), str(cyclesNumber)))
        # nb of cycles exceeds the max, we put a "+" to show it
        else:
            self.numberCycles.setText(
                "{0}/{1}".format(str(self.nxgraph.numCycleToDraw + 1), str(cyclesNumber) + "+"))


# handler of the tabs navigation toolbar
class MultiTabNavTool(NavigationToolbar, QWidget):
    # initializes toolbars
    def __init__(self, canvases, tabs, parent=None):
        QWidget.__init__(self)
        self.tabs = tabs
        self.canvases = canvases
        self.toolbars = []
        self.figures = []
        self.tabs.currentChanged.connect(self.switch_toolbar)

    # adds canvas and toolbar
    def add_canvas(self, canvas, toolbar):
        self.canvases.insert(self.tabs.currentIndex(), canvas)
        self.figures.insert(self.tabs.currentIndex(), canvas.figure)
        self.toolbars.append(toolbar)

    # removes toolbar
    def remove_canvas(self, toolbar):
        for i in range(self.tabs.currentIndex(), len(self.canvases) - 1):
            self.canvases.insert(i, self.canvases[i + 1])
        for i in range(self.tabs.currentIndex(), len(self.figures) - 1):
            self.figures.insert(i, self.figures[i + 1])
        self.toolbars.remove(toolbar)

    # stops displaying toolbars and, then, if there is one displays it again after drawing the graph
    def switch_toolbar(self):
        for toolbar in self.toolbars:
            toolbar.setVisible(False)
            plt.close(toolbar.canvas.figure)
        if len(self.toolbars) != 0:
            widget = self.tabs.widget(self.tabs.currentIndex())
            if widget.generated:
                widget.drawGraph()
                self.toolbars[self.tabs.currentIndex()].setVisible(True)
                print(self.canvases[self.tabs.currentIndex()])


# handler of the tabs
class TabWidget(QWidget):
    # creates and configures tabs
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon("./Cyclos.png"))
        self.tabsWidget = QTabWidget()
        self.tabsWidget.setTabsClosable(True)
        self.tabsWidget.setMovable(False)
        self.tabsWidget.setDocumentMode(False)
        self.tabsWidget.setElideMode(Qt.ElideRight)
        self.tabsWidget.setUsesScrollButtons(True)
        self.tabsWidget.tabCloseRequested.connect(self.closeTab)
        self.plusButton = QtWidgets.QPushButton("+")
        self.plusButton.setFixedSize(QtCore.QSize(25, 25))
        self.tabsWidget.setCornerWidget(self.plusButton)
        self.plusButton.clicked.connect(self.buttonClicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabsWidget)
        self.setLayout(vbox)
        self.toolbars = MultiTabNavTool([], self.tabsWidget)
        self.compt = 2
        self.affichage = 1
        self.addTab("Protocol 1", 1)
        self.showMaximized()

    # adds a tab
    def addTab(self, name, num):
        widget = ProtocoleWidget(self.toolbars, num)
        self.tabsWidget.addTab(widget, name)

    # closes a tab
    def closeTab(self, index):
        tab = self.tabsWidget.widget(index)
        plt.close(tab.canvas.figure)
        self.toolbars.remove_canvas(tab.toolbar)
        tab.deleteLater()
        self.tabsWidget.removeTab(index)
        self.compt -= 1

    # handles click on the add tab button
    def buttonClicked(self):
        self.compt += 1
        self.affichage += 1
        name = "Protocol " + str(self.affichage)
        self.addTab(name, self.compt)


# used to perform "by hand" tests on qt
if __name__ == "__main__":
    app = QApplication([])
    app.setApplicationDisplayName("Cyclos")
    app.setStyleSheet("""
		QTabBar::tab {
			background: lightgray;
			color: black;
			border: 0;
			/* min-width: 100px; */
			max-width: 200px;
			/* width: 150px; */
			height: 20px;
			padding: 5px;
		}

		QTabBar::tab:selected {
			background: gray;
			color: white;
		}
	""")
    widget = TabWidget()
    widget.show()
    sys.exit(app.exec_())
