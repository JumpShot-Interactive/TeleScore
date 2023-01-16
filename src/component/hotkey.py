"""
Developed By: JumpShot Team
Written by: riscyseven
"""

import sys
from pynput import keyboard
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject
from gm_resources import GMessageBox

class HotKey(QObject):
    keys = ["Ctrl", "Alt", "Shift", "Space"]
    signal = pyqtSignal()

    def __init__(self, hotKey):
        super().__init__(None)
        if (sys.platform == "win32"):
            try:
                hotKey = keyboard.HotKey.parse(self._translateKey(hotKey))
            except Exception:
                msg = GMessageBox("Hotkey not registered",
                 "This key sequence is not accepted, please try a different sequence",
                  "Info")
                msg.exec()

            key = keyboard.HotKey(
                hotKey,
                self._onPress
            )
            self.listener = keyboard.Listener(
                on_press=self._for_canonical(key.press),
                on_release=self._for_canonical(key.release)
            )
            self.listener.start()

    def _for_canonical(self, f):
        return lambda k: f(self.listener.canonical(k))

    def _translateKey(self, key: str) -> str:
        for modKey in self.keys:
            if (modKey in key):
                newKey = "<{}>".format(modKey.lower())
                key = key.replace(modKey, newKey)
        return key

    def stopThread(self):
        if (sys.platform == "win32"):
            self.listener.stop()

    def _onPress(self):
        self.signal.emit()