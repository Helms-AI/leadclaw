# Contributing to LeadClaw

Thank you for your interest in contributing to LeadClaw!

## Development Setup

1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Install Node dependencies: `npm install`
4. Copy `.env.example` to `.env` and configure
5. Run the server: `python -m server.app`

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `chore/*` | Maintenance tasks |

## Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]
[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(email): add SendGrid integration

- Implement send_email() function
- Add template rendering
- Include tracking pixel
```

## Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes
3. Write/update tests
4. Update documentation
5. Create PR with description
6. Wait for review
7. Address feedback
8. Merge when approved

## Code Style

- Python: Follow PEP 8
- JavaScript: Follow Airbnb style guide
- Use meaningful variable names
- Comment complex logic
- Keep functions small and focused

## Questions?

Open a Discussion or reach out in Issues.
