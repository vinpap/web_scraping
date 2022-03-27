import os
import shutil
from pathlib import Path

def setWorkingDirectory():

    WORKING_DIR = os.path.expanduser("~\AppData\Local\DailyWiki")

    if not os.path.exists(WORKING_DIR):

        os.mkdir(WORKING_DIR)
        print(Path(os.path.dirname(os.path.realpath(__file__))))
        
        path = Path(os.path.dirname(os.path.realpath(__file__)))
        path = path.parent.parent
        os.chdir(path)
        shutil.copytree("conf", WORKING_DIR + "\\conf")
        shutil.copytree("logs", WORKING_DIR + "\\logs")
        shutil.copytree("resources", WORKING_DIR + "\\resources")

    os.chdir(WORKING_DIR)
