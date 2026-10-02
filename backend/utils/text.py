import html
import re


def sanitize_text(text: str) -> str:
    """Normalize AI/user text for document export while preserving readable punctuation."""
    replacements = {
        "“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-",
        "…": "...", "•": "-", "\u00a0": " ", "\u200b": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_preview(text: str) -> str:
    """Convert plain/markdown-ish AI output into safe preview HTML."""
    safe = html.escape(sanitize_text(text))
    lines = safe.split("\n")
    output = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                output.append("</ul>")
                in_list = False
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{stripped[2:]}</li>")
        elif re.match(r"^\d+[.)]\s", stripped):
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<p><strong>{stripped}</strong></p>")
        elif stripped.isupper() and len(stripped) < 100:
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<h3>{stripped}</h3>")
        else:
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f"<p>{stripped}</p>")
    if in_list:
        output.append("</ul>")
    return "".join(output)
