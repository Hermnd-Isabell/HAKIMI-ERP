import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re

def extract_docx_text(docx_path: str):
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read('word/document.xml')
    root = ET.fromstring(xml)

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = []
    for p in root.findall('.//w:p', ns):
        texts = []
        for t in p.findall('.//w:t', ns):
            texts.append(t.text or '')
        # Also include tab and break hints
        paragraph_text = ''.join(texts).strip()
        if paragraph_text:
            paragraphs.append(paragraph_text)
    return '\n'.join(paragraphs)

def split_by_page_breaks(text: str):
    # Word often inserts form feed or manual page breaks represented in XML as <w:br w:type="page"/>
    # Since we only extracted <w:t>, page breaks don't appear as characters.
    # This function uses approximate heading/blank-line heuristics to split pages.
    # We'll split on double newlines as paragraph boundaries and group them.
    paragraphs = [p for p in text.split('\n') if p.strip()]
    return paragraphs

if __name__ == '__main__':
    docx = Path(__file__).parent / 'refer_docs' / '系统设计报告.docx'
    text = extract_docx_text(str(docx))
    paragraphs = split_by_page_breaks(text)

    # Estimate ~40 lines per page
    lines_per_page = 45
    start_idx = 7 * lines_per_page
    end_idx = 18 * lines_per_page

    print(f'Total paragraphs: {len(paragraphs)}')
    print('--- Pages 8-18 (approximate) ---')
    for i, p in enumerate(paragraphs[start_idx:end_idx], start=start_idx+1):
        print(f'{i}: {p}')
