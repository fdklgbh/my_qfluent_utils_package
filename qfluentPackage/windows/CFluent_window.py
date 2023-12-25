# -*- coding: utf-8 -*-
# @Time: 2023/12/24
# @Author: Administrator
# @File: CFluent_window.py
from typing import Union
from abc import abstractmethod
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationTreeWidget, FluentIconBase, qrouter)
from qfluentwidgets.window.fluent_window import FluentWindowBase, FluentTitleBar

__all__ = ['CFluentWindow']


class CFluentWindow(FluentWindowBase):
    """ CFluent window """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(FluentTitleBar(self))

        self.navigationInterface = NavigationInterface(self)
        self.widgetLayout = QHBoxLayout()

        # initialize layout
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.widgetLayout.addWidget(self.stackedWidget)

        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)
        self.titleBar.raise_()

    @abstractmethod
    def initWindow(self):
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()

    @abstractmethod
    def connectSignalToSlot(self):
        """
        信号
        :return:
        """

    @abstractmethod
    def initNavigation(self):
        """
        导航栏
        :return:
        """

    def addSubInterface(self, interface: QWidget, icon: Union[FluentIconBase, QIcon, str], text: str,
                        position=NavigationItemPosition.TOP, parent=None, isTransparent=False) -> NavigationTreeWidget:
        """ add sub interface, the object name of `interface` should be set already
        before calling this method

        Parameters
        ----------
        interface: QWidget
            the subinterface to be added

        icon: FluentIconBase | QIcon | str
            the icon of navigation item

        text: str
            the text of navigation item

        position: NavigationItemPosition
            the position of navigation item

        parent: QWidget
            the parent of navigation item

        isTransparent: bool
            whether to use transparent background
        """
        if not interface.objectName():
            raise ValueError("The object name of `interface` can't be empty string.")
        if parent and not parent.objectName():
            raise ValueError("The object name of `parent` can't be empty string.")

        interface.setProperty("isStackedTransparent", isTransparent)
        self.stackedWidget.addWidget(interface)

        # add navigation item
        routeKey = interface.objectName()
        item = self.navigationInterface.addItem(
            routeKey=routeKey,
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )

        # initialize selected item
        if self.stackedWidget.count() == 1:
            self.stackedWidget.currentChanged.connect(self._onCurrentInterfaceChanged)
            self.navigationInterface.setCurrentItem(routeKey)
            qrouter.setDefaultRouteKey(self.stackedWidget, routeKey)

        self._updateStackedBackground()

        return item

    def resizeEvent(self, e):
        self.titleBar.move(10, 0)
        self.titleBar.resize(self.width() - 10, self.titleBar.height())
