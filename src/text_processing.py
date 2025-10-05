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

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(node)
            continue
        
        temp_text = text
        segments = []
        
        for link_text, url in links:
            link_pattern = f"[{link_text}]({url})"
            if link_pattern in temp_text:
                before, after = temp_text.split(link_pattern, 1)
                if before:
                    segments.append(TextNode(before, TextType.TEXT))
                segments.append(TextNode(link_text, TextType.LINK, url))
                temp_text = after
            else:
                if temp_text:
                    segments.append(TextNode(temp_text, TextType.TEXT))
                break
        if temp_text and (not segments or segments[-1].text_type != TextType.TEXT):
            segments.append(TextNode(temp_text, TextType.TEXT))
        
        new_nodes.extend(segments)
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(node)
            continue
        
        temp_text = text
        segments = []
        
        for alt_text, url in images:
            image_pattern = f"![{alt_text}]({url})"
            if image_pattern in temp_text:
                before, after = temp_text.split(image_pattern, 1)
                if before:
                    segments.append(TextNode(before, TextType.TEXT))
                segments.append(TextNode(alt_text, TextType.IMAGE, url))
                temp_text = after
            else:
                if temp_text:
                    segments.append(TextNode(temp_text, TextType.TEXT))
                break
        
        if temp_text and (not segments or segments[-1].text_type != TextType.TEXT):
            segments.append(TextNode(temp_text, TextType.TEXT))
        
        new_nodes.extend(segments)
    
    return new_nodes

def text_to_textnodes(text):
    if text == "":
        return [TextNode("", TextType.TEXT)]

    nodes = [TextNode(text, TextType.TEXT)] 
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]
