from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil 
import blocktype
import sys 

"""
class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"
	TEXT = "text" 
"""

def copy_dir_stuff(source, destination):
	print (f"######### STARTING COPY FROM {source} to {destination} ############")
	print (f"i'm currently checking this as the source path '{source}'")
	### erases everything so don't code stupid folders
	if not os.path.exists(source):
		raise Exception ("Source directory missing")
	if os.path.exists(destination):
		print (f"I'm deleting this dir in prep to recreate and copy {destination}")
		shutil.rmtree(destination)
	os.mkdir(destination)
	copythings = os.listdir(path=source)
	print (f"I found this many things to copy in the source dir: {copythings}")
	for thing in copythings:
		pathedthing = source + "/" + thing
		if os.path.isfile(pathedthing):
			print (f"copying this thing now {thing} to {destination}")
			shutil.copy(pathedthing, destination)
		elif os.path.exists(pathedthing):			
			destpath = destination + "/" + thing
			print (f"I found a directory instead, copying this dir {pathedthing} to {destpath}")
			copy_dir_stuff(pathedthing, destpath)
		else:
			print (f"I don't know what I found, it's just {pathedthing}, skipping operation")



def extract_title(markdown):
	# pull the first line from the markdown file
	#./content/index.md 
	# please run this from the root dir of the repo 

	
	with open(markdown,"r") as h:
		headerline = h.readline()

	if headerline[0] != "#":
		raise Exception ("H1 header missing from {markdown}")
	else: 
		hashless_header = headerline.replace("#","")
		cleanh = (hashless_header.lstrip()).rstrip()

	return cleanh



### This is now deprecated thanks to the recusrive version 
def generate_page(basepath, from_path, template_path, dest_path):
	print(f"##### Generating page from {from_path} to {dest_path} using {template_path} #####")
	with open(from_path, "r") as m:
		mdfile = m.read()

	with open(template_path, "r") as t:
		tmplfile = t.read()

	mdfile_htmlnode = blocktype.markdown_to_html_node(mdfile)
	md_htmlstring = mdfile_htmlnode.to_html()

	mdtitle = extract_title(from_path)

	v2tmpl = tmplfile.replace("{{ Title }}", mdtitle)
	v3tmpl = v2tmpl.replace("{{ Content }}", md_htmlstring)

	#dest_path should be just a path, but the instructions CLEARLY SAY 
	#that it's going to be the filename too, so now I have to strip that
	#to check if the dir exists, which is stupid. 
	
	pdestcheck = dest_path.rstrip("/index.html")

	if not os.path.exists(pdestcheck):
		print (f"WARNING: I had to create the dest directory {pdestcheck}")
		os.mkdir(pdestcheck)

	with open(dest_path, "w") as i:
		i.write(v3tmpl)

#well i cheated a bit, and it was an honest misunderstanding, but i just rewrote the recursive code to copy of the regular function's
#behaviour. Fuck it. 
def generate_pages_recursive(bpath, dir_path_content, template_path, dest_dir_path):
	print(f"##### Generating page(s) from {dir_path_content} to {dest_dir_path} using {template_path} #####")
	print("#############################################################################################")

	if not os.path.exists(dest_dir_path):
		print (f"#### Creating DEST DIR #######")
		os.mkdir(dest_dir_path)

	with open(template_path, "r") as t:
		tmplfile = t.read()

	if not os.path.exists(dir_path_content):
		raise Exception ("Source content path missing")
	allthethings = os.listdir(path=dir_path_content)
	print (f"I found this many things to parse in the source content path: {allthethings}")

	for thing in allthethings:
		fullpaththing = dir_path_content + "/" + thing 
		fulldestthing = dest_dir_path + "/" + thing 
		if os.path.isdir(fullpaththing):
			generate_pages_recursive(bpath, fullpaththing, template_path, fulldestthing)

		elif os.path.isfile(fullpaththing) and thing == "index.md":
			print (f"Found a markdown file: {fullpaththing}")

			with open(fullpaththing, "r") as imd:
				mdfile = imd.read()

			mdfile_htmlnode = blocktype.markdown_to_html_node(mdfile)
			md_htmlstring = mdfile_htmlnode.to_html()
			mdtitle = extract_title(fullpaththing)

			v2tmpl = tmplfile.replace("{{ Title }}", mdtitle)
			v3tmpl = v2tmpl.replace("{{ Content }}", md_htmlstring)

			v4tmpl = v3tmpl.replace('href="/','href="{basepath}')
			v5tmpl = v4tmpl.replace('src="/','src="{basepath}')

			if not os.path.exists(dest_dir_path):
				print (f"%%%%%%%%%%%   WARNING: I had to create the dest directory {dest_dir_path}   %%%%%%%%%%%%%%%")
				os.mkdir(dest_dir_path)

			towritefile = dest_dir_path + "/" + "index.html"
			print (f"@@@@@@ Making a index.html file here in {towritefile} @@@@@@")
			with open(towritefile, "w") as ihtml:
				ihtml.write(v3tmpl)

def main():


	if sys.argv[1] is None:
		basepath = "/"
	else: 
		basepath = sys.argv[1]

	#do we still need this? or are we uploading it? 
	copy_dir_stuff("./static", "./docs")

	generate_pages_recursive(basepath, "./content","./template.html","./docs")

if __name__ == "__main__":
	main()
