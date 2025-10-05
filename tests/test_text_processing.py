import unittest

from text_processing import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
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
        nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes_after_code = split_nodes_delimiter(nodes_after_bold, "`", TextType.CODE)
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
        node2 = TextNode("This is bold", TextType.BOLD) 
        node3 = TextNode("This is more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        expected = [
            TextNode("This is text", TextType.TEXT),
            TextNode("This is bold", TextType.BOLD),
            TextNode("This is more text", TextType.TEXT),
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
        node = TextNode("Text with `code **bold** inside` code", TextType.TEXT)
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code **bold** inside", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_code, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_single_image(self):
        text = "This is text with an ![image](https://i.imgur.com/example.png)"
        matches = extract_markdown_images(text)
        expected = [("image", "https://i.imgur.com/example.png")]
        self.assertListEqual(expected, matches)


    def test_extract_multiple_images(self):
        text = "![first](http://example.com/1.png) and ![second](http://site.com/2.jpg)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "http://example.com/1.png"),
            ("second", "http://site.com/2.jpg")
        ]
        self.assertListEqual(expected, matches)


    def test_extract_no_images(self):
        text = "This is plain text with no images"
        matches = extract_markdown_images(text)
        expected = []
        self.assertListEqual(expected, matches)


    def test_extract_image_with_spaces_in_alt(self):
        text = "![my alt text](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        expected = [("my alt text", "https://example.com/image.png")]
        self.assertListEqual(expected, matches)


    def test_extract_image_with_special_chars_in_url(self):
        text = "![icon](https://example.com/image.png?width=100&height=200)"
        matches = extract_markdown_images(text)
        expected = [("icon", "https://example.com/image.png?width=100&height=200")]
        self.assertListEqual(expected, matches)


    def test_extract_image_with_empty_alt_text(self):
        text = "Here is an image ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        expected = [("", "https://example.com/image.png")]
        self.assertListEqual(expected, matches)


    def test_extract_escaped_image_syntax(self):
        text = r"This is escaped \!\[not an image\](https://example.com/fake.png)"
        matches = extract_markdown_images(text)
        expected = []
        self.assertListEqual(expected, matches)


    def test_extract_image_with_parentheses_in_url(self):
        text = "![wiki](https://en.wikipedia.org/wiki/Example_(disambiguation))"
        matches = extract_markdown_images(text)
        expected = [("wiki", "https://en.wikipedia.org/wiki/Example_(disambiguation)")]
        self.assertListEqual(expected, matches)


    def test_extract_adjacent_images(self):
        text = "![first](1.png)![second](2.png)![third](3.jpg)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "1.png"),
            ("second", "2.png"),
            ("third", "3.jpg")
        ]
        self.assertListEqual(expected, matches)


    def test_extract_image_with_unicode_in_alt(self):
        text = "![图片 🎨](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        expected = [("图片 🎨", "https://example.com/image.png")]
        self.assertListEqual(expected, matches)


    def test_extract_image_with_data_url(self):
        text = "![icon](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA)"
        matches = extract_markdown_images(text)
        expected = [("icon", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA")]
        self.assertListEqual(expected, matches)


    def test_extract_image_with_very_long_url(self):
        long_url = "https://example.com/" + "a" * 1000 + ".png"
        text = f"![long]({long_url})"
        matches = extract_markdown_images(text)
        expected = [("long", long_url)]
        self.assertListEqual(expected, matches)


    def test_extract_image_with_uppercase_scheme(self):
        text = "![image](HTTPS://EXAMPLE.COM/image.png)"
        matches = extract_markdown_images(text)
        expected = [("image", "HTTPS://EXAMPLE.COM/image.png")]
        self.assertListEqual(expected, matches)


    def test_return_type_is_list(self):
        text = "![img](url.png)"
        matches = extract_markdown_images(text)
        self.assertIsInstance(matches, list)
        self.assertGreater(len(matches), 0)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        text = "This is [a link](https://www.example.com)"
        matches = extract_markdown_links(text)
        expected = [("a link", "https://www.example.com")]
        self.assertListEqual(expected, matches)


    def test_extract_multiple_links(self):
        text = "[first](http://site1.com) and [second](http://site2.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "http://site1.com"),
            ("second", "http://site2.com")
        ]
        self.assertListEqual(expected, matches)


    def test_distinguish_links_from_images(self):
        text = "![image](pic.png) is not [link](page.html)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        
        expected_links = [("link", "page.html")]
        expected_images = [("image", "pic.png")]
        self.assertListEqual(expected_links, link_matches)
        self.assertListEqual(expected_images, image_matches)


    def test_extract_link_with_title(self):
        text = "[Click here for more info](https://docs.example.com)"
        matches = extract_markdown_links(text)
        expected = [("Click here for more info", "https://docs.example.com")]
        self.assertListEqual(expected, matches)


    def test_extract_relative_links(self):
        text = "[About](/about) and [Contact](./contact.html)"
        matches = extract_markdown_links(text)
        expected = [
            ("About", "/about"),
            ("Contact", "./contact.html")
        ]
        self.assertListEqual(expected, matches)


    def test_extract_link_with_empty_text(self):
        text = "Check this out [](https://example.com)"
        matches = extract_markdown_links(text)
        expected = [("", "https://example.com")]
        self.assertListEqual(expected, matches)


    def test_extract_escaped_link_syntax(self):
        text = r"This is escaped \[not a link\](https://example.com)"
        matches = extract_markdown_links(text)
        expected = []
        self.assertListEqual(expected, matches)


    def test_extract_link_with_parentheses_in_url(self):
        text = "[Wikipedia](https://en.wikipedia.org/wiki/Python_(programming_language))"
        matches = extract_markdown_links(text)
        expected = [("Wikipedia", "https://en.wikipedia.org/wiki/Python_(programming_language)")]
        self.assertListEqual(expected, matches)


    def test_extract_adjacent_links(self):
        text = "[first](1.html)[second](2.html)[third](3.html)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "1.html"),
            ("second", "2.html"),
            ("third", "3.html")
        ]
        self.assertListEqual(expected, matches)


    def test_extract_link_with_title_attribute(self):
        text = '[link](https://example.com "This is a title")'
        matches = extract_markdown_links(text)
        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], "link")
        self.assertIn("https://example.com", matches[0][1])


    def test_extract_link_with_unicode_in_text(self):
        text = "[文档 📚](https://example.com/docs)"
        matches = extract_markdown_links(text)
        expected = [("文档 📚", "https://example.com/docs")]
        self.assertListEqual(expected, matches)


    def test_extract_link_with_very_long_url(self):
        long_url = "https://example.com/" + "b" * 1000 + ".html"
        text = f"[long link]({long_url})"
        matches = extract_markdown_links(text)
        expected = [("long link", long_url)]
        self.assertListEqual(expected, matches)


    def test_return_type_is_list(self):
        text = "[link](url.html)"
        matches = extract_markdown_links(text)
        self.assertIsInstance(matches, list)
        self.assertGreater(len(matches), 0)

