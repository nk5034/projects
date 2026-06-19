# Quick Start Guide for Document Verification Agent

## Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

## Usage Examples

### Verify a Single Document from URL

```bash
python -m src.cli --url https://confluence.example.com/doc --template templates/example_template.md
```

### Verify a Confluence Page

```bash
python -m src.cli --page-id 123456 --template templates/example_template.md
```

### Batch Verify from File

```bash
# Create a file with URLs (one per line)
cat > urls.txt << EOF
https://confluence.example.com/doc1
https://confluence.example.com/doc2
https://confluence.example.com/doc3
EOF

# Run batch verification
python -m src.cli --file urls.txt --template templates/example_template.md
```

### Enable Debug Logging

```bash
python -m src.cli --url <url> --template templates/example_template.md --debug
```

## Python API Usage

```python
from doc_verification_agent import DocumentVerificationAgent

# Create agent
agent = DocumentVerificationAgent()

# Verify a document
result = agent.verify_document(
    url="https://confluence.example.com/doc",
    template_path="templates/example_template.md"
)

# Access results
print(f"Score: {result.score}/10")
print(f"Feedback: {result.llm_feedback}")
print(f"Template Match: {result.template_match}")

# Batch verification
results = agent.batch_verify(
    urls=["url1", "url2", "url3"],
    template_path="templates/example_template.md"
)

for result in results:
    print(f"{result.url}: {result.score}/10")
```

## Project Structure

```
doc_verification_agent/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── agent.py                 # Main verification agent
│   ├── cli.py                   # CLI interface
│   ├── config.py                # Configuration management
│   ├── document_fetcher.py      # Document fetching logic
│   ├── document_parser.py       # Document parsing
│   ├── llm_scorer.py            # LLM-based scoring
│   └── template_matcher.py      # Template comparison
├── tests/
│   ├── __init__.py
│   └── test_agent.py            # Agent tests
├── templates/
│   └── example_template.md      # Example template
├── requirements.txt             # Project dependencies
├── setup.py                     # Package setup
├── .env.example                 # Example env config
├── .gitignore                   # Git ignore rules
├── README.md                    # Full documentation
└── QUICKSTART.md               # This file
```

## Key Components

### DocumentFetcher
- Fetches documents from URLs
- Supports Confluence API
- Includes retry logic

### DocumentParser
- Parses Markdown with front matter
- Extracts HTML content
- Handles Confluence content

### TemplateMatcher
- Compares document structure against template
- Checks for required sections and metadata
- Calculates completeness scores

### LLMScorer
- Uses OpenAI or Anthropic APIs
- Provides intelligent scoring (1-10)
- Generates detailed feedback

### DocumentVerificationAgent
- Orchestrates the entire verification process
- Supports single and batch operations
- Returns comprehensive results

## Configuration

### Environment Variables

Key variables in `.env`:

- `LLM_PROVIDER`: Set to `openai` or `anthropic`
- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4)
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `CONFLUENCE_BASE_URL`: Your Confluence instance URL
- `CONFLUENCE_API_TOKEN`: Your Confluence API token

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_agent.py -v
```

## Troubleshooting

### API Key Issues
- Ensure `.env` file is properly configured
- Verify API keys are valid and have appropriate permissions

### Document Fetching Errors
- Check URL is accessible
- For Confluence, verify page ID and API token
- Check network/firewall settings

### LLM Scoring Errors
- Verify LLM API is working
- Check API rate limits
- Ensure LLM_PROVIDER is correctly set

## Next Steps

1. Create custom templates for your documents
2. Set up batch processing for multiple documents
3. Integrate with your CI/CD pipeline
4. Configure monitoring and alerts for document quality
