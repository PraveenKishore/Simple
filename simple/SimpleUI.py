from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, uic
import sys
import os
import markdown2 # https://github.com/trentm/python-markdown2
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont

simpleUiForm = uic.loadUiType("Simple.ui")[0]

class SimpleWindow(QtWidgets.QMainWindow, simpleUiForm):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.markdown = markdown2.Markdown()
        self.css = open(os.path.join("css", "default.css")).read()
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
            htmlNote = self.getStyledPage(note)
            # print(note)
            self.editNote.hide()
            self.displayNote.show()
            # print(htmlNote)
            self.displayNote.setHtml(htmlNote)
        elif event.type() == QtCore.QEvent.FocusIn:
            print("widget has gained keyboard focus")
        elif event.type() == QtCore.QEvent.FocusOut:
            print("widget has lost keyboard focus")
        return False

    def getStyledPage(self, inputText):
        output = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <style type="text/css">
        """
        output += self.css
        output += """</style>
            </head>
        <body>"""
        output += self.markdown.convert(inputText)
        output += """</body>
        </html>"""
        return output

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setFont(QFont("resources/Geomanist-Regular.otf", 12, QFont.Normal))
    simpleWindow = SimpleWindow()
    simpleWindow.show()
    sys.exit(app.exec_())