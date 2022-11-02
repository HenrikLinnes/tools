# TODO: add library feature
# TODO: viewport screengrab
# TODO: better ui


from logging import RootLogger
from operator import iconcat
import os, sys, hou
from turtle import screensize
from fancy_tools.utils import export_nodes, flow_layout

import importlib

from symbol import flow_stmt
importlib.reload(export_nodes)

from hutil.Qt.QtUiTools import QUiLoader
from hutil.Qt.QtWidgets import QWidget, QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit, QListWidgetItem, QToolButton
from hutil.Qt.QtCore import QFile, QIODevice, Qt, QSize
from hutil.Qt.QtGui import QIcon

class export_import_nodes(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, Qt.WindowStaysOnTopHint)

        #Library paths
        #TODO: Make dynamic dropdown
        asset_paths = [r"T:\assetLibrary\houdini_assets\NodeSnippet", r"T:\assetLibrary\houdini_assets\LightRigs"]

        selected_library = r"T:/assetLibrary/houdini_assets/NodeSnippet"
        self.file_path = selected_library

        # populate assets from default asset library
        self.current_assets = {}
        self.update_current_assets(selected_library)


        #Get ui file path
        root_dir = os.path.realpath(__file__)
        file_name, file_extension = os.path.splitext(root_dir)
        ui_path = os.path.join(os.path.dirname(root_dir), file_name) + '_new.ui'

        # Load UI and apply houdini stylesheet
        self.ui = QUiLoader().load(ui_path, parentWidget=self)

        stylesheet = hou.qt.styleSheet()
        self.setStyleSheet(stylesheet)

        # Top-level layout for panels/qwidget
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.addWidget(self.ui)

        #Qt bindings
        self.asset_area = self.ui.asset_area
        self.asset_lib = self.ui.comboBox_asset_path

        self.asset_lib.addItems(asset_paths)

        # setup for flow layout
        self.widget = QWidget()
        self.asset_area.setWidget(self.widget)

        asset_view = flow_layout.FlowLayout(self.widget)

        # define misc vars
        thumbnail_size = 100

        #Fill FlowLayout with current items
        for idx, asset_name in enumerate(self.current_assets["asset_name"]):
            print("hello: ", asset_name, self.current_assets["icon_path"][idx], self.current_assets["cpio_path"][idx] )
            asset_item = QToolButton()
            asset_item.setIcon(QIcon(self.current_assets["icon_path"][idx]))
            asset_item.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            asset_item.setIconSize(QSize(thumbnail_size, thumbnail_size))
            asset_item.setFixedSize(QSize(thumbnail_size*1.3, thumbnail_size*1.3))
            asset_item.setText(self.current_assets["asset_name"][idx])
            asset_item.setObjectName(self.current_assets["asset_name"][idx])
            asset_view.addWidget(asset_item)
            asset_item.clicked.connect(self.asset_clicked)

        #Resize cuz otherwise the shit wont show
        self.resize(self.ui.size().width(), self.ui.size().height())

        #Link buttons to functions
        # self.ui.pushButton_import.clicked.connect(self.import_nodes)
        # self.ui.toolButton_filepath.clicked.connect(self.get_file_path)
        self.ui.pushButton_export.clicked.connect(self.export_nodes)


    def asset_clicked(self, asset_name):
        print(self.sender().objectName())

    # def get_file_path(self):
    #     file_path = QFileDialog.getExistingDirectory(self, 'Select Folder') #getExistingDirectory, getOpenFileName
    #     self.file_path = file_path
    #     self.ui.lineEdit_filepath.setText(self.file_path)


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

    def update_current_assets(self, library_path):
        # Get all folders in path
        assets = [name for name in os.listdir(library_path) if os.path.isdir(os.path.join(library_path,name))]
        name_list = []
        icon_list = []
        cpio_list = []
        # Get sub files and store in dict
        for asset in assets:
            name_list.append(asset)
            icon_list.append(os.path.join(library_path, asset)+"/{}.jpg".format(asset))
            cpio_list.append(os.path.join(library_path, asset)+"/{}.cpio".format(asset))
        self.current_assets["asset_name"] = name_list
        self.current_assets["icon_path"] = icon_list
        self.current_assets["cpio_path"] = cpio_list

    # old shait
    def update_snippet_view(self):
        #put all snippets in list
        self.existing_snippets = [name for name in os.listdir(self.file_path) if os.path.isdir(os.path.join(self.file_path,name))]
        print(self.existing_snippets)
        for snippet in self.existing_snippets:
            icon_path = os.path.join(self.file_path, snippet)+"/{}.jpg".format(snippet)
            item = QToolButton()
            item.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            item.setIconSize(QSize(200,200))
            item.setFixedSize(QSize(200,200))
            item.setText(snippet)

            #item = QListWidgetItem(snippet)
            #item.setSizeHint(QSize(200,200))
            #item.setIcon(QIcon(icon_path))
            self.snippet_view.addWidget(item)

            item.clicked.connect(self.clicked)