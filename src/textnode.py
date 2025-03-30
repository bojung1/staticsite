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

