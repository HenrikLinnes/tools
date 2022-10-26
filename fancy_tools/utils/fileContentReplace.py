""" A TOOL WHICH LETS YOU BATCH SEARCH AND REPLACE WORDS WITHIN MULTIPLE FILES ACROSS FOLDERS """

import glob
import fileinput

def findFiles(path, file, *args):
    print("files, ", file)
    found_files = []
    print(path,file)
    for f in glob.glob("/%s/**/%s" %(path, file), recursive=True):
        print("found : ", f)
        found_files.append(f)
    return found_files

def replace(found_files, old, new, *args):
    files_renamed = 0
    for f in found_files:
        print("opening ", f)
        temp_file = open(f, "r+")

        for line in fileinput.input(f):
            if old in line:
                print("Match Found")
                temp_file.write(line.replace(old, new))
                files_renamed+=1
            else:
                print("Match Not Found")
        temp_file.close()
    return files_renamed

    