import glob

def findFiles(path, file, *args):
    found_files = []
    for f in glob.glob("/%s/**/%s" %(path, file), recursive=True):
        print("found : ", f)
        found_files.append(f)
    return found_files