from cx_Freeze import setup, Executable


"""This script is used to freeze the code into a Windows executable"""

build_exe_options = {"excludes": ["tkinter"]}

target = Executable(
    script="DailyWiki.py",
    base="Win32GUI",
    icon="wikipedia_iconblack.ico"
    )



setup(
    name = "DailyWiki",
    version = "1.0",
    description = "A new Wikipedia article every day, directly on your desktop",
    options = {"build_exe": build_exe_options},
    executables =[target]
)
