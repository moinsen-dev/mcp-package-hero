# Product Requirements Document: MCP Package Hero

## Project Overview

**Project Name:** MCP Package Hero  
**Version:** 1.0.0  
**Repository:** `/Users/udi/work/moinsen/opensource/mcp-package-hero`  
**Created:** October 6, 2025  
**Status:** Initial Development

### Executive Summary

MCP Package Hero is a focused, reliable Model Context Protocol (MCP) server that provides LLMs with instant access to the latest package versions across three major ecosystems: Python (PyPI), JavaScript/TypeScript (npm), and Dart (pub.dev). Unlike existing solutions that attempt to cover many registries with varying levels of support, Package Hero focuses on doing three things exceptionally well.

### Mission Statement

To provide developers with a simple, fast, and reliable MCP tool that answers one question perfectly: "What is the current latest version of this package?"

---

## Problem Statement

### Current State

Developers and LLMs frequently need to:
1. Check if they're using the latest version of a package
2. Verify package availability before recommending dependencies
3. Ensure code examples use current, non-deprecated versions

### Existing Solutions

- **mcp-package-version** (deprecated): Attempted to support many registries but is no longer maintained
- **Manual checking**: Requires switching contexts to package registry websites
- **Specialized MCP servers**: Dart has its own MCP server, but lacks integration with other ecosystems

### Gap

No single, maintained, focused tool exists that:
- Reliably covers the three most popular development ecosystems
- Maintains a simple, predictable API
- Is actively maintained and production-ready

---

## Goals and Objectives

### Primary Goals (v1.0)

1. **Reliability First**: Provide accurate version information with 99.9% uptime
2. **Simplicity**: Single-purpose tool with minimal cognitive overhead
3. **Speed**: Sub-second response times for version lookups
4. **Developer Experience**: Clean, intuitive API that LLMs can use effectively

### Non-Goals (v1.0)

- Full dependency tree resolution
- Version comparison or compatibility checking
- Package metadata beyond version numbers
- Support for additional package registries
- Private registry support

---

## Target Users

### Primary Users

1. **LLM Agents (Claude, ChatGPT, etc.)**
   - Using MCP-compatible clients
   - Generating code with up-to-date dependencies
   - Verifying package availability

2. **Developers Using AI Assistants**
   - Working with Python, JavaScript/TypeScript, or Dart
   - Want their AI tools to recommend current packages
   - Need quick version verification

### User Personas

**Persona 1: "Alex the Full-Stack Developer"**
- Works across Python backends and TypeScript frontends
- Uses Claude Desktop for coding assistance
- Frustrated by outdated package recommendations

**Persona 2: "Sam the Flutter Developer"**
- Builds mobile apps with Flutter/Dart
- Needs current pub.dev package versions
- Wants AI assistant to suggest compatible packages

**Persona 3: "Jordan the AI Agent Builder"**
- Develops autonomous coding agents
- Requires reliable package information for code generation
- Values simple, predictable APIs

---

## Core Features (v1.0)

### Feature 1: Get Latest Version

**Description**: Retrieve the latest stable version of a package

**Tool Name**: `get_latest_version`

**Parameters**:
- `package_name` (string, required): Name of the package
- `ecosystem` (string, required): One of ["python", "javascript", "dart"]

**Returns**:
```json
{
  "package_name": "requests",
  "ecosystem": "python",
  "latest_version": "2.31.0",
  "registry_url": "https://pypi.org/project/requests/",
  "checked_at": "2025-10-06T10:30:00Z"
}
```

**Success Criteria**:
- Returns correct latest stable version
- Response time < 1 second
- Handles non-existent packages gracefully
- Clear error messages

### Feature 2: Batch Version Check

**Description**: Check multiple packages in a single request

**Tool Name**: `get_latest_versions_batch`

**Parameters**:
- `packages` (array, required): List of {package_name, ecosystem} objects
- `max_packages` (integer, optional): Limit to prevent abuse (default: 10)

**Returns**:
```json
{
  "results": [
    {
      "package_name": "requests",
      "ecosystem": "python",
      "latest_version": "2.31.0",
      "status": "success"
    },
    {
      "package_name": "nonexistent-pkg",
      "ecosystem": "python",
      "latest_version": null,
      "status": "not_found"
    }
  ],
  "checked_at": "2025-10-06T10:30:00Z"
}
```

