import os

def findFiles(path, file, *args):
    found_files = []
    for root, dirs, files in os.walk(path):
        asset, asset_file = file.split("/")
        if asset in dirs:
            for files in os.listdir(os.path.join(root,asset)):
                if asset_file in files:
                    found_files.append(os.path.join(root,asset,files))

    return found_files