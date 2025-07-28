# 📘 PDF Outline Extractor – Adobe Hackathon Round 1A

This project is built for **Adobe India's "Connecting the Dots" Hackathon – Round 1A**. It extracts a clean, hierarchical **outline** from a PDF file, identifying the **title** and structural headings (**H1, H2, H3**) based on visual layout.

---

## 🚀 Features

- Accepts PDF files (≤ 50 pages) from the `/input` directory
- Extracts:
  - Document **Title**
  - Section Headings: **H1**, **H2**, **H3**
- Outputs a JSON file in the required format to `/output` directory
- Compliant with constraints:
  - CPU-only
  - Model-free (no large model dependency)
  - Runs under 10 seconds
  - Offline-only (no internet access required)

---

## 🧠 Approach

1. **Text Extraction:**
   - Uses `PyMuPDF` to extract text spans (text, size, position) from PDF.

2. **Heading Detection:**
   - Groups spans by font size.
   - Chooses the **largest font on page 1** as the title.
   - Next 3 largest sizes are mapped to H1–H3 levels.

3. **Title Extraction:**
   - Picks the first span with the title font size from page 1.

4. **Outline Building:**
   - Constructs a structured outline by filtering spans that match heading levels.
   - Sorts by page number and Y position.

5. **Output Format:**
   - A JSON file like:
     ```json
     {
       "title": "Understanding AI",
       "outline": [
         {"level": "H1", "text": "Introduction", "page": 1},
         {"level": "H2", "text": "History of AI", "page": 2}
       ]
     }
     ```

---

## 🐳 Docker Usage

To build and run the container (example):
```bash
docker build --platform linux/amd64 -t pdf-outline:1a .
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none pdf-outline:1a
