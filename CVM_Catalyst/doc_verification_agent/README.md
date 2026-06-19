# Document Verification Agent

A Python-based document verification agent that fetches documents from URLs (like Confluence), parses them, compares them against template markdown files, and uses LLM APIs to score document readiness.

## Features

- **Document Fetching**: Retrieve documents from URLs (Confluence, web pages, etc.)
- **Parsing**: Extract and parse document content in multiple formats
- **Template Matching**: Compare documents against predefined markdown templates
- **LLM Scoring**: Use LLM APIs to intelligently score document readiness (0-10)
- **Async Support**: High-performance async operations for batch processing
- **Configurable**: Easy configuration via environment variables and config files

## Installation

### Prerequisites

- Python 3.9+
- pip or conda

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/doc-verification-agent.git
cd doc-verification-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

## Usage

### As a CLI Tool

```bash
# Score a single document
doc-verify --url https://confluence.example.com/doc --template templates/example_template.md

# Batch process multiple documents
doc-verify --file documents_list.txt --template templates/example_template.md
```

### As a Python Library

```python
from doc_verification_agent import DocumentVerificationAgent, DocumentFetcher, LLMScorer

# Initialize components
fetcher = DocumentFetcher()
scorer = LLMScorer(api_provider="openai")
agent = DocumentVerificationAgent(fetcher, scorer)

# Verify a document
result = agent.verify_document(
    url="https://confluence.example.com/doc",
    template_path="templates/example_template.md"
)

print(f"Readiness Score: {result.score}/10")
print(f"Feedback: {result.feedback}")
```

## Project Structure

```
doc_verification_agent/
├── src/
│   ├── __init__.py
│   ├── document_fetcher.py      # Document fetching logic
│   ├── document_parser.py       # Document parsing
│   ├── template_matcher.py      # Template comparison
│   ├── llm_scorer.py            # LLM-based scoring
│   ├── agent.py                 # Main agent logic
│   └── config.py                # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   ├── test_scorer.py
│   └── test_agent.py
├── templates/
│   └── example_template.md      # Example document template
├── requirements.txt             # Project dependencies
├── setup.py                     # Package setup
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# LLM API Configuration
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Document Fetching
REQUEST_TIMEOUT=30
MAX_RETRIES=3
USER_AGENT=DocumentVerificationAgent/1.0

# Scoring Configuration
MIN_SCORE=1
MAX_SCORE=10
DEFAULT_MODEL=gpt-4  # or claude-3-opus
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_agent.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

## Supported LLM Providers

- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Local LLMs (via LiteLLM integration)

## API Reference

See individual module documentation in `src/` for detailed API reference.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.
