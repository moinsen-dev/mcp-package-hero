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

## [1.1.0] - 2025-10-06

### 🎉 Major Feature Release: Package Quality Rating System

This release adds comprehensive package quality analysis capabilities to MCP Package Hero.

### ✨ Features

#### New MCP Tool: `rate_package`
- **Comprehensive Package Rating**: Multi-dimensional quality analysis for Python, JavaScript, and Dart packages
  - Overall score (0-100) with letter grades (A+ to F)
  - Three scoring dimensions with configurable weights:
    - 🔧 Maintenance Health (35%): Release frequency, issue resolution, PR activity
    - 📊 Popularity (25%): Downloads, GitHub stars, community adoption
    - ✨ Quality Metrics (40%): Documentation, license, test indicators

#### Rating Components
- **Maintenance Score**:
  - Days since last release
  - Open/closed issue ratio (30-day window)
  - Open/merged PR ratio (30-day window)
- **Popularity Score**:
  - Monthly download counts
  - GitHub stars (logarithmic scale)
  - Dependent packages count
- **Quality Score**:
  - Documentation presence and quality
  - License detection
  - Test suite indicators

#### Ecosystem Integration
- **Python (PyPI)**: Custom scoring + GitHub metrics + pypistats.org downloads
- **JavaScript (npm)**: Blended scoring with npms.io quality/popularity/maintenance scores
- **Dart (pub.dev)**: Integration with native pub points and popularity scores

#### Insights & Red Flags
- **Actionable Insights**: Automatically generated positive highlights
  - "Recently updated (within last 30 days)"
  - "Highly popular with 100K+ monthly downloads"
  - "High quality package with good documentation and license"
- **Red Flags**: Warning signs for package quality issues
  - "Not updated in over a year"
  - "No license found"
  - "Low issue resolution rate"

### 🏗️ New Components

#### Core Modules
- `github_client.py`: GitHub API v3 client for repository metrics
  - Repository stats (stars, forks, watchers, issues)
  - Issue and PR statistics (30-day windows)
  - License detection
  - Last update tracking

- `rating_calculator.py`: Scoring algorithms and utilities
  - Maintenance score calculation
  - Popularity score calculation (logarithmic scaling)
  - Quality score calculation
  - Letter grade conversion
  - Insights and red flags generation

#### Rater Implementations
- `raters/python_rater.py`: Python package rating with PyPI + GitHub + pypistats
- `raters/javascript_rater.py`: JavaScript rating with npm + npms.io + GitHub
- `raters/dart_rater.py`: Dart rating with pub.dev native scores + GitHub

#### Data Models
- `LetterGrade` enum: A+, A, A-, B+, B, B-, C+, C, C-, D, F
- `MaintenanceScore`: Complete breakdown of maintenance metrics
- `PopularityScore`: Download and star metrics with sub-scores
- `QualityScore`: Documentation, license, and test indicators
- `PackageRating`: Comprehensive rating response with all components

### 🧪 Testing

#### New Test Suites
- `tests/test_rating_calculator.py`: 25 unit tests for scoring algorithms
  - Maintenance score edge cases
  - Popularity logarithmic scaling
  - Quality score combinations
  - Letter grade boundaries
  - Insights and red flags generation

- `tests/test_raters.py`: 15 integration tests for package raters
  - Real-world package rating (requests, react, http, flutter_bloc)
  - Error handling (nonexistent packages)
  - Ecosystem-specific score integration
  - Cross-ecosystem comparison

#### Test Results
- **Total Tests**: 48 (up from 8)
- **Status**: 48/48 passing ✅
- **Coverage**: Comprehensive coverage for all rating features

### 🔧 Changed

- Updated `server.py`:
  - Added `rate_package` tool
  - Updated version to 1.1.0
  - Enhanced MCP server instructions

- Updated `models.py`:
  - Added rating-related Pydantic models
  - All models use Pydantic V2 ConfigDict
  - Full type safety with field validation

### 📚 Documentation

- **README.md**:
  - Added Tool 3 documentation (rate_package)
  - Updated features section with quality rating capabilities
  - Added comprehensive example response
  - Updated test results (48 tests)
  - Updated project structure diagram
  - Updated roadmap with v1.1.0 completion

- **CHANGELOG.md**: This comprehensive release documentation

### 🎯 Design Decisions

