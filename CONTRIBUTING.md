# Contributing to GodsEye

Thank you for your interest in contributing to GodsEye! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Go 1.21+ (for Go development)
- Python 3.11+ (for Python development)
- Git

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/GodsEye.git
   cd GodsEye
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   make up
   # or
   ./start.sh
   ```

## 🏗️ Project Structure

```
GodsEye/
├── crawler-service/     # Go-based crawler
│   ├── internal/        # Internal packages
│   │   ├── crawler/     # Crawling logic
│   │   ├── handlers/    # HTTP handlers
│   │   ├── models/      # Data models
│   │   └── database/    # Database connections
│   └── main.go
│
└── intel-service/       # Python-based intelligence
    └── app/
        ├── models/      # Pydantic schemas
        ├── services/    # Business logic
        ├── routers/     # API routes
        └── utils/       # Utilities
```

## 💻 Development Workflow

### Go Service Development

1. **Install dependencies**
   ```bash
   cd crawler-service
   go mod download
   ```

2. **Run locally**
   ```bash
   go run main.go
   ```

3. **Run tests**
   ```bash
   go test ./...
   ```

4. **Format code**
   ```bash
   go fmt ./...
   ```

5. **Lint code**
   ```bash
   golangci-lint run
   ```

### Python Service Development

1. **Create virtual environment**
   ```bash
   cd intel-service
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run locally**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Run tests**
   ```bash
   pytest
   ```

5. **Format code**
   ```bash
   black app/
   isort app/
   ```

6. **Lint code**
   ```bash
   flake8 app/
   mypy app/
   ```

## 📝 Code Style Guidelines

### Go Code Style
- Follow [Effective Go](https://golang.org/doc/effective_go.html)
- Use `gofmt` for formatting
- Add comments for exported functions and types
- Use meaningful variable names
- Keep functions small and focused

### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Use docstrings for functions and classes
- Maximum line length: 100 characters
- Use `black` for formatting

## 🧪 Testing Guidelines

### Writing Tests

**Go Tests**
```go
func TestCrawlerService(t *testing.T) {
    service := NewCrawlerService()
    // Test logic here
}
```

**Python Tests**
```python
def test_nlp_service():
    service = NLPService()
    service.load_models()
    # Test logic here
```

### Test Coverage
- Aim for at least 70% code coverage
- Write unit tests for all business logic
- Write integration tests for API endpoints
- Mock external dependencies

## 🔧 Making Changes

### Branch Naming
- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`
- Refactor: `refactor/description`

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add semantic search endpoint
fix: resolve Neo4j connection timeout
docs: update API documentation
refactor: simplify entity extraction logic
test: add tests for comparison endpoint
```

### Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Test Go service
   cd crawler-service && go test ./...
   
   # Test Python service
   cd intel-service && pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure all tests pass
   - Wait for code review

## 📋 Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests are added/updated
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] All tests pass
- [ ] No linting errors
- [ ] PR description is clear and complete

## 🐛 Reporting Bugs

### Before Submitting
- Check existing issues to avoid duplicates
- Verify the bug in the latest version
- Collect relevant information (logs, screenshots, etc.)

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., macOS 13.0]
- Docker version: [e.g., 24.0.0]
- Service version: [e.g., v1.0.0]

**Logs**
```
Relevant log output
```
```

## 💡 Feature Requests

We welcome feature requests! Please:
1. Check if the feature already exists or is planned
2. Provide a clear use case
3. Explain the expected behavior
4. Consider implementation complexity

## 🤝 Code Review Process

### For Reviewers
- Be respectful and constructive
- Focus on code quality and maintainability
- Check for test coverage
- Verify documentation updates
- Test the changes locally if needed

### For Contributors
- Respond to feedback promptly
- Be open to suggestions
- Ask questions if unclear
- Update the PR based on feedback

## 📚 Resources

- [Go Documentation](https://golang.org/doc/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [spaCy Documentation](https://spacy.io/usage)

## 🎯 Areas We Need Help

- [ ] Additional NLP models integration
- [ ] Better search query handling
- [ ] Performance optimization
- [ ] More comprehensive tests
- [ ] Documentation improvements
- [ ] UI/Dashboard development
- [ ] CLI tool development

## 📞 Getting Help

- Open a GitHub issue
- Join our community discussions
- Check existing documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to DefinitelyNotASpy! 🎉
