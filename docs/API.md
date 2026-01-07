# API Documentation

## Overview

The ABB Agentic Customer Support application exposes three Cloud Functions endpoints for product search, document ingestion, and AI-powered chat functionality.

**Base URL:** `https://us-central1-abb-agentic-support-2026.cloudfunctions.net`

## Authentication

Currently, the API is publicly accessible with CORS enabled for all origins. For production use, consider implementing Firebase Authentication.

---

## Endpoints

### 1. Search Products

Search for product documents based on category path.

**Endpoint:** `POST /search_products`

**Request:**
```json
{
  "full_path": "ABB Products > HPR > Rectifier"
}
```

**Response:**
```json
{
  "products": [
    {
      "title": "High Power Rectifiers for primary aluminum smelting",
      "download_url": "https://search.abb.com/library/Download.aspx?DocumentID=3BHS352574"
    }
  ],
  "query": "HPR Rectifier",
  "search_url": "https://library.abb.com/r?cid=pscat&lang=en&q=HPR%20Rectifier"
}
```

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Missing required parameter |
| 500 | Internal server error |

---

### 2. Ingest Manual

Download and upload a PDF manual to Google Gemini for processing.

**Endpoint:** `POST /ingest_manual`

**Request:**
```json
{
  "download_url": "https://search.abb.com/library/Download.aspx?DocumentID=3BHS352574"
}
```

**Response:**
```json
{
  "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123xyz",
  "file_name": "files/abc123xyz",
  "status": "success"
}
```

| Status Code | Description |
|-------------|-------------|
| 200 | Success - file uploaded and processed |
| 400 | Missing download_url parameter |
| 500 | Processing error or API key not configured |

**Notes:**
- 300-second timeout for large PDF files
- Uses 1GB memory allocation
- Requires `GEMINI_API_KEY` secret

---

### 3. Chat Agent

Send a question about an ingested document and receive an AI-powered response.

**Endpoint:** `POST /chat_agent`

**Request:**
```json
{
  "user_message": "What is the efficiency of the rectifier?",
  "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/abc123xyz",
  "file_name": "files/abc123xyz"
}
```

**Response:**
```json
{
  "response": "According to the manual, the rectiformer efficiency is optimized by...",
  "status": "success"
}
```

| Status Code | Description |
|-------------|-------------|
| 200 | Success - response generated |
| 400 | Missing user_message parameter |
| 500 | Processing error or API key not configured |

---

## Rate Limits

| Function | Timeout | Memory | Concurrent |
|----------|---------|--------|------------|
| search_products | 60s | 256MB | 1000 |
| ingest_manual | 300s | 1GB | 100 |
| chat_agent | 60s | 256MB | 1000 |

---

## Example Usage

### cURL

```bash
# Search for products
curl -X POST https://us-central1-abb-agentic-support-2026.cloudfunctions.net/search_products \
  -H "Content-Type: application/json" \
  -d '{"full_path": "ABB Products > HPR"}'

# Ingest a manual
curl -X POST https://us-central1-abb-agentic-support-2026.cloudfunctions.net/ingest_manual \
  -H "Content-Type: application/json" \
  -d '{"download_url": "https://search.abb.com/library/Download.aspx?DocumentID=3BHS352574"}'

# Chat with the document
curl -X POST https://us-central1-abb-agentic-support-2026.cloudfunctions.net/chat_agent \
  -H "Content-Type: application/json" \
  -d '{"user_message": "What is the efficiency?", "file_uri": "...", "file_name": "..."}'
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-07 | Initial release with search, ingest, and chat endpoints |

