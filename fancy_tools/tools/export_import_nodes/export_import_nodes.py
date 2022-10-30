# TODO: add library feature
# TODO: viewport screengrab
# TODO: better ui


from logging import RootLogger
from operator import iconcat
import os, sys
from turtle import screensize
from fancy_tools.utils import export_nodes

import importlib
importlib.reload(export_nodes)

from hutil.Qt.QtUiTools import QUiLoader
from hutil.Qt.QtWidgets import QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit, QListWidgetItem
from hutil.Qt.QtCore import QFile, QIODevice, Qt, QSize
from hutil.Qt.QtGui import QIcon

class export_import_nodes(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, Qt.WindowStaysOnTopHint)

        self.file_path = ""
        self.existing_snippets = []

        #Get ui file path
        root_dir = os.path.realpath(__file__)
        file_name, file_extension = os.path.splitext(root_dir)
        ui_path = os.path.join(os.path.dirname(root_dir), file_name) + '_new.ui'

        # LOAD UI
        self.ui = QUiLoader().load(ui_path, parentWidget=self)

        # Top-level layout for panels/qwidget
        self.layout = QVBoxLayout(self)
        #self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.ui)

        self.snippet_view = self.ui.listWidget

        self.resize(self.ui.size().width(), self.ui.size().height())


        #Add snippets


        #Link buttons to functions
        self.ui.toolButton_filepath.clicked.connect(self.get_file_path)

        self.ui.pushButton_export.clicked.connect(self.export_nodes)
        #self.ui.pushButton_import.clicked.connect(self.import_nodes)

    def get_file_path(self):
        file_path = QFileDialog.getExistingDirectory(self, 'Select Folder') #getExistingDirectory, getOpenFileName
        self.file_path = file_path
        self.ui.lineEdit_filepath.setText(self.file_path)

        #put all snippets in list
        self.existing_snippets = [name for name in os.listdir(file_path) if os.path.isdir(os.path.join(file_path,name))]

        for snippet in self.existing_snippets:
            icon_path = os.path.join(file_path, snippet)+"/{}.jpg".format(snippet)
            print(icon_path)
            item = QListWidgetItem(snippet)
            #item.setSizeHint(QSize(200,200))
            item.setIcon(QIcon(icon_path))
            self.snippet_view.addItem(item)



    def export_nodes(self):
        snippet_path, screengrab_path = self.prepare_export(self.file_path)

        #CHeck if folder exists
        #TODO: check if snippet already exists, if it does, ask if user wants to overwrite
        folder_path = os.path.dirname(snippet_path)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        export_nodes.export_nodes(snippet_path)
        export_nodes.export_screengrab(screengrab_path)
        print("export complete")

    def import_nodes(self):
        export_nodes.import_nodes(self.file_path)

    def prepare_export(self, path):
        snippet_name = self.ui.lineEdit_export_name.text()
        snippet_path = "{}/{}/{}.cpio".format(path,snippet_name, snippet_name)
        screengrab_path = "{}/{}/{}.jpg".format(path,snippet_name, snippet_name)

        #print("path: {}, snippet_name: {}, snippet_path: {}, screengrab_path: {}".format(path, snippet_name, snippet_path, screengrab_path))

        return snippet_path, screengrab_path