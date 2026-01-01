import pdfplumber
import re

# ---------- Paths ----------
input_pdf = "cleaned.pdf"
output_md = "book.md"

# ---------- Helper functions ----------
def is_heading(line):
    """Treat fully uppercase lines as headings"""
    line = line.strip()
    return line.isupper() and len(line) > 3

def is_list_item(line):
    """Detect bullet points or numbered lists"""
    line = line.strip()
    return line.startswith(("-", "*")) or re.match(r"^\d+\.", line)

# ---------- Open PDF ----------
with pdfplumber.open(input_pdf) as pdf, open(output_md, "w", encoding="utf-8") as f:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        lines = text.split("\n")
        paragraph = []

        for line in lines:
            line = line.strip()
            if not line:
                # End of paragraph
                if paragraph:
                    f.write(" ".join(paragraph) + "\n\n")
                    paragraph = []
                continue

            if is_heading(line):
                if paragraph:
                    f.write(" ".join(paragraph) + "\n\n")
                    paragraph = []
                f.write(f"# {line}\n\n")
            elif is_list_item(line):
                if paragraph:
                    f.write(" ".join(paragraph) + "\n\n")
                    paragraph = []
                # Remove bullet/number from line for clean Markdown
                clean_line = re.sub(r"^(\-|\*|\d+\.)\s*", "", line)
                f.write(f"- {clean_line}\n")
            else:
                paragraph.append(line)

        # Write any remaining paragraph at the end of the page
        if paragraph:
            f.write(" ".join(paragraph) + "\n\n")

print(f"Markdown conversion complete: {output_md}")

