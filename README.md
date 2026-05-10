# Justia Court Opinion Extraction Pipeline

A scalable legal document extraction pipeline for downloading, processing, and structuring United States federal district court opinions from Justia into machine-readable datasets for legal AI and NLP applications.

---

## Overview

This project automates the collection and processing of legal court opinions from Justia. The pipeline is designed for large-scale extraction with robust error handling, checkpointing, and structured JSONL dataset generation.

The extracted legal documents can be used for:
- Legal NLP research
- LLM training
- Retrieval-Augmented Generation (RAG)
- Legal summarization
- Synthetic legal data generation

---

## Features

### Court Opinion Scraping
- Automated scraping of federal district court opinions
- Metadata extraction
- PDF download automation
- URL-based hashed file storage

### PDF Processing
- PDF text extraction
- Structured text cleaning
- Malformed document handling

### Dataset Generation
- JSONL dataset outputs
- Metadata-rich legal records
- Reproducible document organization

### Fault Tolerance
- Existing file checkpoint detection
- Exponential backoff retry strategy
- Error logging and recovery
- Resume support for interrupted runs

---

## Pipeline Architecture

1. Crawl Justia opinion pages
2. Extract case metadata
3. Download opinion PDFs
4. Generate hashed filenames
5. Extract and clean PDF text
6. Convert records into JSONL format
7. Save outputs and logs

---

## Dataset Schema

Example output:

```json
{
  "case_name": "United States v. Example",
  "court": "Federal District Court",
  "date": "2024-01-01",
  "pdf_url": "https://...",
  "document": "Full extracted legal opinion text..."
}
```

---

## Technologies Used

- Python
- BeautifulSoup
- Requests
- PDF processing libraries
- JSONL
- Regex

---

## Usage

```bash
python main.py
```

---

## Project Structure

```text
justia_extraction/
├── data/
├── logs/
├── outputs/
├── scripts/
├── main.py
└── README.md
```

---

## Example Applications

- Legal AI systems
- Court judgment analysis
- Legal document retrieval
- Case summarization
- Synthetic legal dataset generation

---

## Scalability

The pipeline supports:
- Hundreds of thousands of legal opinions
- Long-running scraping workflows
- Automated recovery from failures
- Large-scale dataset generation

---

## Future Improvements

- OCR support for scanned PDFs
- Multi-court extraction support
- Citation extraction
- Named entity recognition
- Legal knowledge graph generation
