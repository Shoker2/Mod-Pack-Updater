# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Shoker2/Desktop/modpack_updater/app/ui/settings_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class UI_Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("Settings")
        self.resize(500, 100)
        self.GeneralScrollArea = QtWidgets.QScrollArea(self)
        self.GeneralScrollArea.setGeometry(QtCore.QRect(0, 0, 651, 171))
        self.GeneralScrollArea.setWidgetResizable(True)
        self.GeneralScrollArea.setObjectName("GeneralScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 649, 169))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.serverEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverEdit.sizePolicy().hasHeightForWidth())
        self.serverEdit.setSizePolicy(sizePolicy)
        self.serverEdit.setObjectName("serverEdit")
        self.horizontalLayout_2.addWidget(self.serverEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.GeneralScrollArea.setWidget(self.scrollAreaWidgetContents)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.selcetFolderButton.clicked.connect(self.selectFolderButtonClicked)
        self.folderEdit.textChanged.connect(self.folderEditEvent)
        self.serverEdit.textChanged.connect(self.serverEditEvent)

        self.setWindowTitle("Настройки")
        self.selcetFolderButton.setText("Выбрать")
    
    def resizeEvent(self, event):
        self.GeneralScrollArea.setGeometry(0, 0, self.size().width(), self.size().height())
        return super().resizeEvent(event)
    
    def selectFolder(self):
        way = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку')
        return way
    
    def selectFolderButtonClicked(self):
        way = self.selectFolder()
        if way != "":
            self.folderEdit.setText(way)

    def folderEditEvent(self):
        print(self.folderEdit.text())
    
    def serverEditEvent(self):
        print(self.serverEdit.text())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_Settings()
    ui.show()
    sys.exit(app.exec_())
