import sys
import os

from fancy_tools.utils import fileContentReplace as fcp
from fancy_tools.utils import find_subfiles as fs

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit
from PySide6.QtCore import QFile, QIODevice, Qt

class FindAndReplace(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)


        #new blah
        #Initialize vars
        self.file_input = ""
        self.find_input = ""
        self.replace_input = ""

        #Get ui file path
        root_dir = os.path.dirname(__file__)
        ui_path = os.path.join(root_dir, os.path.basename(root_dir)) + '.ui'

        # Load .ui file
        self.ui = QUiLoader().load(ui_path, parentWidget=self)

        # Top-level layout for panels/qwidget
        self.layout = QVBoxLayout(self)
        #self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ui)

        #Link buttons to functions
        self.ui.toolButton_file_browse.clicked.connect(self.getFolder)
        self.ui.pushButton_run.clicked.connect(self.runTool)


        #self.resize(self.ui.size().width(), self.ui.size().height())

    def runTool(self):
        #Get all inputs
        self.getInputs()

        found_files = fs.findFiles(self.folder_path.strip(), self.file_input.strip())
        print(found_files)
        files_renamed = fcp.replace(found_files, self.find_input, self.replace_input)
        self.printLog(files_renamed)


    def getFolder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.ui.lineEdit_path.setText(self.folder_path)


    def getInputs(self):
        print("Getting inputs")
        self.folder_path = self.ui.lineEdit_path.text()
        print(self.folder_path)
        self.file_input = self.ui.lineEdit_file_name.text()
        print(self.file_input)
        self.find_input = self.ui.lineEdit_find_word.text()
        self.replace_input = self.ui.lineEdit_replace_word.text()
        print(self.file_input,self.find_input,self.replace_input)

    def printLog(self, value):
        self.ui.lineEdit_log.setText("{} files changed".format(str(value)))

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    window = FindAndReplace()
    window.show()

    sys.exit(app.exec())