import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from stringparse import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_different_text_and_type(self):
        node3 = TextNode("TextNode2", TextType.NORMAL)
        node4 = TextNode("TextNode3", TextType.ITALIC)
        self.assertNotEqual(node3, node4)


    def test_different_url(self):
        node5 = TextNode("Butt", TextType.LINK, "https://www.problem.com")
        node6 = TextNode("Butt", TextType.LINK, None)
        self.assertNotEqual(node5, node6)

    def test_different_type(self):
        node7 = TextNode("Test4", TextType.LINK, "https://www.imgur.com/A38597")
        node8 = TextNode("Test4", TextType.IMAGE, "https://www.imgur.com/A38597")
        self.assertNotEqual(node7, node8)


    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold_n2h(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "<b>")
        self.assertEqual(html_node.value, "bold text")


    def test_italic_n2h(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "<i>")
        self.assertEqual(html_node.value, "italic text")

    def test_code_n2h(self):
        node = TextNode("codey texty", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "<code>")
        self.assertEqual(html_node.value, "codey texty")

    def test_link_n2h(self):
        node = TextNode("a link to somewhere", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "<a>")
        self.assertEqual(html_node.value, "a link to somewhere")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_n2h(self):
        node = TextNode("fucing what", TextType.IMAGE, "https://www.imgur.com/A32587")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"<img>")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.imgur.com/A32587", "alt": "fucing what"})


    def test_TN_spl_bold_two(self):
        nodes = [TextNode("test 1a: **bold** stuff", TextType.TEXT), TextNode("test 1b: **more bold stuff**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "test 1a: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " stuff")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "test 1b: ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT) 
        self.assertEqual(new_nodes[4].text, "more bold stuff")
        self.assertEqual(new_nodes[4].text_type, TextType.BOLD)

    def test_TN_spl_ital_one(self):
        nodes = [TextNode("test 2a: some _italic_ stuff", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "test 2a: some ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " stuff")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)


    def test_TN_spl_code_four(self):
        nodes =  [TextNode("test 3a: `code` stuff", TextType.TEXT), 
                TextNode("test 3b: `more code stuff`", TextType.TEXT), 
                TextNode("`test 3c: stupid prepend` code stuff", TextType.TEXT), 
                TextNode("test 3d: `s`ingle code stuff", TextType.TEXT) ]

        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "test 3a: ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " stuff")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

        self.assertEqual(new_nodes[3].text, "test 3b: ")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT) 
        self.assertEqual(new_nodes[4].text, "more code stuff")
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)        

        self.assertEqual(new_nodes[5].text, "test 3c: stupid prepend")
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
        self.assertEqual(new_nodes[6].text, " code stuff")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)
        
        self.assertEqual(new_nodes[7].text, "test 3d: ")
        self.assertEqual(new_nodes[7].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[8].text, "s")
        self.assertEqual(new_nodes[8].text_type, TextType.CODE)
        self.assertEqual(new_nodes[9].text, "ingle code stuff")
        self.assertEqual(new_nodes[9].text_type, TextType.TEXT)

    def test_TN_spl_invalid_texttype(self):
        with self.assertRaises(Exception) as derp:
            nodes = [TextNode("test 4a: some bad stuff", TextType.POOP)]
        
        exc_msg = str(derp.exception)
        self.assertEqual(exc_msg, "POOP")

    def test_TN_spl_nontext_input(self):
        nodes = [TextNode("test 5a: already italicized", TextType.ITALIC)]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "test 5a: already italicized")
        self.assertEqual(new_nodes[0].text_type, TextType.ITALIC)

    def test_TN_spl_delim_mismatch(self):
        with self.assertRaises(Exception) as derp:
            nodes = [TextNode("test 6a: **bad** delim", TextType.TEXT)]
            new_nodes = split_nodes_delimiter(nodes, "**", TextType.CODE)

        exc_msg = str(derp.exception)
        self.assertEqual(exc_msg, "delimiter / TextType mismatch")

    def test_TN_spl_wrong_delim(self):
        with self.assertRaises(Exception) as derp:
            nodes = [TextNode("test 7a: &&bad&& delim", TextType.TEXT)]
            new_nodes = split_nodes_delimiter(nodes, "&&", TextType.BOLD)

        exc_msg = str(derp.exception)
        self.assertEqual(exc_msg, "no such delimiter, idiot")        


    def test_TN_spl_missing_one_delim(self):
        with self.assertRaises(Exception) as derp:
            nodes = [TextNode("test 8a: **missing delim", TextType.TEXT)]
            new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        exc_msg = str(derp.exception)
        self.assertEqual(exc_msg, "That's invalid Markdown syntax")        



if __name__ == "__main__":
    unittest.main()