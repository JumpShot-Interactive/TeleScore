"""
Developed by: JumpShot Team
Written by: riscyseven, TheLittleDoc
Designed by: Fisk31, TheLittleDoc
"""

import sys, os
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication
from traceback import format_exc

if hasattr(sys, 'frozen'):
    import src
    sys.path.append(src.CURR_PATH)
    from gm_resources import resourcePath, GMessageBox
    from window.mainwindow import MainWindow

    base_path = os.path.dirname(sys.executable)
    lib_path = os.path.join(base_path, 'lib')
    
    # Add lib directory to PATH for DLL loading
    os.environ['PATH'] = lib_path + os.pathsep + os.environ.get('PATH', '')
    
    # Set Qt plugin path
    os.environ['QT_PLUGIN_PATH'] = lib_path
    QCoreApplication.addLibraryPath(lib_path)
    os.environ['QT_DEBUG_PLUGINS'] = '1'
else:
    from gm_resources import resourcePath, GMessageBox
    from window.mainwindow import MainWindow


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        with open(resourcePath("src/theme/fisk.qss"), 'r') as stream:
            style = stream.read()
            self.window.setStyleSheet(style)

    def raise_error(Self):
        assert False

def excepthook(eType, eValue, eTb):
    msg = GMessageBox("Unhandled Exception",
     "Uh Oh! Unhandled Exception Caught!\nReason:\n{}\n{}\n{}"
     .format(eType, eValue, format_exc()), "Info")

    msg.exec()
    QApplication.exit(0)

if __name__ == "__main__":
    if hasattr(sys, 'frozen'):
        sys.excepthook = excepthook

    exception = Application()
    ret = exception.app.exec()
    sys.exit(ret)
    
