import sys
import markdown2
import os
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *

COLOR_PRIMARY = "#FFECB3"
COLOR_PRIMARY_DARK = "#FFEaB3"
COLOR_PRIMARY_DARKER = "#FFECB3"

class SimpleIo(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.resize(280, 290)
        self.layout = QVBoxLayout(self)
        self.controlBar = MyBar(self)
        self.editLayout = QPlainTextEdit(self)
        self.displayLayout = QWebEngineView(self)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setStyleSheet('''QWidget {background: [COLOR_PRIMARY]; }
                QPlainTextEdit { padding: 10, 5, 10; border: 0px; }'''.replace("[COLOR_PRIMARY]", COLOR_PRIMARY))
        self.editLayout.setFont(QFont("Segoe UI", 11))

        self.layout.addWidget(self.controlBar)
        self.layout.addWidget(self.editLayout)
        self.layout.addWidget(self.displayLayout)

        self.markdown = markdown2.Markdown()
        self.css = open(os.path.join("css", "default.css")).read().replace("[COLOR_PRIMARY]", COLOR_PRIMARY)
        self.installEventFilter(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            print("widget window has gained focus")
            self.editLayout.show()
            self.displayLayout.hide()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            print("widget window has lost focus")
            note = self.editLayout.toPlainText()
            htmlNote = self.getStyledPage(note)
            # print(note)
            self.editLayout.hide()
            self.displayLayout.show()
            # print(htmlNote)
            self.displayLayout.setHtml(htmlNote)
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

class MyBar(QWidget):
    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        btn_size = 35

        self.titleBar = QLabel(self)
        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)

        self.btn_min = QPushButton("+")
        self.btn_min = QPushButton("+")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)

        self.btn_max = QPushButton("+")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)

        self.setStyleSheet("background: {};".format(COLOR_PRIMARY_DARK))

        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.titleBar)

        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()

if __name__=="__main__":
    app = QApplication(sys.argv)
    mw = SimpleIo()
    mw.show()
    sys.exit(app.exec_())