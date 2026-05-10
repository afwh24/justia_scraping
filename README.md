
---

# Justia Extraction — README.md

```markdown
# Justia Court Opinion Extraction Pipeline

A scalable legal document extraction pipeline for downloading, processing, and structuring United States federal district court opinions from Justia.

---

## Overview

This project automates the extraction of legal opinions from Justia and converts them into structured machine-readable datasets for legal AI research and downstream NLP applications.

The pipeline is designed to handle large-scale scraping with robust checkpointing, retry logic, and structured JSONL outputs.

---

## Features

### Court Opinion Scraping
- Federal district court opinion extraction
- Automated PDF downloading
- Metadata collection
- URL hashing and file organization

### PDF Processing
- PDF text extraction
- Structured content cleaning
- Error handling for malformed documents

### Data Storage
- JSONL dataset generation
- Metadata-rich legal records
- Hashed filenames for reproducibility

### Fault Tolerance
- Resume support
- Existing file checkpointing
- Exponential backoff retry strategy
- Error logging

---

## Dataset Schema

Example output format:

```json
{
  "case_name": "United States v. Example",
  "court": "District Court",
  "date": "2024-01-01",
  "pdf_url": "https://...",
  "document": "Full extracted opinion text..."
}
