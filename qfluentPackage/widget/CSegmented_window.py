# -*- coding: utf-8 -*-
# @Time: 2023/12/30
# @Author: Administrator
# @File: CSegmented_window.py
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from qfluentwidgets import SegmentedWidget

__all__ = ['CSegmentedWidget']

from qfluentPackage.common.encryption import md5


class CSegmentedWidget(QWidget):
    subInterfaceAdded = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.addWidget(self.pivot)
        self.addWidget(self.stackedWidget)
        self.stackedWidget.currentChanged.connect(self._onCurrentIndexChanged)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)

    def addWidget(self, widget: QWidget):
        self.vBoxLayout.addWidget(widget)

    def setDefaultCurrent(self, widget: QWidget):
        self.stackedWidget.setCurrentWidget(widget)
        if not widget.objectName():
            raise ValueError('要设置objectName')
        self.pivot.setCurrentItem(widget.objectName())

    def addSubInterface(self, widget: QWidget, text, objectName, insert_index: int = None):
        widget.setObjectName(md5((str(objectName))))
        self.stackedWidget.addWidget(widget)
        keyword = {
            'routeKey': widget.objectName(),
            'text': text,
            'onClick': lambda: self.stackedWidget.setCurrentWidget(widget),
        }
        if insert_index is None:
            self.pivot.addItem(**keyword)
        else:
            keyword['index'] = insert_index
            self.pivot.insertItem(**keyword)
        self.subInterfaceAdded.emit(text, widget.objectName())

    def _onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

    def getItemsNum(self):
        return len(self.pivot.items)