**Success Criteria**:
- Processes multiple packages efficiently
- Continues processing even if one package fails
- Clear status indicators for each package

---

## Technical Architecture

### Technology Stack

**Core Framework**: FastMCP 2.0
- Pythonic API design
- Built-in MCP protocol handling
- Excellent documentation and community

**Package Manager**: uv
- Fast dependency resolution
- Modern Python packaging
- Reproducible environments

**Language**: Python 3.10+
- Type hints throughout
- Async/await for performance
- Modern Python patterns

### Registry Integration

#### Python (PyPI)
- **API**: PyPI JSON API (https://pypi.org/pypi/{package}/json)
- **Endpoint**: `https://pypi.org/pypi/{package_name}/json`
- **Rate Limits**: No authentication required, respectful rate limiting
- **Data Format**: JSON with `info.version` field

#### JavaScript/TypeScript (npm)
- **API**: npm Registry API
- **Endpoint**: `https://registry.npmjs.org/{package_name}`
- **Rate Limits**: Generous for read operations
- **Data Format**: JSON with `dist-tags.latest` field

#### Dart (pub.dev)
- **API**: pub.dev API
- **Endpoint**: `https://pub.dev/api/packages/{package_name}`
- **Rate Limits**: Documented limits, respectful usage
- **Data Format**: JSON with `latest.version` field

### Project Structure

```
mcp-package-hero/
├── README.md
├── PRD.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .python-version
├── src/
│   └── mcp_package_hero/
│       ├── __init__.py
│       ├── server.py          # Main FastMCP server
│       ├── registries/
│       │   ├── __init__.py
│       │   ├── base.py        # Abstract base class
│       │   ├── pypi.py        # PyPI integration
│       │   ├── npm.py         # npm integration
│       │   └── pubdev.py      # pub.dev integration
│       └── models.py          # Pydantic models
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   └── test_registries/
│       ├── test_pypi.py
│       ├── test_npm.py
│       └── test_pubdev.py
└── examples/
    └── basic_usage.py
```

### Error Handling Strategy

1. **Package Not Found**: Return structured response with status="not_found"
2. **Registry Unavailable**: Retry logic with exponential backoff
3. **Rate Limiting**: Implement respectful delays, cache results
4. **Invalid Input**: Clear validation errors with suggestions

---

## API Design

### Tool 1: get_latest_version

```python
@mcp.tool()
async def get_latest_version(
    package_name: str,
    ecosystem: Literal["python", "javascript", "dart"]
) -> dict:
    """
    Get the latest stable version of a package.
    
    Args:
        package_name: The name of the package (e.g., "requests", "react", "http")
        ecosystem: The package ecosystem ("python", "javascript", or "dart")
    
    Returns:
        Dictionary with package information including latest version
    
    Examples:
        - get_latest_version("requests", "python")
        - get_latest_version("react", "javascript")
        - get_latest_version("http", "dart")
    """
```

### Tool 2: get_latest_versions_batch

```python
@mcp.tool()
async def get_latest_versions_batch(
    packages: list[dict[str, str]],
    max_packages: int = 10
) -> dict:
    """
    Get latest versions for multiple packages at once.
    
    Args:
        packages: List of dicts with 'package_name' and 'ecosystem' keys
        max_packages: Maximum number of packages to check (default: 10)
    
    Returns:
        Dictionary with results array containing version info for each package
    
    Examples:
        - get_latest_versions_batch([
            {"package_name": "requests", "ecosystem": "python"},
            {"package_name": "react", "ecosystem": "javascript"}
          ])
    """
```

---

## Implementation Phases

### Phase 1: Project Bootstrap (Week 1)
- [ ] Initialize project with uv
- [ ] Set up FastMCP framework
- [ ] Create basic project structure
- [ ] Configure development environment

### Phase 2: Core Registry Integration (Week 1-2)
- [ ] Implement PyPI registry client
- [ ] Implement npm registry client
- [ ] Implement pub.dev registry client
- [ ] Create base registry abstraction
- [ ] Add comprehensive error handling

### Phase 3: MCP Tool Implementation (Week 2)
- [ ] Implement get_latest_version tool
- [ ] Implement get_latest_versions_batch tool
- [ ] Add input validation
- [ ] Add response formatting

### Phase 4: Testing & Quality (Week 3)
- [ ] Unit tests for each registry
- [ ] Integration tests for MCP tools
- [ ] Mock external API calls
- [ ] Error scenario testing

### Phase 5: Documentation & Examples (Week 3)
- [ ] Complete README with installation instructions
- [ ] Add usage examples
- [ ] Document MCP client configuration
- [ ] Create troubleshooting guide

### Phase 6: Release (Week 4)
- [ ] Final testing
- [ ] Version 1.0.0 release
- [ ] GitHub repository setup
- [ ] Community announcement

---

## Success Metrics

### Quantitative Metrics

1. **Response Time**: 95th percentile < 1 second
2. **Accuracy**: 99.9% correct version information
3. **Availability**: 99.9% uptime
4. **Adoption**: 50+ GitHub stars in first 3 months

### Qualitative Metrics

1. **Developer Feedback**: Positive sentiment in issues/discussions
2. **LLM Compatibility**: Works seamlessly with major MCP clients
3. **Code Quality**: Maintainable, well-tested codebase
4. **Documentation**: Clear, comprehensive, beginner-friendly

---

## Future Roadmap (Post v1.0)

### v1.1 - Enhanced Features
- Cache layer for improved performance
- Support for specific version queries
- Package search/fuzzy matching

### v1.2 - Extended Coverage
- Rust (crates.io)
- Go (pkg.go.dev)
- Ruby (rubygems.org)

### v2.0 - Advanced Features
- Dependency tree analysis
- Version compatibility checking
- Security vulnerability detection
- Private registry support

---

## Dependencies

### Core Dependencies
- `fastmcp>=2.0.0` - MCP server framework
- `httpx>=0.27.0` - Async HTTP client
- `pydantic>=2.0.0` - Data validation

### Development Dependencies
- `pytest>=8.0.0` - Testing framework
- `pytest-asyncio>=0.23.0` - Async testing
- `pytest-cov>=4.1.0` - Coverage reporting
- `ruff>=0.3.0` - Linting and formatting
- `mypy>=1.9.0` - Type checking

---

## Configuration

### Environment Variables

```bash
# Optional: Custom registry URLs (for testing)
PYPI_REGISTRY_URL=https://pypi.org/pypi
NPM_REGISTRY_URL=https://registry.npmjs.org
PUBDEV_REGISTRY_URL=https://pub.dev/api

# Optional: Cache settings
CACHE_ENABLED=true
CACHE_TTL=3600

# Optional: Rate limiting
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=60
```

### MCP Client Configuration

```json
{
  "mcpServers": {
    "package-hero": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/udi/work/moinsen/opensource/mcp-package-hero",
        "mcp-package-hero"
      ]
    }
  }
}
```

---

## Risks and Mitigations

### Risk 1: Registry API Changes
**Impact**: High  
**Probability**: Medium  
**Mitigation**: 
- Abstract registry interfaces
- Comprehensive integration tests
- Monitor registry changelog

### Risk 2: Rate Limiting
**Impact**: Medium  
**Probability**: Medium  
**Mitigation**:
- Implement caching layer
- Respectful rate limiting
- Batch request optimization

### Risk 3: Package Name Conflicts
**Impact**: Low  
**Probability**: Low  
**Mitigation**:
- Require ecosystem parameter
- Clear error messages
- Documentation of edge cases

---

## Open Questions

1. Should we support pre-release versions? (Decision: Not in v1.0)
2. Should we cache results? (Decision: Simple in-memory cache in v1.0)
3. Should we support package name aliases? (Decision: Not in v1.0)
4. What's the appropriate batch size limit? (Decision: 10 packages)

---

## Approval

This PRD is a living document and will be updated as the project evolves.

**Author**: Udi (moinsen)  
**Created**: October 6, 2025  
**Last Updated**: October 6, 2025  
**Status**: Approved for Implementation
