# StaticSiteGenerator/src/block_to_html.py

from text_processing import markdown_to_blocks, block_to_block_type, text_to_textnodes
from textnode import TextNode, TextType, BlockType, text_node_to_html_node
from htmlnode import ParentNode
import textwrap

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        blk = block
        lines = blk.split("\n")
        if len(lines) >= 3 and lines[0].lstrip().startswith("```") and lines[-1].lstrip().startswith("```"):
            code_lines = lines[1:-1]
            code_content = "\n".join(code_lines)
            code_content = textwrap.dedent(code_content)
            if not code_content.endswith("\n"):
                code_content = code_content + "\n"
            code_text_node = TextNode(code_content, TextType.TEXT)
            code_child = text_node_to_html_node(code_text_node)
            code_parent = ParentNode("code", [code_child])
            node = ParentNode("pre", [code_parent])
            block_nodes.append(node)
            continue

        block_type = block_to_block_type(blk)

        if block_type == BlockType.PARAGRAPH:
            clean_text = " ".join(line.strip() for line in blk.split("\n"))
            children = text_to_children(clean_text)
            node = ParentNode("p", children)

        elif block_type == BlockType.HEADING:
            first_line = lines[0].lstrip()
            hash_part = first_line.split(" ")[0]
            level = len(hash_part)
            heading_text = first_line[level:].strip()
            children = text_to_children(heading_text)
            node = ParentNode(f"h{level}", children)

        elif block_type == BlockType.QUOTE:
            quote_lines = []
            for line in lines:
                stripped = line.lstrip()
                if stripped.startswith(">"):
                    stripped = stripped[1:]
                    if stripped.startswith(" "):
                        stripped = stripped[1:]
                quote_lines.append(stripped.rstrip())
            quote_text = " ".join(quote_lines)
            children = text_to_children(quote_text)
            node = ParentNode("blockquote", children)

        elif block_type == BlockType.UNORDERED_LIST:
            items = [line[2:].strip() if line.startswith("- ") else line.strip() for line in lines]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            node = ParentNode("ul", li_nodes)

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in lines:
                if "." in line:
                    dot_index = line.find(".")
                    items.append(line[dot_index + 1 :].strip())
                else:
                    items.append(line.strip())
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            node = ParentNode("ol", li_nodes)

        else:
            children = text_to_children(blk.strip())
            node = ParentNode("p", children)

        block_nodes.append(node)

    return ParentNode("div", block_nodes)
