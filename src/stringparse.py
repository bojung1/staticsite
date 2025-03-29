from textnode import TextType, TextNode 

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
