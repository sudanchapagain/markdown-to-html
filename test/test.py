import md2html

heading1_res = (
    "<h3>test <strong>what</strong>?</h3>\n<h3>testing <em>italic</em></h3>\n"
)
heading2_res = "<h1>Hello World 1</h1>\n<h2>Hello World 2</h2>\n<h3>Hello World 3</h3>\n<h4>Hello World 4</h4>\n<h5>Hello World 5</h5>\n<h6>Hello World 6</h6>\n<p>####### Hello World 7 should not work</p>\n"
paragraph_res = "<p>paragraph <em>bold</em> <strong>italic</strong> is reversed.</p>\n<p>what if para in different</p>\n<p>lines cause eighty</p>\n<p>lines limit.</p>\n"
blockquote_res = "<blockquote>support\nthis</blockquote>\n<p>></p>\n<blockquote>question mark. markdown and me lazy moment</blockquote>\n<p>breaker paragraph</p>\n<blockquote>blockquote\nblockquote</blockquote>\n<p>what if this. bruh markdown. why is this blockquote</p>\n<blockquote>maybe for this?</blockquote>\n<p>this</p>\n<p>this</p>\n<p>this</p>\n<p>></p>\n<blockquote>this would continue it as single one</blockquote>\n<p>></p>\n<blockquote>hmm</blockquote>\n"
codeblock_res = '<pre><code>fn main(){\n    println!("Hello");\n}\nwhat if random text and *italic* **bold**\n</code></pre>'
list_res = "<ul>\n<li>bullet or not</li>\n<li>bull</li>\n<li>ball</li>\n<li>bob</li>\n<li>what</li>\n</ul>\n<ul>\n<li>new list question mark</li>\n<li>1029</li>\n</ul>\n"
inline_code_res = "<p>what happens to <code>inline code?</code></p>\n"
link_res = '<p>i can afford links now <a href="./src/main.rs">teehee</a></p>\n'


def test_heading():
    headings_emphasis = "./test/1_heading_emphasis.md"
    res = md2html.convert(headings_emphasis, False, "")
    assert res == heading1_res

    headings = "./test/1_heading.md"
    res = md2html.convert(headings, False, "")
    assert res == heading2_res


def test_paragraph():
    paragraphs = "./test/2_paragraph.md"
    res = md2html.convert(paragraphs, False, "")
    assert res == paragraph_res


def test_blockquote():
    blockquotes = "./test/3_blockquote.md"
    res = md2html.convert(blockquotes, False, "")
    assert res == blockquote_res


def test_codeblock():
    codeblocks = "./test/4_codeblock.md"
    res = md2html.convert(codeblocks, False, "")
    assert res == codeblock_res


def test_list():
    lists = "./test/5_list.md"
    res = md2html.convert(lists, False, "")
    assert res == list_res


def test_inline_code():
    inline_codes = "./test/6_inline_code.md"
    res = md2html.convert(inline_codes, False, "")
    assert res == inline_code_res


def test_link():
    links = "./test/7_link.md"
    res = md2html.convert(links, False, "")
    assert res == link_res


def main():
    test_heading()
    test_paragraph()
    test_blockquote()
    test_codeblock()
    test_list()
    test_inline_code()
    test_link()
    print("tests passed!")


if __name__ == "__main__":
    main()
