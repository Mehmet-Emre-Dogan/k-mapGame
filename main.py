import sys
from json import load
from random import randint
from collections import defaultdict
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore 
from PyQt5 import QtGui

from functools import partial

from mainGui import Ui_mainWindow

wordArr = []
DEBUG = True
MAX_TRIALS = 6

STYLE_SHEET_STR = """
*:disabled {
	background-color:rgb(30, 30, 30);	
	color: rgb(127, 127, 127);
}
*{
	background-color: rgb(90, 90, 90);
	color: white;
}
"""

    
class myWindow(QtWidgets.QMainWindow):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('img.png'))
        self.ui.widget.setObjectName("table")
        self.ui.widget.setStyleSheet("""QWidget#table {background-image: url(./bg.png); background-position: center; background-repeat: no-repeat; }""")
        self.minterms = {}
        # self.ui.btn0.objectName()
        buttons = self.ui.widget.findChildren(QtWidgets.QPushButton)
        for button in buttons:
            # foo = lambda btn = button : btn.setText( str(int(not int(btn.text()))) )
            # https://stackoverflow.com/questions/11723217/python-lambda-doesnt-remember-argument-in-for-loop

            self.minterms.update({button.objectName(): int(button.text())}) # initialize minterm array

            def foo(btn):
                newVal = int(not int(btn.text()))
                btn.setText( str(newVal) )
                self.minterms.update({btn.objectName(): newVal}) # update minyterm array
                if DEBUG:
                    print(self.minterms)

            foo2 = partial(foo, button)
            button.clicked.connect(foo2)
            

    def infoMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText("Tamam")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def warningMessage(self, title="Info", text="Text text"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText("Tamam")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def errorMessage(self, title="Error", text="An error occured"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        btnOk = msg.button(QMessageBox.Ok)
        btnOk.setText("Tamam")
        msg.setStyleSheet(STYLE_SHEET_STR)
        msg.exec_()

    def confirmationMsg(self, title="Question", text="Are you sure doing xyz?"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setWindowIcon(QtGui.QIcon('img.png'))
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        btnYes = msg.button(QMessageBox.Yes)
        btnYes.setText("Evet")
        btnNo = msg.button(QMessageBox.No)
        btnNo.setText("Hayır")
        msg.setStyleSheet(STYLE_SHEET_STR)
        answer = msg.exec_()
        return answer == QMessageBox.Yes

    def game(self):
        try:
            if self.play(self.word):
                self.infoMessage(title="Kazandınız", text=f"{self.word} kelimesini başarıyla buldunuz.")
                if self.confirmationMsg(title="Wordle", text="Tekrar oynamak ister misiniz?"):
                    self.initApp()
                else:
                    sys.exit()
            elif self.attemptCou < MAX_TRIALS:
                self.userStr = ""
            elif self.attemptCou >= MAX_TRIALS:
                self.errorMessage(title="Kaybettiniz", text=f"Seçilen kelime: {self.word} idi.")
                if self.confirmationMsg(title="Wordle", text="Tekrar oynamak ister misiniz?"):
                    self.initApp()
                else:
                    sys.exit()
        except Exception as ex:
            self.errorMessage(text=str(ex))

def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = myWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app()