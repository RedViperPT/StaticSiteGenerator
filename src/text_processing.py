from textnode import TextNode, TextType

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