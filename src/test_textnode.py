import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from stringparse import split_nodes_delimiter
from stringparse import split_nodes_link
from stringparse import split_nodes_image
from stringparse import text_to_textnodes
from stringparse import text_node_to_html_node
from stringparse import markdown_to_blocks


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
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")


    def test_italic_n2h(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code_n2h(self):
        node = TextNode("codey texty", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "codey texty")

    def test_link_n2h(self):
        node = TextNode("a link to somewhere", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "a link to somewhere")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image_n2h(self):
        node = TextNode("fucing what", TextType.IMAGE, "https://www.imgur.com/A32587")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag,"img")
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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],new_nodes,)


    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],new_nodes,)


    def test_split_images_one(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/2.png)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/2.png"),
            ],new_nodes,)


    def test_split_links_one(self):
        node = TextNode(
            "This is text with a link [L2](https://www.L2.com)",
            TextType.TEXT,
            )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("L2", TextType.LINK, "https://www.L2.com"),
            ],new_nodes,)

    def test_split_images_fourx(self):
        node = TextNode(
            "This is text with an ![I3image](https://i.imgur.com/I3.png) and also ![I4image](https://i.imgur.com/I4.gif) and also ![I5image](https://i.imgur.com/I5.gif) and finally ![I6image](https://i.imgur.com/I6.png)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("I3image", TextType.IMAGE, "https://i.imgur.com/I3.png"),
                TextNode(" and also ", TextType.TEXT),
                TextNode("I4image", TextType.IMAGE, "https://i.imgur.com/I4.gif"),
                TextNode(" and also ", TextType.TEXT),
                TextNode("I5image", TextType.IMAGE, "https://i.imgur.com/I5.gif"),
                TextNode(" and finally ", TextType.TEXT),
                TextNode("I6image", TextType.IMAGE, "https://i.imgur.com/I6.png"),

            ],new_nodes,)


    def test_split_links_leftover_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and more",
            TextType.TEXT,
            )
        
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" and more", TextType.TEXT),
            ],new_nodes,)

    def test_to_textnode_initial(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)  
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], new_nodes,)


# Test a string without any formatting
    def test_plain_text(self):
        input_text = "Just plain and simple text."
        # expected output might be a single text node 
        assert text_to_textnodes(input_text) == [TextNode("Just plain and simple text.", TextType.TEXT)]

# Test combining multiple styles in one string
    def test_combined_styles(self):
        input_text = "**bold text** with _italic_ and a `code` block."
        # expected range of nodes combining bold, italic, and code
        assert text_to_textnodes(input_text) == [
            TextNode("bold text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block.", TextType.TEXT)
        ]

# Test an empty string
    def test_empty_string(self):
        input_text = ""
        # expected output is an empty list
        assert text_to_textnodes(input_text) == []


    # Test a single bold word
    def test_single_bold(self):
        input_text = "**bold**"
        self.assertEqual(
            text_to_textnodes(input_text),
            [TextNode("bold", TextType.BOLD)]
        )
    
    # Test a single italic word
    def test_single_italic(self):
        input_text = "_italic_"
        self.assertEqual(
            text_to_textnodes(input_text),
            [TextNode("italic", TextType.ITALIC)]
        )


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])


    def test_markdown_to_blocks_tons_whitespace(self):
        md = """
This one has tons of whitespace 










Like way too much







And then for no reason, this
and this 

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This one has tons of whitespace",
                "Like way too much",
                "And then for no reason, this\nand this",
            ],
        )



if __name__ == "__main__":
    unittest.main()