# CONTRIBUTING

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -e ".[dev]"`

## Running Tests

```bash
pytest tests/
```

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use MyPy for type checking

## Commit Guidelines

- Write clear commit messages
- Reference issues when applicable
- Ensure tests pass before committing
