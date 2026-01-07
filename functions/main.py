"""
ABB Product Support Agent - Firebase Cloud Functions

This module contains three main cloud functions:
1. search_products - Searches ABB library for products based on category path
2. ingest_manual - Downloads and ingests PDF manual into Gemini
3. chat_agent - Handles chat interactions with the ingested manual context

Updated: 2026-01-06 - Using gemini-2.0-flash model
"""

import os
import re
import json
import tempfile
import time
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, quote_plus

import requests
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from firebase_functions import https_fn, options
from firebase_admin import initialize_app

# Initialize Firebase Admin
initialize_app()

# Configure CORS
cors_options = options.CorsOptions(
    cors_origins=["*"],
    cors_methods=["GET", "POST", "OPTIONS"]
)

# Define the secret
GEMINI_API_KEY_SECRET = options.SecretParam("GEMINI_API_KEY")

def get_genai_client():
    """Get Gemini API client with the secret key."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        return genai.Client(api_key=api_key)
    return None

# ABB Library base URL
ABB_LIBRARY_URL = "https://library.abb.com"


def clean_category_path(full_path: str) -> str:
    """
    Clean and transform category path into a search query.
    
    Removes generic root nodes like "ABB Products" or "All Categories"
    and formats the remaining path into space-separated search terms.
    
    Example: "ABB Products > HPR > Rectifier > MCR" -> "HPR Rectifier MCR"
    """
    # Split the path
    parts = full_path.split(" > ")
    
    # Remove generic root nodes
    generic_roots = {"ABB Products", "All Categories", "Products"}
    filtered_parts = [p for p in parts if p not in generic_roots]
    
    # Join with spaces for search query
    return " ".join(filtered_parts)


@https_fn.on_request(cors=cors_options)
def search_products(req: https_fn.Request) -> https_fn.Response:
    """
    Search for products in ABB library based on category path.
    Returns sample products with real ABB Library links.

    Input: JSON with "full_path" string
    Output: JSON list of {"title": "...", "download_url": "..."}
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)

    try:
        data = req.get_json()
        full_path = data.get("full_path", "")

        if not full_path:
            return https_fn.Response(
                json.dumps({"error": "Missing full_path parameter"}),
                status=400,
                content_type="application/json"
            )

        # Transform path to search query
        search_query = clean_category_path(full_path)
        query_lower = search_query.lower()

        # Product database with real ABB Library links
        # ABB Library uses JavaScript rendering, so we provide curated products
        product_database = {
            'hpr': [
                {'title': 'High Power Rectifiers for primary aluminum smelting', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3BHS352574&LanguageCode=en&Action=Launch'},
                {'title': 'High power rectifiers - Product portfolio overview', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK107492A3182&LanguageCode=en&Action=Launch'},
                {'title': 'High Power Rectifiers for Hydrogen Production', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK107992A8938&LanguageCode=en&Action=Launch'},
                {'title': 'High Power Rectifiers for the Chlor-Alkali industry', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3BHS352575&LanguageCode=en&Action=Launch'},
                {'title': 'Service for high power rectifiers', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3BHS505186&LanguageCode=en&Action=Launch'},
            ],
            'rectifier': [
                {'title': 'MCR1000 Medium Current Rectifier', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3BHS546772E01&LanguageCode=en&Action=Launch'},
                {'title': 'Compact Rectifier – Water Cooled', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK108467A6325&LanguageCode=en&Action=Launch'},
                {'title': 'Compact Rectifier CRW Series', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK107046A7093&LanguageCode=en&Action=Launch'},
                {'title': 'Compact Rectifier CRA Series', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK107046A7092&LanguageCode=en&Action=Launch'},
            ],
            'mcr': [
                {'title': 'MCR1000 Medium Current Rectifier', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3BHS546772E01&LanguageCode=en&Action=Launch'},
            ],
            'drive': [
                {'title': 'ACS880 primary control program firmware manual', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3AUA0000085967&LanguageCode=en&Action=Launch'},
                {'title': 'ACS580 User Manual', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3AUA0000064448&LanguageCode=en&Action=Launch'},
                {'title': 'ACS380 Machinery Drive Manual', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3AUA0000117344&LanguageCode=en&Action=Launch'},
            ],
            'robot': [
                {'title': 'IRB 6700 Product Manual', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3HAC052982-001&LanguageCode=en&Action=Launch'},
                {'title': 'IRC5 Controller Product Manual', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=3HAC050945-001&LanguageCode=en&Action=Launch'},
            ],
            'motor': [
                {'title': 'ABB Motors and Generators Catalog', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK105713A8893&LanguageCode=en&Action=Launch'},
                {'title': 'Low voltage motors IEC Technical Catalog', 'download_url': 'https://search.abb.com/library/Download.aspx?DocumentID=9AKK107045A4890&LanguageCode=en&Action=Launch'},
            ],
        }

        # Find matching products
        products = []
        seen_titles = set()

        for keyword, prods in product_database.items():
            if keyword in query_lower:
                for prod in prods:
                    if prod['title'] not in seen_titles:
                        seen_titles.add(prod['title'])
                        products.append(prod)

        # Build ABB Library search URL for reference
        search_url = f"{ABB_LIBRARY_URL}/r?cid=pscat&lang=en&q={search_query.replace(' ', '%20')}"

        return https_fn.Response(
            json.dumps({
                "products": products[:10],  # Limit to 10
                "query": search_query,
                "search_url": search_url
            }),
            content_type="application/json"
        )
        
    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )


@https_fn.on_request(cors=cors_options, timeout_sec=300, memory=options.MemoryOption.GB_1, secrets=[GEMINI_API_KEY_SECRET])
def ingest_manual(req: https_fn.Request) -> https_fn.Response:
    """
    Download and ingest a PDF manual into Gemini.

    Input: JSON with "download_url" string
    Output: JSON with "file_uri" for chat context
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)

    # Get Gemini client
    client = get_genai_client()
    if not client:
        return https_fn.Response(
            json.dumps({"error": "Gemini API key not configured"}),
            status=500,
            content_type="application/json"
        )

    try:
        data = req.get_json()
        download_url = data.get("download_url", "")

        if not download_url:
            return https_fn.Response(
                json.dumps({"error": "Missing download_url parameter"}),
                status=400,
                content_type="application/json"
            )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # First, fetch the download page to extract the actual PDF URL
        page_response = requests.get(download_url, headers=headers, timeout=60)
        page_response.raise_for_status()

        # Check if the response is HTML (ABB library page) or direct PDF
        content_type = page_response.headers.get('Content-Type', '')

        if 'text/html' in content_type:
            # Parse the HTML to find the actual PDF URL in the iframe
            soup = BeautifulSoup(page_response.text, 'lxml')
            iframe = soup.find('iframe', id='mainFrame')

            if iframe and iframe.get('src'):
                actual_pdf_url = iframe['src']
                # Download the actual PDF
                pdf_response = requests.get(actual_pdf_url, headers=headers, timeout=60)
                pdf_response.raise_for_status()
                pdf_content = pdf_response.content
            else:
                return https_fn.Response(
                    json.dumps({"error": "Could not find PDF URL in ABB library page"}),
                    status=500,
                    content_type="application/json"
                )
        else:
            # Direct PDF download
            pdf_content = page_response.content

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(pdf_content)
            tmp_path = tmp_file.name

        try:
            # Upload to Gemini using new SDK
            uploaded_file = client.files.upload(file=tmp_path)

            # Poll until file is active
            max_wait = 120  # seconds
            wait_interval = 5
            elapsed = 0

            while uploaded_file.state.name == "PROCESSING" and elapsed < max_wait:
                time.sleep(wait_interval)
                elapsed += wait_interval
                uploaded_file = client.files.get(name=uploaded_file.name)

            if uploaded_file.state.name != "ACTIVE":
                return https_fn.Response(
                    json.dumps({"error": f"File processing failed: {uploaded_file.state.name}"}),
                    status=500,
                    content_type="application/json"
                )

            return https_fn.Response(
                json.dumps({
                    "file_uri": uploaded_file.uri,
                    "file_name": uploaded_file.name,
                    "status": "success"
                }),
                content_type="application/json"
            )

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )


@https_fn.on_request(cors=cors_options, timeout_sec=60, secrets=[GEMINI_API_KEY_SECRET])
def chat_agent(req: https_fn.Request) -> https_fn.Response:
    """
    Chat with the ingested manual using Gemini.

    Input: JSON with "user_message" and "file_uri"
    Output: JSON with "response" text
    """
    if req.method == "OPTIONS":
        return https_fn.Response("", status=204)

    # Get Gemini client
    client = get_genai_client()
    if not client:
        return https_fn.Response(
            json.dumps({"error": "Gemini API key not configured"}),
            status=500,
            content_type="application/json"
        )

    try:
        data = req.get_json()
        user_message = data.get("user_message", "")
        file_uri = data.get("file_uri", "")
        file_name = data.get("file_name", "")

        if not user_message:
            return https_fn.Response(
                json.dumps({"error": "Missing user_message parameter"}),
                status=400,
                content_type="application/json"
            )

        # System prompt for ABB Technical Support
        system_prompt = """You are a specialized ABB Technical Support AI.
You have access to the specific product manual uploaded by the user.
Answer questions strictly based on the provided file content.
If the answer is not in the file, politely state that the information is missing from the manual.
Be concise, accurate, and helpful. Format technical information clearly."""

        # Build content with file context if available
        contents = []

        if file_name and file_uri:
            # Create a Part from the file URI
            try:
                file_part = types.Part.from_uri(file_uri=file_uri, mime_type="application/pdf")
                contents.append(file_part)
            except Exception:
                pass  # Continue without file if not found

        contents.append(user_message)

        # Generate response using new SDK
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            )
        )

        return https_fn.Response(
            json.dumps({
                "response": response.text,
                "status": "success"
            }),
            content_type="application/json"
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=500,
            content_type="application/json"
        )

