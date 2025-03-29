from enum import Enum
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"
	TEXT = "text" 


class TextNode():
	
	def __init__ (self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url 

	def __eq__(self, other):
		if not isinstance(other, TextNode):
			return False
		return self.text == other.text and self.text_type == other.text_type and self.url == other.url

	def __repr__ (self):
		#if self.url is not None:
		output = (f"TextNode({self.text}, {self.text_type.value}, {self.url})")
		#else:
		#	output = (f"TextNode({self.text}, {self.text_type.value})")
		return output


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