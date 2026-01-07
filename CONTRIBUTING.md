# Contributing to ABB Agentic Customer Support

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Issues](#reporting-issues)

## 🤝 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other contributors

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ABB_agentic_customer_support.git
   cd ABB_agentic_customer_support
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/Pezhman-Mazaheri/ABB_agentic_customer_support.git
   ```

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Firebase CLI)
- Firebase CLI: `npm install -g firebase-tools`

### Local Environment

```bash
# Create and activate virtual environment
cd functions
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up local environment
cp ../.env.example ../.env
# Edit .env with your API keys
```

### Running Locally

```bash
# Start Firebase emulators
firebase emulators:start

# Access at http://localhost:5000
```

## ✏️ Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-product-category`
- `fix/chat-response-error`
- `docs/update-api-documentation`
- `refactor/optimize-pdf-processing`

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(chat): add support for multi-document context
fix(ingest): handle ABB Library timeout errors
docs(readme): update deployment instructions
```

## 🔄 Pull Request Process

1. **Update your fork** with the latest upstream changes:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** and commit them

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** on GitHub

6. **Fill out the PR template** with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)

## 📝 Coding Standards

### Python (Cloud Functions)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function parameters and returns
- Document functions with docstrings
- Maximum line length: 100 characters

```python
def process_document(url: str, timeout: int = 60) -> dict:
    """
    Process a document from the given URL.
    
    Args:
        url: The document URL to process
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary containing processed document data
    """
    pass
```

### JavaScript/HTML (Frontend)

- Use 4 spaces for indentation
- Use descriptive variable names
- Add comments for complex logic
- Keep functions small and focused

### CSS (Tailwind)

- Use Tailwind utility classes when possible
- Group related classes logically
- Use custom CSS only when necessary

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Step-by-step instructions
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Browser, OS, versions
6. **Screenshots**: If applicable

Use the issue template when available.

## 📞 Questions?

If you have questions, feel free to:
- Open a GitHub Discussion
- Create an issue with the `question` label
- Contact the maintainer

---

Thank you for contributing! 🎉

