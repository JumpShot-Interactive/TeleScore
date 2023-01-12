import sys, os
import fnmatch
from cx_Freeze import setup, Executable

py_package = ["os", "sys", "PyQt6", "requests", "pynput"]

def find_files(directory, patterns):
    """ Recursively find all files in a folder tree """
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if ".pyc" not in basename and "__pycache__" not in basename:
                for pattern in patterns:
                    if fnmatch.fnmatch(basename, pattern):
                        filename = os.path.join(root, basename)
                        yield filename

# base="Win32GUI" should be used only for Windows GUI app
base = None
exes = None
PATH = os.path.dirname(os.path.realpath(__file__))

if sys.platform == "win32":
    base = "Win32GUI"
    copy_path = os.path.join(PATH, "src")
    src_files = []
    for i in find_files("src", ["*"]):
        src_files.append((i, os.path.join("lib", i)))
    build_exe_options = {"packages": py_package, "include_files": src_files, "excludes": ["tkinter", "numpy", "pydoc_data", "distutils", "setuptools"]}

elif sys.platform == "darwin":
    copy_path = os.path.join(PATH, "src")
    src_files = []
    for i in find_files("src", ["*"]):
        src_files.append((i, os.path.join("lib", i)))
    build_exe_options = {"packages": py_package, "include_files": src_files, "excludes": ["tkinter", "numpy", "pydoc_data", "distutils", "setuptools"]}


exes = [Executable("src/main.py",
                    base=base,
                    icon=os.path.join(PATH, "src", "resources", "icon.ico"),
                    shortcut_dir="ProgramMenuFolder",
                    target_name="TeleScore")]

setup(
    name="TeleScore",
    version="1.0",
    description="TeleScore - Open Source Scoreboard Software",
    options={"build_exe": build_exe_options},
    executables=exes,
)