class TestEdgeCases(unittest.TestCase):
    def test_empty_string(self):
        expected = []
        self.assertListEqual(expected, extract_markdown_images(""))
        self.assertListEqual(expected, extract_markdown_links(""))


    def test_malformed_syntax(self):
        text = "![missing bracket (http://example.com) and [missing paren](/link"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        expected = []
        self.assertListEqual(expected, image_matches)
        self.assertListEqual(expected, link_matches)


    def test_nested_brackets(self):
        text = "[link [nested]](http://example.com)"
        matches = extract_markdown_links(text)
        self.assertIsInstance(matches, list)
        if len(matches) > 0:
            self.assertEqual(matches[0][1], "http://example.com")


    def test_mixed_content(self):
        text = """
        Welcome! ![Logo](logo.png) Check out our [documentation](/docs)
        for more [info](help.html). Here's another ![icon](icon.jpg).
        """
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        expected_images = [("Logo", "logo.png"), ("icon", "icon.jpg")]
        expected_links = [("documentation", "/docs"), ("info", "help.html")]
        
        self.assertListEqual(expected_images, image_matches)
        self.assertListEqual(expected_links, link_matches)


    def test_adjacent_mixed_markup(self):
        text = "text![img](url.png)[link](url.html)text"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        expected_images = [("img", "url.png")]
        expected_links = [("link", "url.html")]
        
        self.assertListEqual(expected_images, image_matches)
        self.assertListEqual(expected_links, link_matches)


    def test_incomplete_closing_image(self):
        text = "![alt](url.png and more text"
        matches = extract_markdown_images(text)
        self.assertIsInstance(matches, list)


    def test_incomplete_closing_link(self):
        text = "[text](url.html and more text"
        matches = extract_markdown_links(text)
        self.assertIsInstance(matches, list)


    def test_return_type_with_no_matches(self):
        text = "Plain text with no markdown"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        
        self.assertIsInstance(image_matches, list)
        self.assertIsInstance(link_matches, list)
        self.assertEqual(len(image_matches), 0)
        self.assertEqual(len(link_matches), 0)


    def test_whitespace_in_urls(self):
        text = "![img](url with spaces.png)"
        matches = extract_markdown_images(text)
        self.assertIsInstance(matches, list)


    def test_markdown_in_code_context(self):
        text = "`![not an image](fake.png)` and `[not a link](fake.html)`"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertIsInstance(image_matches, list)
        self.assertIsInstance(link_matches, list)

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://example.com/image.png) and ![another](https://example.com/another.jpg)"
        result = extract_markdown_images(text)
        expected = [
            ("image", "https://example.com/image.png"),
            ("another", "https://example.com/another.jpg")
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://example.com) and [another](https://example.com/another)"
        result = extract_markdown_links(text)
        expected = [
            ("link", "https://example.com"),
            ("another", "https://example.com/another")
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_with_links_present(self):
        text = "This has ![image](https://example.com/img.png) and [link](https://example.com) but only images should be extracted"
        result = extract_markdown_images(text)
        expected = [("image", "https://example.com/img.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_with_images_present(self):
        text = "This has ![image](https://example.com/img.png) and [link](https://example.com) but only links should be extracted"
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and [another](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_single_link(self):
        node = TextNode(
            "Click [here](https://example.com) for more info",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" for more info", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_at_start(self):
        node = TextNode(
            "[start link](https://start.com) and then text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "https://start.com"),
            TextNode(" and then text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_at_end(self):
        node = TextNode(
            "Text at start and then [end link](https://end.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text at start and then ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://end.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_only_link(self):
        node = TextNode(
            "[only link](https://only.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://only.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode(
            "This is just plain text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_multiple_nodes(self):
        node1 = TextNode("Text with [link1](https://link1.com)", TextType.TEXT)
        node2 = TextNode("This is bold", TextType.BOLD)
        node3 = TextNode("More text [link2](https://link2.com)", TextType.TEXT)
        
        new_nodes = split_nodes_link([node1, node2, node3])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://link1.com"),
            TextNode("This is bold", TextType.BOLD),
            TextNode("More text ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://link2.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_non_text_nodes_unchanged(self):
        node1 = TextNode("This is bold", TextType.BOLD)
        node2 = TextNode("This is italic", TextType.ITALIC)
        node3 = TextNode("This is code", TextType.CODE)
        
        new_nodes = split_nodes_link([node1, node2, node3])
        expected = [node1, node2, node3]
        self.assertEqual(new_nodes, expected)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png) and ![another](https://example.com/another.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.IMAGE, "https://example.com/another.jpg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_single_image(self):
        node = TextNode(
            "Look at this ![cool image](https://example.com/cool.png) isn't it great?",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Look at this ", TextType.TEXT),
            TextNode("cool image", TextType.IMAGE, "https://example.com/cool.png"),
            TextNode(" isn't it great?", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_at_start(self):
        node = TextNode(
            "![first image](https://first.com/img.png) and then text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first image", TextType.IMAGE, "https://first.com/img.png"),
            TextNode(" and then text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_at_end(self):
        node = TextNode(
            "Text at start and then ![last image](https://last.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text at start and then ", TextType.TEXT),
            TextNode("last image", TextType.IMAGE, "https://last.com/img.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_only_image(self):
        node = TextNode(
            "![only image](https://only.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "https://only.com/img.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode(
            "This is just plain text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_multiple_nodes(self):
        node1 = TextNode("Text with ![image1](https://img1.com)", TextType.TEXT)
        node2 = TextNode("This is code", TextType.CODE)
        node3 = TextNode("More text ![image2](https://img2.com)", TextType.TEXT)
        
        new_nodes = split_nodes_image([node1, node2, node3])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://img1.com"),
            TextNode("This is code", TextType.CODE),
            TextNode("More text ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://img2.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_non_text_nodes_unchanged(self):
        node1 = TextNode("This is bold", TextType.BOLD)
        node2 = TextNode("This is italic", TextType.ITALIC)
        node3 = TextNode("This is a link", TextType.LINK, "https://example.com")
        
        new_nodes = split_nodes_image([node1, node2, node3])
        expected = [node1, node2, node3]
        self.assertEqual(new_nodes, expected)

class TestMixedContent(unittest.TestCase):
    def test_text_with_both_images_and_links(self):
        node = TextNode(
            "This has ![image](https://img.com) and [link](https://link.com) and ![another image](https://img2.com)",
            TextType.TEXT,
        )
        after_images = split_nodes_image([node])
        final_nodes = split_nodes_link(after_images)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://link.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another image", TextType.IMAGE, "https://img2.com"),
        ]
        self.assertEqual(final_nodes, expected)

    def test_complex_nested_processing(self):
        node = TextNode(
            "Start with **bold** then ![image](https://img.com) then `code` and [link](https://link.com) end",
            TextType.TEXT,
        )
        after_images = split_nodes_image([node])
        after_links = split_nodes_link(after_images)
        
        expected = [
            TextNode("Start with **bold** then ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://img.com"),
            TextNode(" then `code` and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://link.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(after_links, expected)

    def test_empty_text_after_splitting(self):
        node = TextNode(
            "[link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_adjacent_links(self):
        node = TextNode(
            "[one](https://one.com)[two](https://two.com)[three](https://three.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("one", TextType.LINK, "https://one.com"),
            TextNode("two", TextType.LINK, "https://two.com"),
            TextNode("three", TextType.LINK, "https://three.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_adjacent_images(self):
        node = TextNode(
            "![one](https://one.com)![two](https://two.com)![three](https://three.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("one", TextType.IMAGE, "https://one.com"),
            TextNode("two", TextType.IMAGE, "https://two.com"),
            TextNode("three", TextType.IMAGE, "https://three.com"),
        ]
        self.assertEqual(new_nodes, expected)

class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_plain_text_only(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text with no formatting", TextType.TEXT)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_comprehensive(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
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
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_single_formatting_types(self):
        test_cases = [
            ("**bold text**", [TextNode("bold text", TextType.BOLD)]),
            ("_italic text_", [TextNode("italic text", TextType.ITALIC)]),
            ("`code block`", [TextNode("code block", TextType.CODE)]),
            ("[link text](https://example.com)", [TextNode("link text", TextType.LINK, "https://example.com")]),
            ("![alt text](https://example.com/image.jpg)", [TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg")]),
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                nodes = text_to_textnodes(text)
                self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_bold_multiple(self):
        text = "**First bold** some text **second bold**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("First bold", TextType.BOLD),
            TextNode(" some text ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_italic_multiple(self):
        text = "_First italic_ some text _second italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("First italic", TextType.ITALIC),
            TextNode(" some text ", TextType.TEXT),
            TextNode("second italic", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_code_multiple(self):
        text = "`first code` and `second code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("first code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_mixed_formatting(self):
        text = "Start **bold** then _italic_ then `code` end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_adjacent_formatting(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_formatting_at_boundaries(self):
        test_cases = [
            ("**bold at start** and text", [
                TextNode("bold at start", TextType.BOLD),
                TextNode(" and text", TextType.TEXT),
            ]),
            ("text and **bold at end**", [
                TextNode("text and ", TextType.TEXT),
                TextNode("bold at end", TextType.BOLD),
            ]),
            ("**only bold**", [
                TextNode("only bold", TextType.BOLD),
            ]),
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                nodes = text_to_textnodes(text)
                self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_preserves_whitespace(self):
        text = "**bold**    _italic_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("    ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_formatting_inside_links_preserved(self):
        text = "Check [this **important** link](https://example.com) out"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this **important** link", TextType.LINK, "https://example.com"),
            TextNode(" out", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_formatting_inside_images_preserved(self):
        text = "See ![image with **bold** alt](image.png) here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("image with **bold** alt", TextType.IMAGE, "image.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_formatting_inside_code_preserved(self):
        text = "This `code has **bold** and _italic_` in it"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("code has **bold** and _italic_", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_multiple_links(self):
        text = "[first](url1.com) and [second](url2.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("first", TextType.LINK, "url1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.LINK, "url2.com"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_multiple_images(self):
        text = "![first](img1.png) and ![second](img2.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("first", TextType.IMAGE, "img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "img2.png"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_links_and_images_mixed(self):
        text = "![image](img.png) with [link](url.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_complex_real_world(self):
        text = "Check out ![logo](logo.png) on **our website** at [example.com](https://example.com) for `code samples` and _documentation_!"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("logo", TextType.IMAGE, "logo.png"),
            TextNode(" on ", TextType.TEXT),
            TextNode("our website", TextType.BOLD),
            TextNode(" at ", TextType.TEXT),
            TextNode("example.com", TextType.LINK, "https://example.com"),
            TextNode(" for ", TextType.TEXT),
            TextNode("code samples", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("documentation", TextType.ITALIC),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_unclosed_bold_raises_error(self):
        text = "This has **unclosed bold"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertIn("unclosed delimiter", str(context.exception).lower())
    
    def test_text_to_textnodes_unclosed_italic_raises_error(self):
        text = "This has _unclosed italic"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertIn("unclosed delimiter", str(context.exception).lower())
    
    def test_text_to_textnodes_unclosed_code_raises_error(self):
        text = "This has `unclosed code"
        with self.assertRaises(ValueError) as context:
            text_to_textnodes(text)
        self.assertIn("unclosed delimiter", str(context.exception).lower())
    
    def test_text_to_textnodes_url_with_parentheses(self):
        text = "[Wikipedia](https://en.wikipedia.org/wiki/Python_(programming_language))"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Wikipedia", TextType.LINK, "https://en.wikipedia.org/wiki/Python_(programming_language)")
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_special_characters_in_text(self):
        text = "Email: test@example.com & phone: 555-1234"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Email: test@example.com & phone: 555-1234", TextType.TEXT)]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_newlines_in_text(self):
        text = "Line 1\nLine 2"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Line 1\nLine 2", TextType.TEXT)]
        self.assertEqual(nodes, expected)

class TestMarkdownToBlocks(unittest.TestCase):

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

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph"])    

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_excessive_newlines(self):
        md = "First paragraph\n\n\n\nSecond paragraph\n\n\n\n\nThird paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph"
            ]
        )

if __name__ == '__main__':
    unittest.main()
