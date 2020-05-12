# -*- coding: utf-8 -*-

from src.IHM_Qt.Cyclos import TabWidget
from PySide2.QtWidgets import QApplication
import sys
from PySide2.QtGui import QIcon


class Window(TabWidget):
    def __init__(self):
        super().__init__()
        self.setIcon()

    def setIcon(self):
        appIcon = QIcon("./Cyclos.png")
        self.setWindowIcon(appIcon)


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
    windows = Window()
    windows.show()
    sys.exit(app.exec_())
