"""Manages the GUI for the settings window. This window is NOT OS-dependant."""

import logging

from PyQt5.QtWidgets import QDialog, QGridLayout, QListWidget, QPushButton, QListWidgetItem, QInputDialog
from usertopicsmanager import UserTopicsManager

class TopicsSelectionDialogWindow(QDialog):

    def __init__(self, settings_reader, settings_writer):

        self.logger = logging.getLogger(__name__)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)

        self.settings_reader = settings_reader
        self.current_settings = self.settings_reader.readSettings()
        self.settings_writer = settings_writer
        self.user_topics_manager = UserTopicsManager(self.current_settings)

        super().__init__()
        self.setModal(True)
        self.setWindowTitle("Select topics")

        self.topics_list = QListWidget()
        self.ok_btn = QPushButton("OK", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.add_btn = QPushButton("Add", self)
        self.delete_btn = QPushButton("Delete", self)

        self.initNewTopicWindow()

        self.topics_widgets = []

        self.setLayout()
        self.setGuiEvents()

    def initNewTopicWindow(self):

        self.new_topic_dialog = QInputDialog(self)
        self.new_topic_dialog.setWindowTitle("Add a new topic")
        self.new_topic_dialog.setLabelText("Please enter the topic you want to add. It must correspond to a valid category on Wikipedia")
        self.new_topic_dialog.accepted.connect(self.insertNewTopic)

    def prepare(self):

        self.resize(350, 150)
        self.topics_list.clear()

        for i in self.current_settings["TOPICS"]:

            self.topics_widgets.append(QListWidgetItem(i, self.topics_list))

    def setLayout(self):

        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.layout.addWidget(self.topics_list, 0, 0, 6, 4)
        self.layout.addWidget(self.add_btn, 1, 4, 1, 1)
        self.layout.addWidget(self.delete_btn, 2, 4, 1, 1)
        self.layout.addWidget(self.ok_btn, 3, 4, 1, 1)
        self.layout.addWidget(self.cancel_btn, 4, 4, 1, 1)

    def setGuiEvents(self):

        self.ok_btn.clicked.connect(self.validateTopicsSelection)
        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn.clicked.connect(self.addTopic)
        self.delete_btn.clicked.connect(self.deleteTopic)

    def addTopic(self, topic):

        self.new_topic_dialog.show()

    def insertNewTopic(self):

        topic = self.new_topic_dialog.textValue()
        self.logger.debug("Topic entered by the user: " + str(topic))
        

        result = self.user_topics_manager.insertNewTopic(topic)

        if result == "OK":

            self.topics_widgets.append(QListWidgetItem(topic, self.topics_list))
            return


        if result == "TOO MANY TOPICS":

            self.new_topic_dialog.setLabelText("You have already selected too many topics. Please delete some of them unitil you have less than 10 of them")
            self.new_topic_dialog.show()
            return

        elif result == "ALREADY EXISTS":

            self.new_topic_dialog.setLabelText("You have already registered that topic")
            self.new_topic_dialog.show()
            return

        elif result == "NOT FOUND":

            self.new_topic_dialog.setLabelText("The category you requested does not exist on Wikipedia. Please enter the name of a valid category")
            self.new_topic_dialog.show()
            return

        elif result == "NO CONNECTION":

            self.new_topic_dialog.setLabelText("Connection with Wikipedia servers has been lost, please try again later")
            self.new_topic_dialog.show()
            return

        else:

            self.new_topic_dialog.setLabelText("An error has occured, please try again later")
            self.new_topic_dialog.show()
            return


    def deleteTopic(self):

        current_item = self.topics_list.item(self.topics_list.currentRow())

        if current_item != None:

            current_item_name = current_item.text()

        else:
            return
        
        self.user_topics_manager.deleteTopic(str(current_item_name))
        self.topics_list.takeItem(self.topics_list.currentRow())



    def validateTopicsSelection(self):

        self.accept()

        return

    def getUserTopics(self):

        return self.current_settings["TOPICS"]

