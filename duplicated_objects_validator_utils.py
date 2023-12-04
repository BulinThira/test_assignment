"""
duplicatedObjectValidator_utils
Contains: Maya Commands (2022)
"""
import maya.cmds as cmds

def object_list_command(quantity=""):
    """
    function that returns selected
    this function can returns various type of variable depends on input argument

    Args:
        quantity (str): default for type of return; single means one object's name will be returned

    Returns:
        None: if nothing is selected
        str: if input argument is defined as single (return the first member of list)
        list: return all of selections
    """
    object_name_list = cmds.ls(selection=True)
    if len(object_name_list) == 0:
        return
    if quantity == "single":
        return(object_name_list[0])
    else:
        # if len(object_name_list) == 1:
        #     return(object_name_list[0])
        # else:
        return(object_name_list)

def duplicated_objects_validating_command():
    """
    main function for the validation

    Returns:
        dict: dictionary that have root name for key and list of referred nodes as value(s)
    """
    objs_dict = {}
    scene_dag_nodes = cmds.ls(dagObjects=True, transforms=True)
    for nodes in scene_dag_nodes:
        splitting = nodes.split("|")
        if len(splitting) > 1:
            root_node = splitting[-1]
            if root_node not in objs_dict:
                objs_dict[root_node] = [nodes]
            else:
                objs_dict[root_node].append(nodes)
    
    return(objs_dict)

def rename_duplicateds(root_name="", name_list=[]):
    ordering = 1
    for member in name_list:
        actual_ordering = (str(ordering)).zfill(3)
        new_name = root_name + "_" + actual_ordering
        cmds.rename(member, new_name)
        ordering += 1

def simple_objs_selection(objs_list=[]):
    """
    just a bloody simple objects selection
    that will clear selection beforehand

    Args:
        objs_list (list): list of objects
    """
    cmds.select(clear=True)
    for sub_list in objs_list:
        cmds.select(sub_list, add=True)