from logging import RootLogger
import os, sys
import hou
import json

from hutil.Qt.QtUiTools import QUiLoader
from hutil.Qt.QtWidgets import QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit
from hutil.Qt.QtCore import QFile, QIODevice, Qt

class Assign_Shaders(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        print("INITIALIZING..")
        self.json_file = ""

        #Get ui file path
        root_dir = os.path.realpath(__file__)
        file_name, file_extension = os.path.splitext(root_dir)
        ui_path = os.path.join(os.path.dirname(root_dir), file_name) + '.ui'

        # LOAD UI
        self.ui = QUiLoader().load(ui_path, parentWidget=self)

        # Top-level layout for panels/qwidget
        self.layout = QVBoxLayout(self)
        #self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ui)

        #Link buttons to functions
        self.ui.toolButton_file_path.clicked.connect(self.getFolder)
        self.ui.pushButton_run.clicked.connect(self.run)


    def run(self):
        self.getInputs()

        print("running")
        matlib_node = hou.node(self.matlib_input)

        with open(self.file_path, 'r') as openfile:
            json_read = json.load(openfile)

        matlib_node.parm("materials").set(len(json_read))

        idx=1
        for key, value in json_read.items():
            value_str = " ".join(value)
            value_str = value_str.replace("|", "/")
            matlib_node.parm("matnode{}".format(idx)).set(key)
            matlib_node.parm("matpath{}".format(idx)).set(key)
            matlib_node.parm("geopath{}".format(idx)).set(value_str)
            idx += 1

    def getFolder(self):
        self.file_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.ui.lineEdit_file_path.setText(self.folder_path)


    def getInputs(self):
        print("Getting inputs")
        self.file_path = self.ui.lineEdit_file_path.text()
        self.matlib_input = self.ui.lineEdit_matlib.text()