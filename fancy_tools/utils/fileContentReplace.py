# REPLACE STRING WITHIN A LIST OF FILES
import fileinput

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

