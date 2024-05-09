#!/usr/bin/python3

"""
    Convert Markdown file to HTML file
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(markdown_text):
    """Convert Markdown to HTML"""

    lines = markdown_text.split('\n')
    html_lines = []
    in_ul = False
    in_ol = False
    in_paragraph = False

    for line in lines:
        if line.startswith('#'):
            html_lines.append(f'<h1>{line.strip("# ").strip()}</h1>')
            in_ul = False
            in_ol = False
            in_paragraph = False
        elif line.startswith('* '):
            if not in_ul:
                if in_ol:
                    html_lines.append('</ol>')
                    in_ol = False
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append('<ul>')
                in_ul = True
            html_lines.append(f'<li>{apply_formatting(line.strip("* ").strip())}</li>')
        elif line.startswith('1. '):
            if not in_ol:
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                if in_paragraph:
                    html_lines.append('</p>')
                    in_paragraph = False
                html_lines.append('<ol>')
                in_ol = True
            html_lines.append(f'<li>{apply_formatting(line.strip("1. ").strip())}</li>')
        elif line.strip() == '':
            if in_ul:
                html_lines.append('</ul>')
                in_ul = False
            elif in_ol:
                html_lines.append('</ol>')
                in_ol = False
            if in_paragraph:
                html_lines.append('</p>')
                in_paragraph = False
        else:
            if not in_paragraph:
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                elif in_ol:
                    html_lines.append('</ol>')
                    in_ol = False
                html_lines.append('<p>')
                in_paragraph = True
            html_lines.append(apply_formatting(line))

    if in_ul:
        html_lines.append('</ul>')
    elif in_ol:
        html_lines.append('</ol>')
    if in_paragraph:
        html_lines.append('</p>')
    return '\n'.join(html_lines)

def apply_formatting(text):
    """Apply Markdown formatting"""

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    text = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), text)
    text = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), text)
    return text

def main():
    """Main function"""

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as f:
        markdown_text = f.read()

    html_text = convert_markdown_to_html(markdown_text)

    with open(output_file, 'w') as f:
        f.write(html_text)

if __name__ == "__main__":
    main()
