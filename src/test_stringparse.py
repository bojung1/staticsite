import unittest
from main import extract_title

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import TextNode, TextType
from stringparse import extract_markdown_images
from stringparse import extract_markdown_links

class TestExtractRegex(unittest.TestCase):

	def test_extract_markdown_images(self):
		matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


	def test_extract_markdown_links(self):
		matches  = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
		self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


	def test_extract_md_bad_format_image(self):
		matches = extract_markdown_images("This is text with an !image](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([], matches)


	def test_extract_md_bad_format_links(self):
		matches = extract_markdown_links("This is text with an ![image]https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([], matches)


	def test_markdown_extract_title(self):
		matches = extract_title("./content/index.md")
		self.assertEqual("Tolkien Fan Club", matches)




if __name__ == "__main__":
    unittest.main()
