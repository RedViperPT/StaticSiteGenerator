#!/usr/bin/env python3

from textnode import TextNode, TextType
from htmlnode import LeafNode
import os
import shutil


def copy_static_to_public(dir):
    source_dir = os.path.join(dir, "static")
    target_dir = os.path.join(dir, "public")
    
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")
    
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    def copy_recursive(source, target):
        os.makedirs(target, exist_ok=True)
        
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            target_path = os.path.join(target, item)
            
            if os.path.isdir(source_path):
                copy_recursive(source_path, target_path)
            else:
                shutil.copy(source_path, target_path)
    
    copy_recursive(source_dir, target_dir)

def main():
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    static_path = os.path.join(current_dir, "static")
    if not os.path.exists(static_path):
        print(f"Static folder not found at: {static_path}")
        return
    
    print("Static folder found, copying to public...")
    copy_static_to_public(current_dir)
    print("Copy completed!")

if __name__ == "__main__":
    main()