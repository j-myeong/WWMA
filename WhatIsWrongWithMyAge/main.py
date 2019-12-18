import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QToolButton, \
    QSizePolicy, QLabel, QHBoxLayout, QDialog
from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui
from gamedata import PersonData, PersonDataDetail
from imagecheck import FaceAPI

class Button(QToolButton):
    def __init__(self, text, callback):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)
        self.clicked.connect(callback)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.game = PersonData()
        self.game_detail = PersonDataDetail()
        self.col_header_labels = ["Nickname", "1번", "2번", "3번", "4번", "5번", "점수"]
        self.lbl = QLabel(self)
        self.lbl2 = QLabel(self)
        self.sequence = 1
        self.api_play = FaceAPI()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("내 나이가 어때서?")
        self.setGeometry(50, 50, 900, 500)
        self.api_play.setFile("../img/face" + str(self.sequence) + ".jpeg")
        api_gender, api_age = self.api_play.imagecheck()
        self.lbl.resize(400, 400)
        self.lbl2.setMaximumHeight(20)
        self.lbl2.setText("API DATA || Gender = {gender} || Age = {age}".format(gender=api_gender, age=api_age))

        self.pixmap = QPixmap("../img/face" + str(self.sequence) + ".jpeg")
        self.pixmap = self.pixmap.scaledToWidth(400)
        self.lbl.setPixmap(self.pixmap)

        # Make Ranking Table
        self.create_table()

        # Make Buttons
        self.server_button = Button("Load Server Data", self.getData)
        self.quit_button = Button("Quit", quit)
        self.next_button = Button("Next", self.next)
        self.send_button = Button("Send Server Data", self.send)
        self.answer_button = Button("Answer", self.answer)
        self.next_button.setFixedHeight(20)
        self.server_button.setFixedHeight(20)
        self.quit_button.setFixedHeight(20)
        self.send_button.setFixedHeight(20)
        self.answer_button.setFixedHeight(20)

        self.hlayout = QHBoxLayout()

        self.vlayout1 = QVBoxLayout()
        self.vlayout1.addWidget(self.table)
        self.vlayout1.addWidget(self.server_button)
        self.vlayout1.addWidget(self.quit_button)

        self.vlayout2 = QVBoxLayout()
        self.vlayout2.addWidget(self.lbl)
        self.vlayout2.addWidget(self.lbl2)
        self.vlayout2.addWidget(self.answer_button)
        self.vlayout2.addWidget(self.send_button)
        self.vlayout2.addWidget(self.next_button)

        self.hlayout.addLayout(self.vlayout2)
        self.hlayout.addLayout(self.vlayout1)

        self.setLayout(self.hlayout)
        self.show()

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(self.col_header_labels)
        self.table.setColumnWidth(0, 140)
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 40)
        self.table.setColumnWidth(3, 40)
        self.table.setColumnWidth(4, 40)
        self.table.setColumnWidth(5, 40)
        self.table.setColumnWidth(6, 65)

    def getData(self):
        self.game_data = self.game_detail.getGameDataDetail()
        self.game_result = self.game.getGameData()
        print(self.game_data)
        print(self.game_result)
        self.table.setRowCount(len(self.game_data.keys()))
        for i in range(len(self.game_data.keys())):
            nickname = list(self.game_data.keys())[i]
            self.table.setItem(i, 0, QTableWidgetItem(nickname))
            if len(self.game_data[nickname]) == 5:
                self.table.setItem(i, 1, QTableWidgetItem(self.game_data[nickname][0]))
                self.table.setItem(i, 2, QTableWidgetItem(self.game_data[nickname][1]))
                self.table.setItem(i, 3, QTableWidgetItem(self.game_data[nickname][2]))
                self.table.setItem(i, 4, QTableWidgetItem(self.game_data[nickname][3]))
                self.table.setItem(i, 5, QTableWidgetItem(self.game_data[nickname][4]))
                self.table.setItem(i, 6, QTableWidgetItem(str(self.game_result[nickname])))

    def next(self):
        if self.sequence < 5:
            self.sequence += 1
        else:
            self.sequence = 1
        self.pixmap = QPixmap("../img/face" + str(self.sequence) + ".jpeg")
        self.pixmap = self.pixmap.scaledToWidth(400)
        self.lbl.setPixmap(self.pixmap)

        self.api_play.setFile("../img/face" + str(self.sequence) + ".jpeg")
        api_gender, api_age = self.api_play.imagecheck()
        self.lbl2.setText("API DATA || Gender = {gender} || Age = {age}".format(gender=api_gender, age=api_age))

    def send(self):
        self.api_play.sendServer()

    def answer(self):
        answer = [
            ('male', 20),
            ('male', 20),
            ('female', 26),
            ('male', 4),
            ('male', 27),
        ]

        dialog = QDialog()
        dialog.setWindowTitle("Answer")
        dialog.setGeometry(200, 200, 200, 200)
        answer_lbl1 = QLabel()
        answer_lbl2 = QLabel()
        answer_lbl1.setFont(QtGui.QFont('NanumSquare', 40, QtGui.QFont.Bold))
        answer_lbl1.setAlignment(Qt.AlignCenter)
        answer_lbl2.setFont(QtGui.QFont('NanumSquare', 40, QtGui.QFont.Bold))
        answer_lbl2.setAlignment(Qt.AlignCenter)
        answer_lbl1.setText("남자" if answer[self.sequence - 1][0] == "male" else "여자")
        answer_lbl2.setText(str(answer[self.sequence - 1][1]) + "세")
        layout = QVBoxLayout()
        layout.addWidget(answer_lbl1)
        layout.addWidget(answer_lbl2)
        dialog.setLayout(layout)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

