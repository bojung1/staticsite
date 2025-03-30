from textnode import TextType, TextNode 
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	outlist = []

	#old_nodes is supposed to be a list
	#a node is a TextNode, usually TEXT  

	for node in list(old_nodes):
	
		if node.text_type != TextType.TEXT:
			outlist.append(node)
		else:
			delindexpos = node.text.find(delimiter)
			if delindexpos == -1:
				outlist.append(node)
			else:
				seconddelindexpos = node.text.find((delimiter),delindexpos+1)

				if seconddelindexpos == -1:
					raise Exception ("That's invalid Markdown syntax")

				match delimiter:
					case "`":
						newtype = TextType.CODE
					case "**":
						newtype = TextType.BOLD
					case "_":
						newtype = TextType.ITALIC
					case _:
						raise Exception ("no such delimiter, idiot")

				if newtype != text_type:
					raise Exception ("delimiter / TextType mismatch")


				newnode1 = TextNode(node.text.split(delimiter)[0], TextType.TEXT)
				newnode2 = TextNode(node.text.split(delimiter)[1], newtype)
				newnode3 = TextNode(node.text.split(delimiter)[2], TextType.TEXT)
				if newnode1.text != "":
					outlist.append(newnode1)
				if newnode2.text != "":
					outlist.append(newnode2)
				if newnode3.text != "":
					outlist.append(newnode3)
				
	return outlist 

#always images 
def split_nodes_image(old_nodes):
	outlist = []


	for node in old_nodes:

		if node.text_type != TextType.TEXT:
			outlist.append(node)
		else:
			while node.text.count('![') > 0:
				advance_position = (node.text.find(')'))+1
			
				first_bit_text = node.text.split("![")[0]
				node_to_add = TextNode(first_bit_text, TextType.TEXT)
				outlist.append(node_to_add)

				matches = extract_markdown_images(node.text)

				entry = matches.pop(0)
				image_meta_text1 = entry[0]
				image_url_text  = entry[1]

				node_to_add = TextNode(image_meta_text1, TextType.IMAGE, image_url_text)
				
				outlist.append(node_to_add)

				node.text = node.text[advance_position:]

			if node.text != "":
				node_to_add = TextNode(node.text, TextType.TEXT)
				outlist.append(node_to_add)

	return outlist 


def split_nodes_link(old_nodes):
	outlist = []

	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			outlist.append(node)
		else:

			number_left_bracket = node.text.count("[")
			number_right_bracket = node.text.count("]")
			number_left_par = node.text.count("(")
			number_right_par = node.text.count(")")
		
			if number_left_bracket != number_right_bracket or number_left_par != number_right_par or number_left_par != number_left_bracket:
				raise Exception ("badly formatted images - missing bracket or parenthesis")

			while node.text.count(')') > 0:
				advance_position = (node.text.find(')'))+1
			
				first_bit_text = node.text.split("[")[0]
				node_to_add = TextNode(first_bit_text, TextType.TEXT)
				outlist.append(node_to_add)

				matches = extract_markdown_links(node.text)

				entry = matches.pop(0)
				link_meta_text1 = entry[0]
				link_url_text  = entry[1]

				node_to_add = TextNode(link_meta_text1, TextType.LINK, link_url_text)
				outlist.append(node_to_add)

				node.text = node.text[advance_position:]

			if node.text != "":
				node_to_add = TextNode(node.text, TextType.TEXT)
				outlist.append(node_to_add)

	return outlist 


def extract_markdown_images(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	return matches 

def extract_markdown_links(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	return matches

#if you don't do it in this order there may be trouble
def text_to_textnodes(text):

	A = TextNode(text, TextType.TEXT)
	B = split_nodes_image([A])
	C = split_nodes_link(B)
	D = split_nodes_delimiter(C, "**", TextType.BOLD)
	E = split_nodes_delimiter(D, "_", TextType.ITALIC)
	F = split_nodes_delimiter(E, "`", TextType.CODE)

	return F



def text_node_to_html_node(text_node):
	match text_node.text_type: 
		case (TextType.TEXT):
			return LeafNode(None, text_node.text)
		case (TextType.BOLD):
			return LeafNode("<b>",text_node.text)
		case (TextType.ITALIC):
			return LeafNode("<i>",text_node.text)
		case (TextType.CODE):
			return LeafNode("<code>", text_node.text)
		case (TextType.LINK):
			return LeafNode("<a>", text_node.text, {"href": text_node.url})
		case (TextType.IMAGE):
			return LeafNode("<img>", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise Exception ("No TextType identified")

#raw markdown string
def markdown_to_blocks(markdown):
	listblocks = list(filter(None,markdown.split("\n\n")))

	for block in listblocks:

		newblock = block.strip()

		if newblock == "" or newblock == '' or newblock == " " or newblock == "\n" or newblock is None:
			listblocks.remove(block)
		else:
			idxblock = listblocks.index(block)
			listblocks[idxblock] = newblock 
	return listblocks 


