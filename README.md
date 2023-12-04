# test_assignment

#run this script in Maya Script Editor after putting the .py file in the maya scripts folder

from importlib import reload
from duplicated_objects_validator import duplicated_objects_validator_ui
reload(duplicated_objects_validator_ui)
duplicated_objects_validator_ui.run()
