import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
