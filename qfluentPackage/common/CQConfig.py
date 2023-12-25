# -*- coding: utf-8 -*-
# @FileName: CQConfig.py
"""

"""

import json
from copy import deepcopy
from pathlib import Path

from PyQt5.QtCore import QObject
from qfluentwidgets import ConfigItem, exceptionHandler, QConfig

__all__ = ['CustomConfig']


class CustomConfig(QObject):
    """ Config of app """

    def __init__(self, file_path: str):
        super().__init__()
        self.file = Path(file_path)
        self._cfg = self

    @staticmethod
    def get(item):
        """ get the value of config item """
        return item.value

    def set(self, item, value, save=True, copy=True):
        """ set the value of config item

        Parameters
        ----------
        item: ConfigItem
            config item

        value:
            the new value of config item

        save: bool
            whether to save the change to config file

        copy: bool
            whether to deep copy the new value
        """
        if item.value == value:
            return

        try:
            item.value = deepcopy(value) if copy else value
        except:
            item.value = value

        if save:
            self.save()

    def toDict(self, serialize=True):
        """ convert config items to `dict` """
        items = {}
        for name in dir(self._cfg.__class__):
            item = getattr(self._cfg.__class__, name)
            if not isinstance(item, ConfigItem):
                continue

            value = item.serialize() if serialize else item.value
            if not items.get(item.group):
                if not item.name:
                    items[item.group] = value
                else:
                    items[item.group] = {}

            if item.name:
                items[item.group][item.name] = value

        return items

    def save(self):
        """ save config """
        self._cfg.file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._cfg.file, "w", encoding="utf-8") as f:
            json.dump(self._cfg.toDict(), f, ensure_ascii=False, indent=4)

    @exceptionHandler()
    def load(self, file=None, config=None):
        """ load config

        Parameters
        ----------
        file: str or Path
            the path of json config file

        config: Config
            config object to be initialized
        """
        if isinstance(config, QConfig):
            self._cfg = config

        if isinstance(file, (str, Path)):
            self._cfg.file = Path(file)

        try:
            with open(self._cfg.file, encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            cfg = {}

        # map config items'key to item
        items = {}
        for name in dir(self._cfg.__class__):
            item = getattr(self._cfg.__class__, name)
            if isinstance(item, ConfigItem):
                items[item.key] = item

        # update the value of config item
        for k, v in cfg.items():
            if not isinstance(v, dict) and items.get(k) is not None:
                items[k].deserializeFrom(v)
            elif isinstance(v, dict):
                for key, value in v.items():
                    key = k + "." + key
                    if items.get(key) is not None:
                        items[key].deserializeFrom(value)
