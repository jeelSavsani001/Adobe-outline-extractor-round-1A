#!/usr/bin/env python3
# outline_extractor.py

import os
import json
import fitz   # PyMuPDF
from collections import Counter

INPUT_DIR = "input"
OUTPUT_DIR = "/adobe_1a/output"
MIN_TEXT_LEN = 3  # ignore noise

def extract_spans(doc):
    """Extract all text spans with their metadata."""
    spans = []
    for pno, page in enumerate(doc, start=1):
        j = page.get_text("dict")
        for block in j["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if len(text) < MIN_TEXT_LEN: continue
                    size = round(span["size"], 1)
                    flags = span.get("flags", 0)
                    bold = bool(flags & 2)
                    italic = bool(flags & 1)
                    y0 = span["bbox"][1]
                    spans.append({
                        "text": text,
                        "size": size,
                        "bold": bold,
                        "italic": italic,
                        "page": pno,
                        "y": y0
                    })
    return spans

def pick_levels(spans):
    """Determine title size and H1–H3 sizes via font‐size clustering."""
    # Collect all sizes
    size_counts = Counter(s["size"] for s in spans)
    # Title = single largest size on page 1
    title_candidates = [s for s in spans if s["page"] == 1]
    title_size = max((s["size"] for s in title_candidates), default=None)
    # Remaining sizes sorted descending
    other_sizes = sorted({sz for sz in size_counts if sz != title_size}, reverse=True)
    # Map sizes to levels
    level_map = {}
    if title_size:
        level_map[title_size] = "TITLE"
    for lvl, sz in enumerate(other_sizes[:3], start=1):
        level_map[sz] = f"H{lvl}"
    return level_map

def build_outline(spans, level_map):
    """Filter only TITLE/H1/H2/H3 spans and sort them."""
    items = []
    for s in spans:
        lvl = level_map.get(s["size"])
        if lvl:
            items.append((s["page"], s["y"], lvl, s["text"]))
    # Sort by page, then vertical position
    items.sort(key=lambda x: (x[0], x[1]))
    outline = []
    for page, y, lvl, text in items:
        if lvl == "TITLE":
            continue  # will handle title separately
        outline.append({"level": lvl, "text": text, "page": page})
    return outline

def extract_title(spans, title_size):
    """Grab the first span on page 1 with the title size."""
    for s in spans:
        if s["page"] == 1 and s["size"] == title_size:
            return s["text"]
    return ""

def process_pdf(path_in, path_out):
    doc = fitz.open(path_in)
    spans = extract_spans(doc)
    if not spans:
        print(f"No text found in {path_in}")
        return
    level_map = pick_levels(spans)
    title = extract_title(spans, list(level_map.keys())[0])
    outline = build_outline(spans, level_map)
    out = {"title": title, "outline": outline}
    with open(path_out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fn in os.listdir(INPUT_DIR):
        if not fn.lower().endswith(".pdf"): continue
        in_pdf = os.path.join(INPUT_DIR, fn)
        out_json = os.path.join(OUTPUT_DIR, fn[:-4] + ".json")
        process_pdf(in_pdf, out_json)
        print(f"Wrote outline to {out_json}")

if __name__ == "__main__":
    main()
