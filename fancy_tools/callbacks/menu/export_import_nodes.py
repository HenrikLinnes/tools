from fancy_tools.tools.export_import_nodes import export_import_nodes
import importlib

window_instance = None

def show():
    global window_instance

    importlib.reload(export_import_nodes)
    window_instance = export_import_nodes.export_import_nodes()

    window_instance.show()

