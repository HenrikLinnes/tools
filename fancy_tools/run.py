import os
import sys

from PySide6 import QtWidgets, QtCore


def bootstrap():
    this_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(this_dir)

    if not parent_dir in sys.path:
        sys.path.insert(0, parent_dir)


def main():
    from fancy_tools.tools import find_replace

    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    window = find_replace.FindAndReplace()
    window.show()

    sys.exit(app.exec())


# TODO: Implement argparse -> https://docs.python.org/3/library/argparse.html
if __name__ == "__main__":
    bootstrap()
    main()
