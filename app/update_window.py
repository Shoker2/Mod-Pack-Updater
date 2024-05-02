# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Shoker2/Desktop/Pomariol Launcher/Resourses/ui/update_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_Update(QMainWindow):
    progressBarSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("Update")
        self.resize(500, 150)
        self.GeneralScrollArea = QtWidgets.QScrollArea(self)
        self.GeneralScrollArea.setGeometry(QtCore.QRect(10, 10, 531, 261))
        self.GeneralScrollArea.setWidgetResizable(True)
        self.GeneralScrollArea.setObjectName("GeneralScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 259))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.modpacksComboBox = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.modpacksComboBox.setObjectName("modpacksComboBox")
        self.verticalLayout_2.addWidget(self.modpacksComboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.folderEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.folderEdit.setObjectName("folderEdit")
        self.horizontalLayout.addWidget(self.folderEdit)
        self.selcetFolderButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.selcetFolderButton.setObjectName("selcetFolderButton")
        self.horizontalLayout.addWidget(self.selcetFolderButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.updateButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.updateButton.setFont(font)
        self.updateButton.setObjectName("updateButton")
        self.verticalLayout_2.addWidget(self.updateButton)
        self.progressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.GeneralScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.setWindowTitle("Обновление сборки")
        self.updateButton.setText("Обновить")
        self.selcetFolderButton.setText("Выбрать")
        self.folderEdit.setToolTip("Папка с модами")

        self.progressBar.setTextVisible(False)
    
        self.progressBarSignal.connect(self.progressBarSignalEvent)
        self.selcetFolderButton.clicked.connect(self.selectFolderButtonClicked)
        self.updateButton.clicked.connect(self.updateButtonClicked)
        self.folderEdit.textChanged.connect(self.folderEditEvent)

        self.progressBarSignal.emit(0)
    
    def resizeEvent(self, event):
        self.GeneralScrollArea.setGeometry(0, 0, self.size().width(), self.size().height())
        return super().resizeEvent(event)
    
    def progressBarSignalEvent(self, value):
        self.progressBar.setValue(value)

    def selectFolder(self):
        way = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        return way
    
    def selectFolderButtonClicked(self):
        way = self.selectFolder()
        if way != "":
            self.folderEdit.setText(way)

    def folderEditEvent(self):
        print(self.folderEdit.text())
    
    def updateButtonClicked(self):
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_Update()
    ui.show()

    sys.exit(app.exec_())