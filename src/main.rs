use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader, Write};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: md2html <markdown file> <html file>");
        std::process::exit(1);
    }

    let markdown_file = &args[1];
    let html_file = &args[2];

    let file = File::open(markdown_file).expect("Unable to open file");
    let reader = BufReader::new(file);

    let mut html = String::new();
    let mut in_code_block = false;
    let mut in_list = false;

    let mut in_blockquote = false;
    let mut blockquote_buffer = String::new();

    for line in reader.lines() {
        let line = line.unwrap();
        let line = line.to_string();

        let line = if !in_code_block {
            line.trim()
        } else {
            &line
        };

        if line.is_empty() {
            if in_list {
                html.push_str("</ul>\n");
                in_list = false;
            }
            continue;
        }

        if line.starts_with("```") {
            in_code_block = !in_code_block;
            if in_code_block {
                html.push_str("<pre><code>");
            } else {
                html.push_str("</code></pre>");
            }
            continue;
        }

        if in_code_block {
            html.push_str(&line);
            html.push_str("\n");
            continue;
        }

        if line.starts_with("#") {
            let mut count = 0;
            for c in line.chars() {
                if c == '#' {
                    count += 1;
                } else {
                    break;
                }
            }

            if count <= 6 {
                let tag = format!("h{}", count);
                let heading_content = parse_inline_formatting(&line[count..].trim());
                html.push_str(&format!("<{}>{}</{}>\n", tag, heading_content, tag));
            } else {
                html.push_str(&format!("<p>{}</p>\n", line.trim()));
            }
            continue;
        }


        if line.starts_with("* ") || line.starts_with("- ") {
            if !in_list {
                html.push_str("<ul>\n");
                in_list = true;
            }
            html.push_str(&format!("<li>{}</li>\n", &line[2..].trim()));
            continue;
        } else if in_list {
            html.push_str("</ul>\n");
            in_list = false;
        }

        if line.starts_with("> ") {
            if !in_blockquote {
                in_blockquote = true;
                blockquote_buffer.clear();
            }
            blockquote_buffer.push_str(&line[2..]);
            blockquote_buffer.push('\n');
            continue;
        } else if in_blockquote {
            html.push_str("<blockquote>");
            html.push_str(&parse_inline_formatting(blockquote_buffer.trim()));
            html.push_str("</blockquote>\n");
            in_blockquote = false;
        }

        let parsed_line = parse_inline_formatting(&line);

        html.push_str(&format!("<p>{}</p>\n", parsed_line));
    }

    if in_list {
        html.push_str("</ul>\n");
    }

    if in_blockquote {
        html.push_str("<blockquote>");
        html.push_str(&parse_inline_formatting(blockquote_buffer.trim()));
        html.push_str("</blockquote>\n");
    }

    let mut file = File::create(html_file).expect("Unable to create file");
    file.write_all(html.as_bytes())
        .expect("Unable to write data");
}

fn parse_inline_formatting(line: &str) -> String {
    let mut result = String::new();
    let mut chars = line.chars().peekable();
    let mut in_inline_code = false;

    while let Some(c) = chars.next() {
        if c == '*' {
            if let Some('*') = chars.peek() {
                chars.next();
                result.push_str("<strong>");
                while let Some(inner_c) = chars.next() {
                    if inner_c == '*' && chars.peek() == Some(&'*') {
                        chars.next();
                        result.push_str("</strong>");
                        break;
                    } else {
                        result.push(inner_c);
                    }
                }
            } else {
                result.push_str("<em>");
                while let Some(inner_c) = chars.next() {
                    if inner_c == '*' {
                        result.push_str("</em>");
                        break;
                    } else {
                        result.push(inner_c);
                    }
                }
            }
        } else if c == '[' {
            let mut link_text = String::new();
            while let Some(inner_c) = chars.next() {
                if inner_c == ']' {
                    if let Some('(') = chars.next() {
                        let mut link_url = String::new();
                        while let Some(url_c) = chars.next() {
                            if url_c == ')' {
                                result.push_str(&format!(
                                    "<a href=\"{}\">{}</a>",
                                    link_url, link_text
                                ));
                                break;
                            } else {
                                link_url.push(url_c);
                            }
                        }
                    }
                    break;
                } else {
                    link_text.push(inner_c);
                }
            }
        } else if c == '`' {
            if in_inline_code {
                result.push_str("</code>");
                in_inline_code = false;
            } else {
                result.push_str("<code>");
                in_inline_code = true;
            }
        } else {
            result.push(c);
        }
    }

    if in_inline_code {
        result.push_str("</code>");
    }
    result
}
