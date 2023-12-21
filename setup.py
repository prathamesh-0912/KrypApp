import sys, os
from cx_Freeze import setup, Executable

# Specify your Python installation directory here
python_dir = "C:/Users/lawan/AppData/Local/Programs/Python/Python39"

os.environ["TCL_LIBRARY"] = os.path.join(python_dir, "tcl", "tcl8.6")
os.environ["TK_LIBRARY"] = os.path.join(python_dir, "tcl", "tk8.6")

base = None
include_files = [
    "./assets",
    os.path.join(python_dir, "DLLs", "tcl86t.dll"),
    os.path.join(python_dir, "DLLs", "tk86t.dll")
]

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="KrypApp",
    version="1.4",
    description="File Encryption App",
    options={
        "build_exe": {
            "include_files": include_files
        }
    },
    executables=[
        Executable(
            script="KrypApp.py",
            base=base,
            #targetName="KrypApp.py",
            icon="./assets/icon.ico"
        )
    ]
)
