"""
Developed By: JumpShot Team
Written by: riscyseven
"""

class EditorInterface:
    def __init__(self, remCallBack, dropCallBack,
                 compMovedCallBack, compResizeCallBack):
        self._remCallBack = remCallBack
        self._dropCallBack = dropCallBack
        self._compMovedCallBack = compMovedCallBack
        self._compResizeCallBack = compResizeCallBack


    def callRemCallBack(self, comp):
        self._remCallBack(comp)
    

    def callDropCallBack(self, evt, comp):
        self._dropCallBack(evt, comp)
    

    def callCompMoveCallBack(self, oldPos: list, newPos: list, comp):
        self._compMovedCallBack(oldPos, newPos, comp)


    def callCompResizeCallBack(self, oldProp: list, newProp: list, comp):
        self._compResizeCallBack(oldProp, newProp, comp)
