# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-06

### 🎉 Initial Release

First production-ready release of MCP Package Hero - a focused, reliable MCP server for checking latest package versions.

### ✨ Features

#### Core Functionality
- **Multi-Ecosystem Support**: Check package versions across three major ecosystems
  - Python (PyPI)
  - JavaScript/TypeScript (npm)
  - Dart/Flutter (pub.dev)

#### MCP Tools
- `get_latest_version`: Get the latest version of a single package
  - Parameters: `package_name` (string), `ecosystem` (string)
  - Returns: Package information with version, registry URL, status, and timestamp
  - Supports: Python, JavaScript, and Dart packages

- `get_latest_versions_batch`: Check multiple packages in a single request
  - Parameters: `packages` (list of package objects), `max_packages` (optional, default: 10)
  - Returns: Array of package version results with batch timestamp
  - Efficient async processing with graceful error handling

#### Technical Features
- **Async/Await**: Fast, non-blocking operations using httpx
- **Type Safety**: Full type hints with mypy compliance
- **Data Validation**: Pydantic V2 models with ConfigDict
- **Error Handling**: Comprehensive error handling with clear status indicators
  - Status types: `success`, `not_found`, `error`
  - Detailed error messages for debugging
- **Timezone-Aware**: All timestamps use UTC timezone
- **Clean Architecture**: Abstract base class for registry clients

### 🧪 Testing
- **Test Coverage**: 81% overall coverage
  - 100% coverage for models and initialization
  - 72-92% coverage for registry clients
  - 78% coverage for server
- **Test Types**:
  - Unit tests for each registry (PyPI, npm, pub.dev)
  - Integration tests for MCP tools
  - Live API validation tests
- **All Tests Passing**: 8/8 tests passing

### 📚 Documentation
- Comprehensive README with installation and usage instructions
- Configuration examples for Claude Desktop and Cline
- API documentation with examples
- PRD (Product Requirements Document)
- Implementation summary

### 🏗️ Development Setup
- **Python**: 3.10+ support (tested with 3.13)
- **Package Manager**: uv for fast, reproducible builds
- **Code Quality Tools**:
  - Ruff for linting and formatting
  - mypy for type checking with Pydantic plugin
  - pytest for testing with asyncio support
  - pytest-cov for coverage reporting

### 🐛 Fixed (Initial Development)
- Fixed FastMCP initialization (changed `description` to `instructions` parameter)
- Updated Pydantic models from deprecated V1 `Config` class to V2 `ConfigDict`
- Replaced deprecated `datetime.utcnow()` with timezone-aware `datetime.now(timezone.utc)`
- Added proper type annotations for mypy compliance
- Auto-fixed 47 linting issues with ruff

### 📦 Dependencies

#### Core
- `fastmcp>=2.12.4` - MCP server framework
- `httpx>=0.28.1` - Async HTTP client
- `pydantic>=2.11.10` - Data validation and models

#### Development
- `pytest>=8.4.2` - Testing framework
- `pytest-asyncio>=1.2.0` - Async test support
- `pytest-cov>=7.0.0` - Coverage reporting
- `ruff>=0.13.3` - Linting and formatting
- `mypy>=1.18.2` - Type checking

### 🎯 Design Decisions
- **Focus over Feature Creep**: Deliberately limited scope to version checking only
- **Registry Pattern**: Extensible design allows easy addition of new registries
- **Batch Limit**: Default max of 10 packages to prevent abuse
- **Real API Tests**: Integration tests use real APIs (not mocks) for validation
- **Timezone Awareness**: Modern Python datetime best practices

### 🔒 Security
- No credentials or secrets in code
- Input validation via Pydantic
- Timeout handling (10 seconds per request)
- No SQL injection risks (no database)

### 📝 Known Limitations
- No caching layer (planned for v1.1)
- No support for specific version queries (planned for v1.1)
- Batch limit of 10 packages (configurable, but enforced)
- Error handling paths have lower test coverage (by design - tested via success/not_found cases)

---

## [Unreleased]

### Planned for v1.1
- [ ] Cache layer for improved performance
- [ ] Support for specific version queries (not just latest)
- [ ] Package search/fuzzy matching
- [ ] Retry logic with exponential backoff
- [ ] Connection pooling for httpx clients

### Planned for v1.2
- [ ] Additional ecosystems: Rust (crates.io), Go (pkg.go.dev), Ruby (rubygems.org)
- [ ] Performance metrics and monitoring
- [ ] Rate limiting protection

### Planned for v2.0
- [ ] Dependency tree analysis
- [ ] Version compatibility checking
- [ ] Security vulnerability detection
- [ ] Private registry support

---

## Version History

### Release Notes

#### v1.0.0 (2025-10-06) - Initial Release
**Status**: ✅ Production Ready

This is the first stable release of MCP Package Hero. The codebase has been thoroughly tested, type-checked, and follows modern Python best practices.

**Highlights**:
- Three ecosystems supported (Python, JavaScript/TypeScript, Dart)
- 81% test coverage
- Full mypy type checking compliance
- Comprehensive error handling
- Production-ready architecture

**Breaking Changes**: N/A (initial release)

**Migration Guide**: N/A (initial release)

---

## Contributing

When contributing, please:
1. Update this CHANGELOG with your changes
2. Follow the format: Added, Changed, Deprecated, Removed, Fixed, Security
3. Link to issues and PRs where appropriate
4. Keep entries clear and concise
5. Date releases in YYYY-MM-DD format

---

## Links

- [Repository](https://github.com/moinsen-dev/mcp-package-hero)
- [Issues](https://github.com/moinsen-dev/mcp-package-hero/issues)
- [Discussions](https://github.com/moinsen-dev/mcp-package-hero/discussions)
- [PRD](./PRD.md)
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)
