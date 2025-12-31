import pikepdf
from pathlib import Path
from natsort import natsorted

pdf_dir = Path("pdfs")
output_pdf = "combined.pdf"

pdf_files = natsorted(pdf_dir.glob("*.pdf"), key=lambda p: p.name)

with pikepdf.Pdf.new() as out_pdf:
    for pdf in pdf_files:
        with pikepdf.open(pdf) as src:
            out_pdf.pages.extend(src.pages)
    out_pdf.save(output_pdf)

print(f"Merged {len(pdf_files)} PDFs into {output_pdf}")
