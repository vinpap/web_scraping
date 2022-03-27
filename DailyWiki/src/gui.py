"""Main GUI module. It inits all the different dialog windows and manages the
events. Please note that it offers two different GUI: a reduced interface in the
system tray (for Windows only) and a classical GUI with dialog windows popping
on the screen (for all other platforms)."""

import logging
import logging.handlers
import sys
import random
import platform
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QSystemTrayIcon, QMenu, QAction, QDialog, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon

# =============================================================================
# Base GUI class
# =============================================================================

class GuiCore():

    "Infrastructure layer class that manages the graphical user interface"


    def __init__(self, daily_article_selector):

        self.logger = logging.getLogger(__name__)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)
        self.logger.debug("Loading GUI")

        self.app = QApplication(sys.argv)


        os_name = platform.system()
        self.logger.info("Platform: " + os_name)

        self.article_selector = daily_article_selector
        self.article_title = self.article_selector.getDailyArticleTitle()

        self.setSystemTrayGUI()

    def setSettingsGui(self, settings_gui):

        """Inits the module that manages the GUI for the settings window."""

        self.settings_gui = settings_gui

    def setSystemTrayGUI(self):

        """Manages how DailyWiki appears in the system tray.
        Note: the installer automatically edits Windows' registry to make
        sure that balloons mssages are supported."""

        self.app.setQuitOnLastWindowClosed(False)
        self.icon = QIcon("resources/wikipedia_icon.png")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setToolTip("DailyWiki")
        self.tray.setVisible(True)

        self.menu = QMenu()
        self.settings_action = QAction("Settings")
        self.exit_action = QAction("Exit")
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.exit_action)

        self.settings_action.triggered.connect(self.openSettings)
        self.exit_action.triggered.connect(self.exitFromBackground)

        self.tray.setContextMenu(self.menu)
        
        self.logger.debug("Balloon messages supported by the platform: " +
                          str(QSystemTrayIcon.supportsMessages()))

        self.tray.showMessage("Your daily article is ready!", self.article_title)
        self.tray.messageClicked.connect(self.accessArticleFromTray)

        self.tray.activated.connect(self.accessArticleFromTray)
        self.tray.show()

   

    

    def accessArticleFromTray(self, activation_reason=QSystemTrayIcon.DoubleClick):

        """Allows to access the Wikipedia article when the user double-clicks
        the icon in the system tray"""

        if activation_reason != QSystemTrayIcon.DoubleClick:

            return

        self.logger.debug("Accessing article...")


        try:

            self.article_selector.accessDailyArticle()

        except requests.exceptions.ConnectionError:

            self.dialog_msg.setText("It looks like the connection has been interrupted... Try again later!")


    def openSettings(self):

        self.logger.debug("Opening settings...")
        self.settings_gui.displaySettings()

    def run(self):

        """Main loop function"""

        self.logger.debug("Entering main execution loop")

        sys.exit(self.app.exec_())

    def exitFromBackground(self):

        """Called to exit when the program is running in the system tray."""

        sys.exit()
