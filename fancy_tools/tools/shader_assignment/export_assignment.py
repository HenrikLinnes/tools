# GET ALL SHADERS IN SCENE
import json
import maya.cmds as m

class export_assignment():
    def __init__(self) -> None:

        self.connected_dict = {}
    
    def run(self):
        all_materials = self.get_materials()

        for material in all_materials:
            connections = []
            connections = m.listConnections(m.listConnections(material, type="shadingEngine"), type="mesh")
            if connections != None:
                self.connected_dict[material] = connections

        my_json = json.dumps(self.connected_dict)
        print(my_json)
            
                
                

    def get_materials(self):
        materials = []
        for shading_engine in m.ls(type='shadingEngine'):
            if m.sets(shading_engine, q=True):
                for material in m.ls(m.listConnections(shading_engine), materials=True):
                    materials.append(material)
        return materials
    