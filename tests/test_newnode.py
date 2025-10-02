import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_ineq2(self):
        node = TextNode("This isn't a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="http://example.com")
        self.assertEqual(node, node2)

    def test_ineq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="http://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, url="http://different.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()