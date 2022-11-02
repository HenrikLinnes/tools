import hou
import os

def export_nodes(path):
    sel = hou.selectedNodes()
    context_node = sel[0].parent()
    context_node.saveItemsToFile(sel, path, False)

def import_nodes(path):
    context_node = ""
    context_node = get_scene_viewer().pwd()
    context_node.loadChildrenFromFile(path, False)

def get_scene_viewer():
    desk = hou.ui.currentPaneTabs()
    for i in desk:
        if i.type() == hou.paneTabType.SceneViewer:
            return i
            break

def export_screengrab(path):
    # GET FIRST VIEWPORT
    viewer = get_scene_viewer()

    # SET FLIPBOOK SETTINGS
    fbs = viewer.flipbookSettings().stash()
    fbs.frameRange((1,1))
    fbs.resolution((100,100))
    fbs.output("{}.jpg".format(path.rsplit('.',1)[0]))
    fbs.outputToMPlay(False)
    # WRITE FILE
    viewer.flipbook(viewer.curViewport(), fbs)