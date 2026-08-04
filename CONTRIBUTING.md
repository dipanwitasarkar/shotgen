# Contributing to ShotGen

Thanks for your interest in contributing to ShotGen! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/shotgen.git`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Run `black` for formatting
- Run `ruff` for linting

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow ESLint rules
- Use Prettier for formatting

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update the README if needed
5. Create a PR with a clear description

## Adding a New AI Provider

1. Create a new file in `backend/app/providers/`
2. Implement the `AIProvider` interface
3. Register in `backend/app/providers/factory.py`
4. Add configuration in `backend/app/core/config.py`
5. Update documentation

Example:

```python
from app.providers.base import AIProvider, GenerationRequest, GenerationResult

class MyProvider(AIProvider):
    @property
    def name(self) -> str:
        return "myprovider"
    
    @property
    def supported_models(self) -> list[str]:
        return ["model-1", "model-2"]
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        # Implementation here
        pass
    
    async def health_check(self) -> bool:
        # Implementation here
        pass
```

## Reporting Issues

- Use the GitHub issue tracker
- Include steps to reproduce
- Include environment details
- Include error messages/logs

## Questions?

Open a discussion on GitHub or reach out on Discord.
