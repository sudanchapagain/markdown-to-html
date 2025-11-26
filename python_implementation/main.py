import sys


def parse_inline_formatting(line):
    result = []
    i = 0
    in_inline_code = False

    while i < len(line):
        c = line[i]

        if c == "*":
            if i + 1 < len(line) and line[i + 1] == "*":
                i += 2
                result.append("<strong>")

                while i < len(line) - 1:
                    if line[i] == "*" and line[i + 1] == "*":
                        result.append("</strong>")
                        i += 2
                        break
                    result.append(line[i])
                    i += 1
                continue
            else:
                i += 1
                result.append("<em>")

                while i < len(line):
                    if line[i] == "*":
                        result.append("</em>")
                        i += 1
                        break
                    result.append(line[i])
                    i += 1
                continue

        if c == "[":
            i += 1
            link_text = []

            while i < len(line) and line[i] != "]":
                link_text.append(line[i])
                i += 1

            if i < len(line) and line[i] == "]":
                i += 1

                if i < len(line) and line[i] == "(":
                    i += 1
                    link_url = []

                    while i < len(line) and line[i] != ")":
                        link_url.append(line[i])
                        i += 1

                    if i < len(line) and line[i] == ")":
                        i += 1
                        result.append(
                            f'<a href="{"".join(link_url)}">{"".join(link_text)}</a>'
                        )
                        continue

            result.append("[" + "".join(link_text))
            continue

        if c == "`":
            if in_inline_code:
                result.append("</code>")
                in_inline_code = False
            else:
                result.append("<code>")
                in_inline_code = True

            i += 1
            continue

        result.append(c)
        i += 1

    if in_inline_code:
        result.append("</code>")

    return "".join(result)


def convert(markdown_file, html_file):
    with open(markdown_file, "r") as f:
        lines = f.readlines()

    html = []
    in_code_block = False
    in_list = False
    in_blockquote = False
    blockquote_buffer = []

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line if in_code_block else line.strip()

        if stripped == "":
            if in_list:
                html.append("</ul>\n")
                in_list = False
            continue

        if stripped.startswith("```"):
            in_code_block = not in_code_block

            if in_code_block:
                html.append("<pre><code>")
            else:
                html.append("</code></pre>")
            continue

        if in_code_block:
            html.append(stripped + "\n")
            continue

        if stripped.startswith("#"):
            count = 0

            for c in stripped:
                if c == "#":
                    count += 1
                else:
                    break

            if count <= 6:
                tag = f"h{count}"
                content = parse_inline_formatting(stripped[count:].strip())
                html.append(f"<{tag}>{content}</{tag}>\n")
            else:
                html.append(f"<p>{stripped}</p>\n")
            continue

        if stripped.startswith("* ") or stripped.startswith("- "):
            item = stripped[2:].strip()

            if not in_list:
                html.append("<ul>\n")
                in_list = True

            html.append(f"<li>{item}</li>\n")
            continue

        if stripped.startswith("> "):
            if not in_blockquote:
                in_blockquote = True
                blockquote_buffer = []

            blockquote_buffer.append(stripped[2:])
            continue
        else:
            if in_blockquote:
                html.append("<blockquote>")
                html.append(
                    parse_inline_formatting("\n".join(blockquote_buffer).strip())
                )
                html.append("</blockquote>\n")
                in_blockquote = False

        parsed = parse_inline_formatting(stripped)
        html.append(f"<p>{parsed}</p>\n")

    if in_list:
        html.append("</ul>\n")

    if in_blockquote:
        html.append("<blockquote>")
        html.append(parse_inline_formatting("\n".join(blockquote_buffer).strip()))
        html.append("</blockquote>\n")

    out = "".join(html)

    with open(html_file, "w") as f:
        f.write(out)

    return out


def main():
    if len(sys.argv) != 3:
        print("usage: python main.py input.md output.html")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    convert(markdown_file, html_file)


if __name__ == "__main__":
    main()
