import sys, os
from cx_Freeze import setup, Executable

os.environ["TCL_LIBRARY"] = "./python310"
os.environ["TK_LIBRARY"] = "./python310"

base = None
include_files = [
    "./assets",
    "./python310"
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
            "KrypApp.py",
            base=base,
            target_Name="KrypApp.exe",
            icon="./assets/icon.ico"
        )
    ]
)
