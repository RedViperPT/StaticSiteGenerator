import unittest

from text_processing import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This has **bold** and `code` and *italic*", TextType.TEXT)
        # First split for bold
        nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split for code
        nodes_after_code = split_nodes_delimiter(nodes_after_bold, "`", TextType.CODE)
        # Finally split for italic
        new_nodes = split_nodes_delimiter(nodes_after_code, "*", TextType.ITALIC)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("text at end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("text at end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_only_delimited_content(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_multiple_same_delimiters(self):
        node = TextNode("This has **bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_nodes_unchanged(self):
        node1 = TextNode("This is text", TextType.TEXT)
        node2 = TextNode("This is bold", TextType.BOLD)  # Should remain unchanged
        node3 = TextNode("This is more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        expected = [
            TextNode("This is text", TextType.TEXT),  # No delimiters, so unchanged
            TextNode("This is bold", TextType.BOLD),  # Non-text type, so unchanged
            TextNode("This is more text", TextType.TEXT),  # No delimiters, so unchanged
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter_raises_error(self):
        node = TextNode("This has **unclosed delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: unclosed delimiter '**' in text: This has **unclosed delimiter")

    def test_empty_segments_ignored(self):
        node = TextNode("Text ** ** with empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode(" ", TextType.BOLD),
            TextNode(" with empty", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_nested_delimiters_as_text(self):
        # This tests that delimiters inside other delimiters are treated as text
        # when processed in the correct order
        node = TextNode("Text with `code **bold** inside` code", TextType.TEXT)
        # First process code delimiters
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        # The bold inside code should remain as text within the code block
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code **bold** inside", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_code, expected)

if __name__ == "__main__":
    unittest.main()