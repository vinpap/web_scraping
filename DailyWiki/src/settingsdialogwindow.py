"""Implementation of the settings dialog window. From there the user can choose
the settings and access the custom topics selection window."""

from PyQt5.QtWidgets import QDialog, QGridLayout, QButtonGroup, QCheckBox, QPushButton
from topicsselectiondialogwindow import TopicsSelectionDialogWindow
import logging
import sys

class SettingsDialogWindow(QDialog):

    def __init__(self, settings_reader, settings_writer):

        self.logger = logging.getLogger(__name__)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)

        self.settings_reader = settings_reader
        self.settings_writer = settings_writer

        self.current_settings = self.settings_reader.readSettings()

        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Settings")
        self.resize(400, 150)

        self.topics_selection_boxes_group = QButtonGroup(self)

        self.random_article_box = QCheckBox(self)
        self.random_article_box.setText("Open a random article")
        self.select_topics_box = QCheckBox(self)
        self.select_topics_box.setText("Open an article about a selected topic")
        self.launch_at_startup_box = QCheckBox(self)
        self.launch_at_startup_box.setText("Launch DailyWiki at startup")

        self.topics_selection_btn = QPushButton("Select topics", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.ok_btn = QPushButton("OK", self)

        self.topics_selection_boxes_group.addButton(self.random_article_box)
        self.topics_selection_boxes_group.addButton(self.select_topics_box)

        if self.current_settings["RANDOM"]:

            self.random_article_box.setChecked(True)

        else:

            self.select_topics_box.setChecked(True)

        if self.current_settings["AUTOLAUNCH"]:

            self.launch_at_startup_box.setChecked(True)

        self.setLayout()
        self.setGuiEvents()

        self.topics_selection_dialog_window = TopicsSelectionDialogWindow(self.settings_reader,
                                                                          self.settings_writer)

    def setLayout(self):

        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.random_article_box, 0, 0, 1, 4)
        self.layout.addWidget(self.select_topics_box, 1, 0, 1, 3)
        self.layout.addWidget(self.topics_selection_btn, 1, 3, 1, 1)
        self.layout.addWidget(self.launch_at_startup_box, 2, 0, 1, 4)
        self.layout.addWidget(self.cancel_btn, 3, 1, 1, 1)
        self.layout.addWidget(self.ok_btn, 3, 2, 1, 1)

    def setGuiEvents(self):

        self.topics_selection_btn.clicked.connect(self.selectTopics)
        self.ok_btn.clicked.connect(self.validateSettings)
        self.cancel_btn.clicked.connect(self.reject)

    def selectTopics(self):

        self.logger.debug("Opening topics selection window...")
        self.topics_selection_dialog_window.prepare()
        self.topics_selection_dialog_window.show()

    def validateSettings(self):

        if self.random_article_box.isChecked():

            self.current_settings["RANDOM"] = True

        else:

            self.current_settings["RANDOM"] = False

        if self.launch_at_startup_box.isChecked():

            self.current_settings["AUTOLAUNCH"] = True

        else:

            self.current_settings["AUTOLAUNCH"] = False

        self.current_settings["TOPICS"] = self.topics_selection_dialog_window.getUserTopics()

        if not self.settings_writer.saveSettings(self.current_settings):

            self.logger.error("Unable to save the settings. Please read the logs for more details")
            sys.exit()
            
        self.accept()
