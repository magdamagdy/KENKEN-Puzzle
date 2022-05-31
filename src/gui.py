from PyQt5 import QtCore, QtGui, QtWidgets
from time import time
from draw_kenken import kenken_draw
from csp_algorithms import kenken_solver
from KenKen_Game import kenken_data,kenken_generator
import pygame


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(200, 60, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(200, 130, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 210, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 60, 91, 21))#55, 16
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 130, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.start_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "3*3"))
        self.comboBox.setItemText(1, _translate("MainWindow", "4*4"))
        self.comboBox.setItemText(2, _translate("MainWindow", "5*5"))
        self.comboBox.setItemText(3, _translate("MainWindow", "6*6"))
        self.comboBox.setItemText(4, _translate("MainWindow", "7*7"))
        self.comboBox.setItemText(5, _translate("MainWindow", "8*8"))
        self.comboBox.setItemText(6, _translate("MainWindow", "9*9"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Backtrack"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Forward Checking"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Arc Consistency"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Size"))
        self.label_2.setText(_translate("MainWindow", "Algorithm"))

    def start_button(self):
        # empty_curr_domains()
        board_size = self.comboBox.currentText()
        board_size = int(board_size[0])
        Algorithm = self.comboBox_2.currentText()

        print("size",board_size,type(board_size))
        print("algo",Algorithm)
        ken = kenken_generator(board_size)
        gen_cages = ken.generate_kenken()
        # print(type(gen_cages))
        ken_data = kenken_data()
        domains = ken_data.kenken_domains(board_size, gen_cages)
        neighbors_cages = ken_data.get_neighbors_cages(gen_cages)
        variables = ken_data.get_variables(gen_cages)
        # print(type(domains),type(neighbors_cages),type(variables))
        ken_board=kenken_draw(board_size)

        ken_solver = kenken_solver()

        if(Algorithm=='Backtrack'):
            t1 = time()
            assignment = ken_solver.backtracking_search(variables,domains,neighbors_cages)
            print("assignemnt_bk",assignment)
            t2 = time()
            print("Time_of_BK",t2-t1)
            ken_board.draw(assignment,gen_cages)
        elif(Algorithm=='Forward Checking'):
            t1 = time()
            assignment = ken_solver.backtracking_search(variables,domains,neighbors_cages, inference="fc")
            print("assignemnt_fc",assignment)
            t2 = time()
            print("Time_of_FC",t2-t1)
            ken_board.draw(assignment,gen_cages)
        elif(Algorithm=='Arc Consistency'):
            t1 = time()
            assignment = ken_solver.backtracking_search(variables,domains,neighbors_cages, inference="arc")
            print("assignemnt_ARC_C",assignment)
            t2 = time()
            print("Time_of_ARC_C",t2-t1)
            ken_board.draw(assignment,gen_cages)
        else:
            print("no algorithm has been chosen")
        
        run=True
        while run:
            # Loop through the events stored in event.get()
            for event in pygame.event.get():
                # Quit the game window
                if event.type == pygame.QUIT:
                    run = False
        # Quit pygame window
        pygame.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
