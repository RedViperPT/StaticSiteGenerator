import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestParentNode(unittest.TestCase):
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

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        child3 = LeafNode("p", "Third paragraph")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p><p>Third paragraph</p></div>"
        )

    def test_to_html_with_mixed_children(self):
        child1 = LeafNode("b", "bold text")
        child2 = LeafNode(None, "normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, " more normal text")
        parent_node = ParentNode("p", [child1, child2, child3, child4])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>bold text</b>normal text<i>italic text</i> more normal text</p>"
        )

    def test_to_html_with_props(self):
        child1 = LeafNode("span", "child with props", {"class": "child-class"})
        child2 = LeafNode("a", "link", {"href": "https://example.com"})
        parent_node = ParentNode("div", [child1, child2], {"id": "parent", "class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent" class="container"><span class="child-class">child with props</span><a href="https://example.com">link</a></div>'
        )

    def test_to_html_with_nested_parents(self):
        grandchild1 = LeafNode("b", "bold grandchild")
        grandchild2 = LeafNode("i", "italic grandchild")
        child1 = ParentNode("span", [grandchild1, grandchild2])
        child2 = LeafNode("p", "simple child")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>bold grandchild</b><i>italic grandchild</i></span><p>simple child</p></div>"
        )

    def test_to_html_with_empty_children_raises_error(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have children")

    def test_to_html_with_none_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have children")

    def test_to_html_with_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test_to_html_complex_structure(self):
        # Building a more complex HTML structure
        link = LeafNode("a", "Click me!", {"href": "#", "target": "_blank"})
        strong_text = LeafNode("strong", "Important!")
        paragraph = ParentNode("p", [strong_text, LeafNode(None, " Some text. "), link])
        list_item1 = LeafNode("li", "Item 1")
        list_item2 = LeafNode("li", "Item 2")
        list_node = ParentNode("ul", [list_item1, list_item2])
        container = ParentNode("div", [paragraph, list_node], {"class": "main-content"})
        
        self.assertEqual(
            container.to_html(),
            '<div class="main-content"><p><strong>Important!</strong> Some text. <a href="#" target="_blank">Click me!</a></p><ul><li>Item 1</li><li>Item 2</li></ul></div>'
        )

    def test_to_html_with_only_leaf_children(self):
        children = [
            LeafNode("h1", "Title"),
            LeafNode("p", "Paragraph 1"),
            LeafNode("p", "Paragraph 2"),
            LeafNode("footer", "Footer content")
        ]
        parent_node = ParentNode("article", children, {"id": "main-article"})
        self.assertEqual(
            parent_node.to_html(),
            '<article id="main-article"><h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p><footer>Footer content</footer></article>'
        )

    def test_to_html_deep_nesting(self):
        level4 = LeafNode("em", "deeply nested")
        level3 = ParentNode("span", [level4])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
        root = ParentNode("main", [level1])
        
        self.assertEqual(
            root.to_html(),
            "<main><section><div><span><em>deeply nested</em></span></div></section></main>"
        )

if __name__ == "__main__":
    unittest.main()