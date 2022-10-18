import sys
import os

from fancy_tools.utils import fileContentReplace

path = "\\storage01.qvisten.no\rendertemp\kutoppen3\output\groomdata\q002.4\shots"
file = "bernt\hair.usda"
found_files = fileContentReplace.findFiles(path, file)

old = "__default"
new = "__bigHair"

fileContentReplace.replace(found_files, old, new)