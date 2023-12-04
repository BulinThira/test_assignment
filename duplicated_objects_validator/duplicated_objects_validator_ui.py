"""
#run this script in Maya Script Editor after putting the .py file in the maya scripts folder

from importlib import reload
from duplicated_objects_validator import duplicated_objects_validator_ui
reload(duplicated_objects_validator_ui)
duplicated_objects_validator_ui.run()
"""

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
from importlib import reload
import maya.OpenMayaUI as omui

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from duplicated_objects_validator import duplicated_objects_validator_utils
reload(duplicated_objects_validator_utils)

class MainWidget(QMainWindow):
    """
    main widget that contains TabWidget of the 3 main features
    """
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self.resize(320, 380)
        self.setWindowTitle("Duplicated Objects Validator")

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.objects_item_list = ObjectListWidget()

        # - - - main ui components build - - -#
        self.procedure_buttons_layout = QHBoxLayout()

        self.fix_button = QPushButton("fix")
        self.fix_button.setMinimumHeight(30)
        self.custom_close_button = QPushButton("close")
        self.custom_close_button.setMinimumHeight(30)

        # - - - initiate finding duplicateds - - - #
        self.objects_item_list.add_new_item()
        if self.objects_item_list.count() == 0:
            self.fix_button.setEnabled(False)

        # - - - signal & slot - - - #
        self.objects_item_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.objects_item_list.itemClicked.connect(self.objects_item_list.on_item_clicked)
        self.fix_button.clicked.connect(self.objects_item_list.fix_naming)
        self.custom_close_button.clicked.connect(lambda: self.close())

        self.procedure_buttons_layout.addWidget(self.fix_button)
        self.procedure_buttons_layout.addWidget(self.custom_close_button)

        # - - - add layout/widget/item to the main layout - - -#
        self.main_layout.addWidget(self.objects_item_list)
        self.main_layout.addLayout(self.procedure_buttons_layout)


class ObjectListWidget(QListWidget):
    """
    interactive ListWidget for showing main controller's children
    """
    def __init__(self, *args, **kwargs):
        super(ObjectListWidget, self).__init__(*args, **kwargs)
        self.item_list = []
    
    def add_new_item(self):
        """
        add new selected objects in Maya viewport into ListWidget
        """
        objects_dict = duplicated_objects_validator_utils.duplicated_objects_validating_command()
        if bool(objects_dict):
            for key, values in objects_dict.items():
                item = ObjectListWidgetItem(values, key)
                self.indexFromItem(item)

                self.addItem(item)
        else:
            logger.warning("There are no objects with the same name")
    
    def on_item_clicked(self, item):
        """
        function that select referred objects when click ListWidget's item
        """
        # selected_item_text = item.item_name()
        # duplicated_objects_validator_utils.simple_objs_selection(selected_item_text)
        tmp_list = []
        selected_items = self.selectedItems()
        for item in selected_items:
            tmp_list.append(item.item_name())
        duplicated_objects_validator_utils.simple_objs_selection(tmp_list)
        logger.info(tmp_list)
    
    def fix_naming(self):
        """
        main function for fixing the duplicateds name
        """
        if self.count() == 0:
            logger.warning("There are no objects with the same name")
            return
        selected_items = self.selectedItems()
        for item in selected_items:
            duplicated_objects_validator_utils.rename_duplicateds(item.text(), item.item_name())
            self.takeItem(self.currentRow())


class ObjectListWidgetItem(QListWidgetItem):
    """
    create single item of ObjectListWidget

    Args:
        obj_item (str): name of obj item
        obj_item_display (list): list of of obj's display name
    """
    def __init__(self, obj_item, obj_item_display):
        super(ObjectListWidgetItem, self).__init__()
        self.obj_item = obj_item
        self.obj_item_display = obj_item_display
        self.setText(self.obj_item_display)
    
    def item_name(self):
        """
        function for returnnig actual object's name

        Returns:
            str: name of actual object's name
        """
        return(self.obj_item)
    
def run():
    """
    run command
    """
    maya_ptr = omui.MQtUtil.mainWindow()
    ptr = wrapInstance(int(maya_ptr), QWidget)

    global ui
    try:
        ui.close()
    except:
        pass

    ui = MainWidget(parent=ptr)
    ui.show()
