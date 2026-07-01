# Contributing to ThreatScope

Thank you for your interest in improving ThreatScope. This document explains the workflow.

## Setup
1. Fork the repo
2. Clone your fork
3. Create a virtual environment
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Start services with Docker Compose

## Branch Naming
- Feature: `feature/<short-description>`
- Bug fix: `bugfix/<issue-number>-<description>`
- Hotfix: `hotfix/<description>`
- Documentation: `docs/<description>`

Examples:
- `feature/threat-correlation-engine`
- `bugfix/425-misp-import-failure`
- `docs/api-reference-update`

## Commit Conventions

Use [Conventional Commits](https://conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
- `feat(backend): add IOC enrichment endpoint`
- `fix(ioc): deduplicate VirusTotal results`
- `docs(architecture): add threat workflow diagram`

## Pull Request Process
1. Update `CHANGELOG.md`
2. Ensure CI passes
3. Request review from maintainers
4. Address review comments
5. Squash and merge when approved

## Coding Standards
- Python: Black, flake8, type hints
- TypeScript/React: ESLint, Prettier
- Tests: pytest for backend, Jest for frontend
- Commit often and keep PRs focused

## Security Guidelines
- Never commit secrets or API keys
- Report security issues via SECURITY.md process
- Follow secure coding practices
- Update dependencies regularly

Thank you for contributing!