- **Weighted Scoring**: Careful balance of maintenance (35%), quality (40%), and popularity (25%)
- **Logarithmic Scaling**: Downloads and stars use log scale to handle massive ranges (10 to 100M+)
- **Ecosystem Blending**: Native scores (pub points, npms.io) are blended with our calculations for better accuracy
- **Graceful Degradation**: Missing data (e.g., GitHub rate limits) doesn't crash - uses neutral scores
- **30-Day Windows**: Issue/PR statistics use rolling 30-day windows for recency

### 📦 Dependencies

No new dependencies added - uses existing httpx for all HTTP operations.

### 🐛 Fixed

- Fixed `.git` suffix removal in npm repository URLs (was truncating package names ending in 'git')
- Fixed float-to-int conversion for npms.io download counts

### 📝 Known Limitations

- GitHub API rate limiting (60 requests/hour unauthenticated)
  - Can be improved with GITHUB_TOKEN environment variable (5000 requests/hour)
- pypistats.org sometimes returns null for newer packages
- pub.dev doesn't expose download counts via API
- Test detection is heuristic-based (may have false negatives)

---

## [1.1.1] - 2025-10-07

### 🐛 Bug Fixes

This patch release fixes three critical bugs in the JavaScript package rating system that were causing significant underscoring of high-quality packages.

#### Fixed npms.io Score Access (javascript_rater.py)
- **Issue**: Incorrectly accessed `score.maintenance` instead of `score.detail.maintenance`
- **Impact**: npms.io quality scores returned 0 instead of actual values (e.g., 0.93 for React)
- **Fix**: Updated to correct API v2 structure path: `score.detail.{maintenance,popularity,quality}`
- **Result**: Packages now correctly receive blended scores from npms.io

#### Fixed GitHub Repository Name Mangling (github_client.py)
- **Issue**: Used `rstrip(".git")` which removed any trailing characters in ".git" string
- **Impact**: Repository names were corrupted:
  - `eslint` → `eslin`
  - `react` → `reac`
  - `typescript` → `typescrip`
- **Fix**: Changed to `removesuffix(".git")` for proper suffix removal
- **Result**: GitHub API calls now succeed, stars and metrics properly fetched

#### Switched to Official npm Downloads API (javascript_rater.py)
- **Issue**: Relied on npms.io for download counts, which is outdated/stale for many packages
- **Impact**: Severely incorrect download counts:
  - Expo: 0 downloads (actual: 7.7M/month)
  - TypeScript: 0 downloads (actual: 395M/month)
  - React: 72M downloads (actual: 189M/month)
- **Fix**:
  - Added `_get_npm_downloads()` method using official npm downloads API
  - Made npms.io optional, only used when data appears valid
  - Detect stale npms.io data (0 downloads when we have real data) and skip blending
- **Result**: Accurate, up-to-date download counts from npm registry

### 📊 Impact

Package ratings dramatically improved with accurate data:

| Package | Before (v1.1.0) | After (v1.1.1) | Improvement |
|---------|-----------------|----------------|-------------|
| **ESLint** | 46.3 (F) | **93.3 (A)** | +47.0 points |
| **React** | 40.7 (F) | **87.1 (A-)** | +46.4 points |
| **Expo** | 28.2 (F) | **81.4 (B+)** | +53.2 points |
| **TypeScript** | 48.5 (F) | **81.4 (B+)** | +32.9 points |
| **Zod** | 45.7 (F) | **89.4 (A-)** | +43.7 points |

### 🧪 Testing

- All 48 tests continue to pass
- Validated against real-world packages (React, ESLint, TypeScript, Expo, Zod)
- No regressions in existing functionality

### 🔧 Changed Files

- `src/mcp_package_hero/raters/javascript_rater.py`:
  - Lines 67-74: Switch to npm downloads API
  - Lines 76-95: Add npms.io stale data detection
  - Lines 153-156: Conditional npms.io insights
  - Lines 220-240: New `_get_npm_downloads()` method
- `src/mcp_package_hero/github_client.py`:
  - Line 197: Fix `rstrip()` → `removesuffix()`

---

## [Unreleased]

### Planned for v1.2
- [ ] Additional ecosystems: Rust (crates.io), Go (pkg.go.dev), Swift (SwiftPM)
- [ ] Cache layer for improved performance
- [ ] Support for specific version queries (not just latest)
- [ ] GitHub token configuration for higher rate limits

### Planned for v2.0
- [ ] Dependency tree analysis
- [ ] Version compatibility checking
- [ ] Security vulnerability detection
- [ ] Historical rating trends

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
