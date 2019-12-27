# add section and dots behind section names. All sections are listed in a file 'sections.txt'

from unidecode import unidecode
import io

section_file 	= "Elegant-Puzzle/sections.txt"
in_file 		= "Elegant-Puzzle/Elegant-Puzzle3.txt"
out_fn_prefix 	= "Elegant-Puzzle/txt/Elegant-Puzzle-"
out_fn_suffix 	= ".txt"
out_fn_part 	= 0
prefix 		  	= " Section "
suffix 			= "."
chapter_prefix  = "Chapter "
long_pause		= "...   "
max_file_size 	= 5000			# limitation of GCP TTS API
sections 		= []

# get the list of sections and add them to the array
f = open(section_file, "r")
for line in f:
	sections.append(line.rstrip())
f.close()


# read the source text file, process sections and write to output file.
in_file = io.open(in_file, mode = "r", encoding="utf-8")
out_file = open(out_fn_prefix + out_fn_suffix, "w")
for line in in_file:
	# convert unicode quotes to ascii and remove trailing spaces/new lines.
	line = unidecode(line).rstrip()

	# skip empty lines
	if len(line) == 0:
		continue
		
	# add section prefix/suffix if this line is a section header
	if line in sections:
		line = line.replace(" ", ". ", 1)					# replace the first space with dot and space
		line = prefix + line + suffix						# add prefix and suffix for sections.	
	
	# open a new file on new chapter
	if line.startswith(chapter_prefix):
		out_file.close()
		out_fn_part = 0
		chapter_as_fn = line.replace (".", "").replace (" ", "-") 
		out_fn = out_fn_prefix + chapter_as_fn + "_" + str(out_fn_part) + out_fn_suffix
		out_file = open(out_fn, "w")

	# remove last dot (if exist) and add long pause
	line = line.rstrip(".") + long_pause

	# replace colon with long pause
	line = line.replace(":", long_pause)

	# remove stars (used for bullets)
	line = line.replace("*", "")

	# convert quotes to \" etc.
	line = line.replace('"','\\"')

	# make a new file if we go above the GCP limit
	if out_file.tell() + len(line) > max_file_size:
		out_file.close()
		out_fn_part += 1
		out_fn = out_fn_prefix + chapter_as_fn + "_" + str(out_fn_part) + out_fn_suffix
		out_file = open(out_fn, "w")

	out_file.write(line)

in_file.close()
out_file.close()
