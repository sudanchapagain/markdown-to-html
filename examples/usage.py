import os

import md2html
import tempfile

md_text = r"""
# Hello World

## This is a Subheading

- Item 1
- Item 2
- Item 3

```python
def hello():
    print("Hello, World!")
```

Here is a blockquote:

> This is a blockquote.
> It can span multiple lines.

link: [example](https://www.example.com)

And here is some **bold text** and some *italic text*.

inline code too `print("Hello, World!")`

paragraphs are separated by a blank line. paragraphs are separated by a blank line.
paragraphs are separated by a blank line. paragraphs are separated by a blank line.

paragraphs are separated by a blank line. paragraphs are separated by a blank line.
paragraphs are separated by a blank line. paragraphs are separated by a blank line.
"""

with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8") as tmp:
    tmp.write(md_text)
    tmp_path = tmp.name

html_output = md2html.convert(tmp_path, False, "") # source (string), output as file (bool), output file name (string)
print(html_output)
os.remove(tmp_path)
