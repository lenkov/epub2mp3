# create json files based on the txt files

import fnmatch 
import os 
from string import Template

src_folder      = "Elegant-Puzzle/txt/"
dest_folder     = "Elegant-Puzzle/json/"
template        = "payload.json"
file_pattern    = "*.txt"

files = os.listdir(src_folder) 
matched_files = fnmatch.filter(files, file_pattern)

if len(matched_files) == 0: 
    quit()

with open(template, "r") as f:
        template = f.read()
tmpl = Template(template)        

for file in matched_files:
    with open(src_folder + file, "r") as f:
        t = f.read()
    out_fn =   file.replace(".txt", ".json", 1) 
    with open(dest_folder + out_fn, "w") as f:
        t = f.write(tmpl.substitute(text = t))

