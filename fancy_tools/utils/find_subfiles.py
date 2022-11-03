import glob
import os

def findFiles(path, file, *args):
    found_files = []
    for f in glob.glob("/%s/**/%s" %(path, file), recursive=True):
        print("found : ", f)
        found_files.append(f)
    return found_files


#     for root, dirs, files in os.walk(path):
#         asset, asset_file = file.split("/")
#         if asset in dirs:
#             if asset_file in files:
#                 print(os.path.join(root, file))


# findFiles(r"\\storage01.qvisten.no\rendertemp\kutoppen3\output\groomdata\q002.6", r"bernt/hair.usda")

