import unittest
from blocktype import block_to_block_type, BlockType
from blocktype import markdown_to_html_node
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestBlockType(unittest.TestCase):

# Test an empty string
# result: paragraph
	def test_b2bt_empty(self):
		a = ""
		b = block_to_block_type(a)
		self.assertEqual(BlockType.PARAGRAPH,b)

	def test_b2bt_nothing_else(self):
		a = "gelrkughalriguhalgiuhalidfughaliguh"
		b = block_to_block_type(a)

		self.assertEqual(BlockType.PARAGRAPH,b)

	def test_b2bt_headings(self):
		h1 = "# heading 1"
		h2 = "## heading 2"
		h3 = "### heading 3"
		h4 = "#### heading 4"
		h5 = "##### heading 5"
		h6 = "###### heading 6"
		
		self.assertEqual(BlockType.HEADING,block_to_block_type(h1))
		self.assertEqual(BlockType.HEADING,block_to_block_type(h2))
		self.assertEqual(BlockType.HEADING,block_to_block_type(h3))
		self.assertEqual(BlockType.HEADING,block_to_block_type(h4))
		self.assertEqual(BlockType.HEADING,block_to_block_type(h5))
		self.assertEqual(BlockType.HEADING,block_to_block_type(h6))

	def test_b2bt_code(self):
		c1 = "``` some example ```"

		self.assertEqual(BlockType.CODE,block_to_block_type(c1))

	def test_b2bt_code_invalid(self):
		c2 = "``` some example"

		self.assertEqual(BlockType.PARAGRAPH,block_to_block_type(c2))


	def test_b2bt_quote(self):
		q1 = "> ewofjweofijwoefijowjif"

		self.assertEqual(BlockType.QUOTE, block_to_block_type(q1))


	def test_b2bt_quote_invalid(self):
		q2 = "#> ewofjweofijwoefijowjif"

		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(q2))


	def test_b2bt_uor_list(self):
		uo1 = "- surewhy not\n- this one too"

		self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(uo1))

	def test_b2bt_uor_list_invalid(self):
		uo2 = "-- should not work "

		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(uo2))

	def test_b2bt_or_list(self):
		o1 = "1. derp\n2.  herp"

		self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(o1))

	def test_b2bt_or_list(self):
		o1 = ".1. derp\n2.  herp"

		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(o1))

	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)


	def test_mixed_blocks(self):
		md = """
# Main Title

This is a paragraph with **bold** and _italic_ text.

## Subsection

* List item 1
* List item 2 with `code`

> A profound quote
> with multiple lines

```
def example_code():
	return "This is code that *shouldn't* be formatted"
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>Main Title</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><h2>Subsection</h2><ul><li>List item 1</li><li>List item 2 with <code>code</code></li></ul><blockquote>A profound quote with multiple lines</blockquote><pre><code>def example_code():\n	return \"This is code that *shouldn't* be formatted\"\n</code></pre></div>",
		)


	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)





if __name__ == "__main__":
	unittest.main()