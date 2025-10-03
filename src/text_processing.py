from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        segments = text.split(delimiter)

        if len(segments) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: unclosed delimiter '{delimiter}' in text: {text}")
        
        for i, segment in enumerate(segments):
            if segment == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.TEXT))
            else:
                new_nodes.append(TextNode(segment, text_type))
    
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)"
    matches = []

    for match in re.finditer(pattern, text):
        if match.start() > 0 and text[match.start() - 1] == '\\':
            continue
        alt_text = match.group(1)
        url = match.group(2)
        matches.append((alt_text, url))

    return matches



def extract_markdown_links(text):
    pattern = r"\[([^\[\]]*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)"
    matches = []

    for match in re.finditer(pattern, text):
        if match.start() > 0 and text[match.start() - 1] == '\\':
            continue
        if match.start() > 0 and text[match.start() - 1] == '!':
            continue
        link_text = match.group(1)
        url = match.group(2)
        matches.append((link_text, url))

    return matches

