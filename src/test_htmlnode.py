import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello, World!, None, {'class': 'my-class'})")

    def test_props_to_html(self):
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", props={"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">Hello, world!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()