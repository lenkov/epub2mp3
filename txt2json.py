# create json files based on the txt files

import fnmatch 
import os 
from string import Template
import sys

folder          = sys.argv[1] + "/"
fn_prefix       = sys.argv[1] + "-"
txt_folder      = folder + "txt/"
json_folder     = folder + "json/"
mp3_folder      = folder + "mp3/"
json_template   = "payload.json"
exec_template   = "curl --request POST 'https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=KKKK' --header 'Accept: application/json' --header 'Content-Type: application/json' -d '@$src_file' | jq .audioContent | sed 's/\"//g' | base64 -D > $dest_file"
file_pattern    = "*.txt"

files = os.listdir(txt_folder) 
matched_files = fnmatch.filter(files, file_pattern)

if len(matched_files) == 0: 
    quit()

with open(json_template, "r") as f:
        json_content = f.read()
json_tmpl = Template(json_content)  
exec_tmpl = Template(exec_template)      

for file in matched_files:
    with open(txt_folder + file, "r") as f:
        t = f.read()
    json_fn = file.replace(".txt", ".json", 1)
    mp3_fn  = file.replace(".txt", ".mp3", 1)
    with open(json_folder + json_fn, "w") as f:
        t = f.write(json_tmpl.substitute(text = t))
    print exec_tmpl.substitute(src_file = json_folder + json_fn, dest_file = mp3_folder + fn_prefix + mp3_fn)
