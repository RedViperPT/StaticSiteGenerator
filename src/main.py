#!/usr/bin/env python3

from textnode import TextNode, TextType
from htmlnode import LeafNode


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)  

if __name__ == "__main__":
    main()