# ABB Agentic Customer Support

<div align="center">

![ABB Logo](docs/images/abb-logo.png)

**AI-Powered Technical Documentation Assistant for Industrial Products**

[![Firebase](https://img.shields.io/badge/Firebase-Deployed-orange?logo=firebase)](https://abb-agentic-support-2026.web.app)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Google AI](https://img.shields.io/badge/Google_AI-Gemini_2.0-4285F4?logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Live Demo](https://abb-agentic-support-2026.web.app) • [API Documentation](docs/API.md) • [Architecture](#architecture)

</div>

---

## 🌐 Live Deployment

> **🚀 This application is deployed and live at: [https://abb-agentic-support-2026.web.app/](https://abb-agentic-support-2026.web.app/)**

---

## 📚 Academic Project Notice

> **⚠️ Open Source Academic Project**
>
> This is an open source academic project developed for educational and demonstration purposes. It is **not affiliated with, endorsed by, or sponsored by ABB Ltd.** The project showcases the integration of modern AI technologies with enterprise product documentation systems.
>
> - **Purpose:** Educational demonstration of AI-powered customer support systems
> - **License:** MIT License - free to use, modify, and distribute
> - **Contributions:** Welcome from the open source community

---

## 🎯 Overview

ABB Agentic Customer Support is an intelligent web application that enables customers to interact with ABB product documentation using natural language. Users can browse product categories, select technical manuals, and ask questions about the products - receiving accurate, context-aware responses powered by Google's Gemini 2.0 AI.

### Key Features

- 🔍 **Product Catalog Browser** - Hierarchical navigation of ABB product categories
- 📄 **PDF Manual Integration** - Direct access to official ABB Library documents
- 🤖 **AI-Powered Q&A** - Ask questions about product manuals in natural language
- 🌙 **Dark Mode Support** - Comfortable viewing in any environment
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices
- ⚡ **Real-time Processing** - Fast PDF ingestion and instant responses

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Firebase Hosting)               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  HTML/Tailwind CSS │ Product Browser │ Chat Interface       │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Cloud Functions (Python 3.11)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │search_products│  │ingest_manual │  │    chat_agent        │  │
│  │ (Category→   │  │ (PDF → Gemini│  │ (Question → Answer)  │  │
│  │  Products)   │  │  Upload)     │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     External Services                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ ABB Library  │  │Google Gemini │  │ Firebase Admin       │  │
│  │ (PDF Source) │  │ 2.0 Flash    │  │ (Auth & Config)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript |
| **Backend** | Python 3.11, Firebase Cloud Functions |
| **AI/ML** | Google Gemini 2.0 Flash (google-genai SDK) |
| **Hosting** | Firebase Hosting |
| **PDF Processing** | BeautifulSoup4, lxml, Requests |
| **Data Source** | ABB Library API |

## 📋 Prerequisites

- Node.js 18+ (for Firebase CLI)
- Python 3.11+
- Firebase CLI (`npm install -g firebase-tools`)
- Google Cloud Project with Gemini API enabled
- Firebase project with Blaze (pay-as-you-go) plan

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Pezhman-Mazaheri/ABB_agentic_customer_support.git
cd ABB_agentic_customer_support
```

### 2. Set Up Firebase

```bash
# Login to Firebase
firebase login

# Initialize project (if needed)
firebase use --add
```

### 3. Configure Environment

```bash
# Set the Gemini API key as a Firebase secret
firebase functions:secrets:set GEMINI_API_KEY
# Enter your API key when prompted
```

### 4. Install Dependencies

```bash
cd functions
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### 5. Deploy

```bash
# Deploy everything
firebase deploy

# Or deploy only hosting
firebase deploy --only hosting:abb-agentic-support-2026

## 💬 Usage

### Browsing Products

1. Navigate to the application
2. Use the sidebar to browse product categories
3. Click on a category to expand subcategories
4. Select a product document to view

### Chatting with Documents

1. Click the **"Chat"** button next to any product document
2. Wait for the document to be processed (indicated by green status)
3. Type your question in the chat input
4. Receive AI-powered answers based on the document content

### Example Questions

- "What is the efficiency of this rectifier?"
- "What are the installation requirements?"
- "Explain the cooling system specifications"
- "What maintenance is required?"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google AI API key for Gemini | Yes |

### Firebase Secrets

```bash
# Set production secrets
firebase functions:secrets:set GEMINI_API_KEY

# View current secrets
firebase functions:secrets:access GEMINI_API_KEY
```

## 🧪 Testing

### Local Development

```bash
# Start Firebase emulators
firebase emulators:start

# Access local version
open http://localhost:5000
```

### API Testing

```bash
# Test search_products endpoint
curl -X POST https://us-central1-abb-agentic-support-2026.cloudfunctions.net/search_products \
  -H "Content-Type: application/json" \
  -d '{"full_path": "ABB Products > HPR"}'

# Test ingest_manual endpoint
curl -X POST https://us-central1-abb-agentic-support-2026.cloudfunctions.net/ingest_manual \
  -H "Content-Type: application/json" \
  -d '{"download_url": "https://search.abb.com/library/Download.aspx?DocumentID=3BHS352574"}'
```

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Gemini API key not configured" | Set the secret: `firebase functions:secrets:set GEMINI_API_KEY` |
| Functions not deploying | Ensure you have Blaze plan enabled |
| PDF not loading | Check if the ABB Library URL is accessible |
| Chat not responding | Verify Cloud Functions are deployed and running |

### Logs

```bash
# View function logs
firebase functions:log

# View specific function logs
firebase functions:log --only chat_agent
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ABB Ltd](https://new.abb.com) - Product documentation and technical data
- [Google AI](https://ai.google.dev) - Gemini 2.0 Flash model
- [Firebase](https://firebase.google.com) - Hosting and Cloud Functions
- [Tailwind CSS](https://tailwindcss.com) - UI styling framework

## 📞 Contact

**Pejman Mazaheri**
- GitHub: [@Pezhman-Mazaheri](https://github.com/Pezhman-Mazaheri)
- LinkedIn: [Pejman Mazaheri](https://www.linkedin.com/in/pejman-mazaheri/)

---

<div align="center">
Made with ❤️ for industrial innovation
</div>
