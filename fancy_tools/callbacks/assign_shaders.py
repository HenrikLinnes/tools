from fancy_tools.tools.shader_assignment import assign_shaders
import importlib

window_instance = None

def show():
    global window_instance

    importlib.reload(assign_shaders)
    window_instance = assign_shaders.Assign_Shaders()

    window_instance.show()

    