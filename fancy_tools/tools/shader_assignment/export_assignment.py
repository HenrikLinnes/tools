# GET ALL SHADERS IN SCENE
import os
import json
import maya.cmds as m

class export_assignment():
    def __init__(self):

        self.connected_dict = {}
        self.file_path = m.file(q=True, sn=True)
        self.folder_path = os.path.dirname(self.file_path)
        self.file_name = os.path.basename(self.file_path)
        self.raw_name, self.extension = os.path.splitext(self.file_name)
    
    def run(self):
        all_materials = self.get_materials()

        for material in all_materials:
            connections = []
            connections = m.ls(m.listConnections(m.listConnections(material, type="shadingEngine"), type="mesh"), long=True)
            if connections != None:
                self.connected_dict[material] = connections

        my_json = json.dumps(self.connected_dict, indent=4)
        self.export_json(my_json)
            
                
    def export_json(self, json_list):
        with open("{}/{}.json".format(self.folder_path, self.raw_name), "w") as outfile:
            outfile.write(json_list)

    def get_materials(self):
        materials = []
        for shading_engine in m.ls(type='shadingEngine'):
            if m.sets(shading_engine, q=True):
                for material in m.ls(m.listConnections(shading_engine), materials=True):
                    materials.append(material)
        return materials
    
