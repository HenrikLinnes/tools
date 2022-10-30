import hou
import os

def export_nodes(path):
    sel = hou.selectedNodes()
    context_node = sel[0].parent()
    context_node.saveItemsToFile(sel, path, False)



def import_nodes(path):
    context_node = ""
    desk = hou.ui.currentPaneTabs()
    for i in desk:
        if "SceneViewer" in i.type().name():
            context_node = i.pwd()
            break


    print("context_node: ", context_node)
    context_node.loadChildrenFromFile(path, False)
    print("loaded")