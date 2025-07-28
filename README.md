# PDF Outline Extractor – Adobe Hackathon Round 1A

This project extracts a hierarchical outline (Title, H1, H2, H3) from PDF files into JSON format.  
Built for the Adobe India Hackathon – "Connecting the Dots" challenge (Round 1A).

---

## 🧩 **What it does**

- Accepts PDF files (up to 50 pages) from `input/` folder.
- Detects:
  - Document title
  - Headings: H1, H2, H3 with page number
- Outputs structured JSON into `output/` folder.

Example output:
```json
{
  "title": "Understanding AI",
  "outline": [
    {"level": "H1", "text": "Introduction", "page": 1},
    {"level": "H2", "text": "History of AI", "page": 2}
  ]
}
