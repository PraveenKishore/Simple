from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, uic
import sys
import os
import markdown2 # https://github.com/trentm/python-markdown2
from PyQt5.QtCore import QRect

simpleUiForm = uic.loadUiType("Simple.ui")[0]

class SimpleWindow(QtWidgets.QMainWindow, simpleUiForm):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.markdown = markdown2.Markdown()
        self.editNote.setPlainText("")
        #self.noteView = QtWebEngineWidgets.QWebEngineView(self)
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            print("widget window has gained focus")
            self.editNote.show()
            self.displayNote.hide()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            print("widget window has lost focus")
            note = self.editNote.toPlainText()
            htmlNote = self.markdown.convert(note)
            # print(note)
            self.editNote.hide()
            self.displayNote.show()
            self.displayNote.setHtml(htmlNote)
        elif event.type() == QtCore.QEvent.FocusIn:
            print("widget has gained keyboard focus")
        elif event.type() == QtCore.QEvent.FocusOut:
            print("widget has lost keyboard focus")
        return False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    simpleWindow = SimpleWindow()
    simpleWindow.show()
    sys.exit(app.exec_())