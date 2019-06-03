from PySide2.QtCore import QBuffer, QByteArray, QFile
from PySide2.QtUiTools import QUiLoader

from hexrd import importlib_resources

from .image_canvas import ImageCanvas
from .image_tab_widget import ImageTabWidget
from .menu_bar import MenuBar
from .status_bar import StatusBar

import hexrd.resources.ui

class UiLoader(QUiLoader):
    def __init__(self, parent=None):
        super(UiLoader, self).__init__(parent)

        self.registerCustomWidget(ImageCanvas)
        self.registerCustomWidget(ImageTabWidget)
        self.registerCustomWidget(MenuBar)
        self.registerCustomWidget(StatusBar)

    def load_file(self, file_name, parent=None):
        """Load a UI file and return the widget

        Returns a widget created from the UI file.

        :param file_name: The name of the ui file to load (must be located
                          in hexrd.resources.ui).
        """
        text = importlib_resources.read_text(hexrd.resources.ui, file_name)
        return self.load_string(text, parent)

    def load_string(self, string, parent=None):
        """Load a UI file from a string and return the widget"""
        data = QByteArray(string.encode('utf-8'))
        buf = QBuffer(data)
        return self.load(buf, parent)
