import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()