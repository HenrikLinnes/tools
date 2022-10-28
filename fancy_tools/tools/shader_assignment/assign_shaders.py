from logging import RootLogger
import os, sys
import hou
import json

from hutil.Qt.QtUiTools import QUiLoader
from hutil.Qt.QtWidgets import QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit
from hutil.Qt.QtCore import QFile, QIODevice, Qt

class Assign_Shaders(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, Qt.WindowStaysOnTopHint)

        #print("INITIALIZING..")
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

        self.resize(self.ui.size().width(), self.ui.size().height())

        #Link buttons to functions
        self.ui.toolButton_file_path.clicked.connect(self.getFolder)
        self.ui.pushButton_run.clicked.connect(self.run)


    def run(self):
        self.getInputs()
        self.populate_library()


    def populate_library(self):

        #TODO: change to also run when line edit is updated
        with open(self.file_path, 'r') as openfile:
            json_read = json.load(openfile)

        matlib_node = hou.node(self.matlib_input)
        matlib_node.parm("materials").set(len(json_read))

        idx=1
        for key, value in json_read.items():
            new_value = []
            for item in value:
                item = "{}{}{}".format(self.get_asset(), "/Root/RootOffset", item)
                new_value.append(item)
            value_str = " ".join(new_value)
            value_str = value_str.replace("|", "/")
            matlib_node.parm("matnode{}".format(idx)).set(key)
            matlib_node.parm("matpath{}".format(idx)).set(key)
            matlib_node.parm("geopath{}".format(idx)).set(value_str)
            idx += 1

    def get_asset(self):
        asset = self.asset_input.split("/g_geometry")[0]
        return asset

    def getFolder(self):
        self.file_path = QFileDialog.getOpenFileName(self, 'Select File')
        self.ui.lineEdit_file_path.setText(self.file_path[0])


    def getInputs(self):
        self.file_path = self.ui.lineEdit_file_path.text()
        self.matlib_input = self.ui.lineEdit_matlib.text()
        self.asset_input = self.ui.lineEdit_asset.text()

'''
if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    window = Assign_Shaders()
    window.show()

    sys.exit(app.exec())

'''