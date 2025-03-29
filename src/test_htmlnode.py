import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node1 = HTMLNode("a", "herpderp", [], {})
		node2 = HTMLNode("a", "herpderp", [], {})

		self.assertEqual(node1, node2)

	def test_eq_empty(self):
		node3 = HTMLNode()
		node4 = HTMLNode()

		self.assertEqual(node3, node4)

	def test_props(self):
		node5 = HTMLNode("<a>","superb", [], {"href": "https://www.google.com"})
		node6 = HTMLNode("<a>","superb", [], {"href": "https://www.google.com"})

		self.assertEqual(node5.props_to_html() , node6.props_to_html())

	def test_repr(self):
		node7 = HTMLNode("<p>","node78", [], {})
		node8 = HTMLNode("<p>","node78", [], {})

		self.assertEqual(repr(node7), repr(node8))


	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


	def test_leaf_with_attributes(self):
		node = LeafNode("a", "Click me", {"href": "https://example.com"})
		self.assertEqual(node.to_html(), '<a href="https://example.com">Click me</a>')


	def test_leaf_with_multiple_attributes(self):
		node = LeafNode("img", "Alt text", {"src": "image.jpg", "alt": "Alt text", "width": "100"})
		self.assertEqual(node.to_html(), '<img src="image.jpg" alt="Alt text" width="100">Alt text</img>')


	def test_leaf_with_no_tag(self):
		node = LeafNode(None, "Just some text")
		self.assertEqual(node.to_html(), "Just some text")


	def test_leaf_with_no_value(self):
		node = LeafNode("p", None)
		with self.assertRaises(ValueError):
			node.to_html()    

	def test_leaf_constructor(self):
		# This should pass
		node = LeafNode("div", "content")
		# Make sure children parameter isn't accepted or is ignored
		# The exact test will depend on your implementation     


	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
    	)

	def test_to_html_with_two_flat_children(self):
		child_node = LeafNode("butt","child1")
		child_node2 = LeafNode("butt2", "child2")
		parent_node = ParentNode("assface", [child_node, child_node2])
		self.assertEqual(
			parent_node.to_html(),
			"<assface><butt>child1</butt><butt2>child2</butt2></assface>",

		)


	def test_to_html_with_mult_children_and_grandkids(self):
		child_node1 = LeafNode("butt","child1")
		child_node2 = LeafNode("butt2", "child2")
		grandchild_node1 = LeafNode("cheeks","child3")
		grandchild_node2 = LeafNode("cheeks2","child4")
		child_node3 = ParentNode("assface2", [grandchild_node1, grandchild_node2])
		parent_node = ParentNode("assface", [child_node1, child_node2, child_node3])
		self.assertEqual(
			parent_node.to_html(),
			"<assface><butt>child1</butt><butt2>child2</butt2><assface2><cheeks>child3</cheeks><cheeks2>child4</cheeks2></assface2></assface>",
		)

	def test_to_html_with_somanygrandkids(self):
		g_g_gchild_node1 = LeafNode("assface5", "ggchild1")
		g_gchild_node1 = ParentNode("assface4",[g_g_gchild_node1])
		grandchild_node1 = ParentNode("assface3", [g_gchild_node1])
		child_node1 = ParentNode("assface2", [grandchild_node1])
		parent_node = ParentNode("assface", [child_node1])
	
		
		self.assertEqual(
			parent_node.to_html(),
			"<assface><assface2><assface3><assface4><assface5>ggchild1</assface5></assface4></assface3></assface2></assface>",
		)


	def test_to_empty_children(self):
		parent_node = ParentNode("shitbag", [])
		self.assertEqual(
			parent_node.to_html(),
			"<shitbag></shitbag>"
		)

	def test_to_tagless_parent(self):
		with self.assertRaises(ValueError) as derp: 
			child_node1 = LeafNode("butt","child1")
			parent_node = ParentNode(None, child_node1)
			parent_node.to_html()

		exc_msg = str(derp.exception)
		self.assertEqual(exc_msg, "ParentNodes must have a tag and this doesn't") 

	def test_to_kidless_parent(self):
		with self.assertRaises(ValueError) as derp:
			parent_node = ParentNode("assface", None)
			parent_node.to_html()

		exc_msg = str(derp.exception)
		self.assertEqual(exc_msg, "Children of ParentNodes must have a value, and this doesn't")

	def test_to_multi_prop_parent(self):
		grandchild_node1 = LeafNode("butt2", "cheeks")
		child_node1 = LeafNode("butt","child1")
		child_node2 = ParentNode("assface2", [grandchild_node1])
		parent_node = ParentNode("assface", [child_node1,child_node2], {"class": "container", "id": "main", "data-test": "true"})

		self.assertEqual(
			parent_node.to_html(),
			'<assface class="container" id="main" data-test="true"><butt>child1</butt><assface2><butt2>cheeks</butt2></assface2></assface>'
		)

	def test_special_characters_in_text(self):
		leaf = LeafNode("p", "This has <b>tags</b> & special chars")
		parent = ParentNode("div", [leaf])
		self.assertEqual(parent.to_html(), "<div><p>This has <b>tags</b> & special chars</p></div>")	

	def test_special_characters_in_attributes(self):
		leaf = LeafNode("span", "Text")
		parent = ParentNode("div", [leaf], {"data-value": "a < b & c > d"})
		self.assertEqual(parent.to_html(), '<div data-value="a < b & c > d"><span>Text</span></div>')


# Complex structures tests
	def test_html_document_structure(self):
		paragraph = LeafNode("p", "Hello World")
		div = ParentNode("div", [paragraph])
		body = ParentNode("body", [div])
		html = ParentNode("html", [body])
		self.assertEqual(html.to_html(), "<html><body><div><p>Hello World</p></div></body></html>")

	def test_list_structure(self):
		item1 = LeafNode("li", "Item 1")
		item2 = LeafNode("li", "Item 2")
		item3 = LeafNode("li", "Item 3")
		ul = ParentNode("ul", [item1, item2, item3])
		self.assertEqual(ul.to_html(), "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

	def test_table_structure(self):
		cell1 = LeafNode("td", "Cell 1")
		cell2 = LeafNode("td", "Cell 2")
		row = ParentNode("tr", [cell1, cell2])
		table = ParentNode("table", [row])
		self.assertEqual(table.to_html(), "<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>")


if __name__ == "__main__":
    unittest.main()
