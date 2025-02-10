import sys, os
from cx_Freeze import setup, Executable, build_exe
from PyQt6 import QtCore

BUILD_PATH = "build/exe.win-amd64-3.12"
base = None
PATH = os.path.dirname(os.path.realpath(__file__))
LICENSE = os.path.join(PATH, "LICENSE")

theme_path = os.path.join(PATH, "src", "theme")
output_path = os.path.join(PATH, "Output")
qt_path = os.path.dirname(QtCore.__file__)
qt_bin_path = os.path.join(qt_path, "Qt6", "bin")
py_package = ["os", "sys", "PyQt6", "requests", "pynput", "src"]


def convPytoExe() -> list:
    pyfile = []
    for dir in sys.path:
        pyfile.append((dir, "*"))
    pyfile.append((PATH, "*"))
    return pyfile

if sys.platform == "win32":
    base = "Win32GUI"
    copy_path = "src"
    src_files = [(theme_path, os.path.join("src", "theme")), (LICENSE, "LICENSE")]
    qt_media_files = [
        (qt_bin_path, "lib")
    ]

    build_exe_options = {
        "packages": py_package,
        "include_files": src_files + qt_media_files,
        "excludes": ["tkinter", "numpy", "pydoc_data", "distutils", "setuptools"],
        "optimize": 2,
        "replace_paths": convPytoExe(),
        "include_msvcr": True,
    }


exes = [
    Executable(
        "src/main.py",
        base=base,
        icon=os.path.join(PATH, "src", "resources", "icon.ico"),
        shortcut_dir="ProgramMenuFolder",
        target_name="TeleScore"
        )
    ]

def post_build():
    directories = [
        "Output",
        "required"
    ]

    for directory in directories:
        lib_path = os.path.join(BUILD_PATH, directory)
        os.makedirs(lib_path, exist_ok=True)

setup(
    name="TeleScore",
    version="1.0",
    description="TeleScore - Open Source Scoreboard Software",
    options={"build_exe": build_exe_options},
    executables=exes,
)

if __name__ == "__main__":
    post_build()