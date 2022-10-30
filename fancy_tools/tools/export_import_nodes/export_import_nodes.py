from logging import RootLogger
import os, sys
from fancy_tools.utils import export_nodes

import importlib
importlib.reload(export_nodes)

from hutil.Qt.QtUiTools import QUiLoader
from hutil.Qt.QtWidgets import QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit
from hutil.Qt.QtCore import QFile, QIODevice, Qt

class export_import_nodes(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, Qt.WindowStaysOnTopHint)

        self.file_path = ""

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
        self.ui.toolButton_filepath.clicked.connect(self.get_file_path)

        self.ui.pushButton_export.clicked.connect(self.export_nodes)
        self.ui.pushButton_import.clicked.connect(self.import_nodes)

    def get_file_path(self):
        file_path = QFileDialog.getOpenFileName(self, 'Select File')
        self.file_path = file_path[0]
        self.ui.lineEdit_filepath.setText(self.file_path)

    def export_nodes(self):
        export_nodes.export_nodes(self.file_path)

    def import_nodes(self):
        export_nodes.import_nodes(self.file_path)