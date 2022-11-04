import os
import sys

from PySide6 import QtWidgets, QtCore


def bootstrap():
    this_dir = os.path.dirname(__file__) # menu
    parent_dir = os.path.dirname(this_dir) # callbacks
    grand_parent_dir = os.path.dirname(parent_dir) # fancy_tools
    grand_grand_parent_dir = os.path.dirname(grand_parent_dir) # henrik-tools

    if not grand_grand_parent_dir in sys.path:
        sys.path.insert(0, grand_grand_parent_dir)


def bootstrap_dynamic():
    target_module = 'fancy_tools'
    this_path = __file__.replace('\\', '/')
    containing_folder, _ = this_path.split('/{}/'.format(target_module))

    if not containing_folder in sys.path:
        print('Bootstrapping {}'.format(containing_folder))
        sys.path.insert(0, containing_folder)


def main():
    from fancy_tools.tools import find_replace

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    window = find_replace.FindAndReplace()
    window.show()

    sys.exit(app.exec())


# TODO: Implement argparse -> https://docs.python.org/3/library/argparse.html
if __name__ == "__main__":
    bootstrap_dynamic()
    main()
