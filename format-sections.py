# add section and dots behind section names. All sections are listed in a file 'sections.txt'

from unidecode import unidecode
import io


section_file 	= "sections.txt"
in_file 		= "Elegant-Puzzle3.txt"
out_fn_prefix 	= "Elegant-Puzzle-"
out_fn_suffix 	= ".txt"
out_fn_part 	= 0
prefix 		  	= " Section "
suffix 			= "."
chapter_prefix  = "Chapter "
max_file_size 	= 5000			# limitation of GCP TTS API


sections 		= []

# get the list of sections and add them to the array
f = open(section_file, "r")
for line in f:
	sections.append(line.rstrip())
f.close()


# read the source text file, process sections and write to output file.
in_file = io.open(in_file, mode = "r", encoding="utf-8")
out_file = open(out_fn_prefix, "w")
for line in in_file:
	# convert unicode quotes to ascii and remove trailing spaces/new lines.
	line = unidecode(line).rstrip()
		
	# check if this line exist in sections[]?
	if line in sections:
		line = line.replace(" ", ". ", 1)					# replace the first space with space and dot
		line = prefix + line + suffix						# add prefix and suffix for sections.	
	
	# check if new chapter and open a new file
	if line.startswith(chapter_prefix):
		out_file.close()
		out_fn_part = 0
		chapter_as_fn = line.replace (".", "").replace (" ", "-") 
		out_fn = out_fn_prefix + chapter_as_fn + "_" + str(out_fn_part) + out_fn_suffix
		out_file = open(out_fn, "w")

	# add dot at the end if not there.
	line = line + "."
	line = line.replace ("..", ".")

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
