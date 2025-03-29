from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

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



def main():
	print ("hello world")
	derp = TextNode("derp", TextType.LINK, "https://www.boot.dev")
	print (derp)


if __name__ == "__main__":
    main()