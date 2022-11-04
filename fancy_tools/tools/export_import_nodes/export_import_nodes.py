# TODO: add library feature : WIP
# TODO: viewport screengrab : DONE
# TODO: better ui : WIP
# TODO: load thumbnails in threads to prevent houdini from being blocked ( if possible )

import os, sys, hou
import importlib

from fancy_tools.utils import export_nodes, flow_layout
importlib.reload(export_nodes)

from hutil.Qt.QtUiTools import QUiLoader
from hutil.Qt.QtWidgets import QWidget, QApplication, QDialog, QVBoxLayout, QFileDialog, QLineEdit, QListWidgetItem, QToolButton
from hutil.Qt.QtCore import QFile, QIODevice, Qt, QSize
from hutil.Qt.QtGui import QIcon

class export_import_nodes(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, Qt.WindowStaysOnTopHint)

        # HARD CODED PATHS
        #TODO: Make dynamic dropdown, hard coded for now
        asset_paths = [r"T:\assetLibrary\houdini_assets\NodeSnippet", r"T:\assetLibrary\houdini_assets\LightRigs"]

        #Get ui file path
        root_dir = os.path.realpath(__file__)
        file_name, file_extension = os.path.splitext(root_dir)
        ui_path = os.path.join(os.path.dirname(root_dir), file_name)+".ui"

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
        self.asset_lib_list = self.ui.comboBox_asset_path

        # setup for flow layout
        self.widget = QWidget()
        self.asset_area.setWidget(self.widget)

        asset_view = flow_layout.FlowLayout(self.widget)

        # Populate asset library dropdown
        self.asset_lib_list.addItems(asset_paths)

        # Get current assete_library value
        selected_library = self.asset_lib_list.currentText()
        # self.file_path = selected_library

        # populate assets from default asset library
        self.current_assets = {}
        self.update_asset_dict(selected_library)

        # TODO: add support for different thumbnail sizes
        # define thumbnail size used in gui
        thumbnail_size = 100

        #Fill FlowLayout with current items
        # TODO: Wrap into function and recall it when library is changed or new assets are exported
        for asset in self.current_assets.keys():
            asset_item = QToolButton()
            asset_item.setIcon(QIcon(self.current_assets[asset]["icon_path"]))
            asset_item.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            asset_item.setIconSize(QSize(thumbnail_size, thumbnail_size))
            asset_item.setFixedSize(QSize(thumbnail_size*1.3, thumbnail_size*1.3))
            asset_item.setText(self.current_assets[asset]["asset_name"])
            asset_item.setObjectName(self.current_assets[asset]["asset_name"])
            asset_view.addWidget(asset_item)
            asset_item.clicked.connect(self.import_nodes)

        #Resize cuz otherwise the shit wont show
        self.resize(self.ui.size().width(), self.ui.size().height())

        #Link buttons to functions
        self.ui.pushButton_export.clicked.connect(self.export_nodes)

    def export_nodes(self):
        snippet_path, screengrab_path = self.prepare_export(self.asset_lib_list.currentText())
        #CHeck if folder exists
        #TODO: check if snippet already exists, if it does, ask if user wants to overwrite
        folder_path = os.path.dirname(snippet_path)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        export_nodes.export_nodes(snippet_path)
        export_nodes.export_screengrab(screengrab_path)
        print("export complete")

    def import_nodes(self):
        cpio_path = self.current_assets[self.sender().objectName()]["cpio_path"]
        export_nodes.import_nodes(cpio_path)

    def prepare_export(self, path):
        snippet_name = self.ui.lineEdit_export_name.text()
        snippet_path = "{}/{}/{}.cpio".format(path,snippet_name, snippet_name)
        screengrab_path = "{}/{}/{}.jpg".format(path,snippet_name, snippet_name)

        #print("path: {}, snippet_name: {}, snippet_path: {}, screengrab_path: {}".format(path, snippet_name, snippet_path, screengrab_path))
        return snippet_path, screengrab_path

    #TODO: test using nested dict
    def update_asset_dict(self, library_path):
        # Get all folders in path
        assets = [name for name in os.listdir(library_path) if os.path.isdir(os.path.join(library_path,name))]

        for idx in range (len(assets)):
            self.current_assets[assets[idx]] = {}
            self.current_assets[assets[idx]]["asset_name"] = assets[idx]
            self.current_assets[assets[idx]]["icon_path"] = os.path.join(library_path, assets[idx])+"/{}.jpg".format(assets[idx])
            self.current_assets[assets[idx]]["cpio_path"] = os.path.join(library_path, assets[idx])+"/{}.cpio".format(assets[idx])
