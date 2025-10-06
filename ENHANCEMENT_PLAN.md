# Enhancement Plan: Adding Swift, Go, and Rust Support

**Project:** MCP Package Hero
**Version:** For v1.2 Release
**Created:** 2025-10-06
**Status:** Planning Phase

---

## 🎯 Executive Summary

This document outlines the plan to add support for three additional package ecosystems to MCP Package Hero:
- **Rust** (crates.io) - HIGH PRIORITY
- **Go** (proxy.golang.org / pkg.go.dev) - MEDIUM PRIORITY
- **Swift** (Swift Package Registry) - MEDIUM PRIORITY

**Estimated Timeline:** 4-6 weeks for all three
**Estimated Effort:** ~40-60 hours total
**Complexity:** Medium (similar to existing registries)

---

## 📊 Research Summary

### 1. Rust (crates.io)

**API Endpoint:** `https://crates.io/api/v1/crates/{crate_name}`

**Characteristics:**
- ✅ **Well-documented REST API**
- ✅ **JSON responses**
- ✅ **Similar to PyPI/npm**
- ⚠️ **Requires User-Agent header** (crates.io policy)
- ⚠️ **Rate limiting** (must respect crawler policy)
- ✅ **OpenAPI spec available** (https://crates.io/api/openapi.json)

**Response Structure:**
```json
{
  "crate": {
    "name": "serde",
    "max_version": "1.0.195",  // Latest version
    "newest_version": "1.0.195",
    "description": "...",
    "repository": "...",
    "documentation": "...",
    "homepage": "..."
  }
}
```

**Key Fields:**
- `max_version` or `newest_version` - Latest version number
- Standard semver format
- No authentication required for read operations

**Implementation Complexity:** ⭐⭐ (Low-Medium)
**Estimated Time:** 4-6 hours

---

### 2. Go (pkg.go.dev / proxy.golang.org)

**API Endpoints:**
- List versions: `https://proxy.golang.org/{module}/@v/list`
- Version info: `https://proxy.golang.org/{module}/@v/{version}.info`
- Latest: `https://proxy.golang.org/{module}/@latest`

**Characteristics:**
- ✅ **Go Module Proxy Protocol**
- ✅ **Simple text-based responses**
- ⚠️ **Different from JSON APIs** (plain text lists)
- ✅ **No authentication required**
- ⚠️ **Module path complexity** (e.g., github.com/org/repo)
- ✅ **Well-documented protocol**

**Response Format:**

`/@v/list` returns:
```
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

`/@latest` returns JSON:
```json
{
  "Version": "v1.2.3",
  "Time": "2025-01-15T12:00:00Z"
}
```

**Key Challenges:**
- Parsing plain text version lists
- Determining latest from list (semantic version comparison)
- Module path format validation

**Implementation Complexity:** ⭐⭐⭐ (Medium)
**Estimated Time:** 6-8 hours

---

### 3. Swift (Swift Package Registry)

**API Endpoint:** `GET /{scope}/{name}`

**Characteristics:**
- ⚠️ **Newer API** (still evolving)
- ✅ **JSON responses**
- ⚠️ **Requires specific Accept header** (`application/vnd.swift.registry.v1+json`)
- ⚠️ **Less widely used** (compared to CocoaPods historically)
- ⚠️ **Package scope required** (format: `scope.package`)
- ✅ **HTTPS required**
- ⚠️ **Multiple registries possible** (not centralized like PyPI)

**Response Structure:**
```json
{
  "releases": {
    "1.0.0": {
      "url": "..."
    }
  }
}
```

Plus `Link` header with `latest-version` relation

**Key Challenges:**
- Registry discovery (no central registry like PyPI)
- Scope/name format handling
- Less adoption = harder to test

**Implementation Complexity:** ⭐⭐⭐⭐ (Medium-High)
**Estimated Time:** 8-10 hours

---

## 🗺️ Implementation Roadmap

### Phase 1: Rust (crates.io) - Week 1-2

**Priority:** HIGH (part of original goals)

**Tasks:**
1. **Create `registries/rust.py`** (2 hours)
   - Implement `CratesIORegistry` class
   - Extend `BaseRegistry`
   - HTTP client with required User-Agent
   - Parse `max_version` or `newest_version` field

2. **Add to ecosystem enum** (30 mins)
   - Update `models.py` Ecosystem enum
   - Add "rust" option

3. **Update server.py** (30 mins)
   - Add crates.io registry instance
   - Update `get_registry()` function

4. **Write tests** (2 hours)
   - Success case (e.g., "serde")
   - Not found case
   - Error handling

5. **Documentation** (1 hour)
   - Update README with Rust examples
   - Update CHANGELOG

**Total Time:** ~6 hours
**Risk Level:** LOW

---

### Phase 2: Go (proxy.golang.org) - Week 2-3

**Priority:** MEDIUM

**Tasks:**
1. **Create `registries/go.py`** (3 hours)
   - Implement `GoProxyRegistry` class
   - Parse plain text version lists
   - Implement semver comparison for latest
   - Handle module path formats

2. **Add version parsing utility** (2 hours)
   - Semantic version comparison
   - Handle `v` prefix in versions
   - Support for retracted versions (skip them)

3. **Add to ecosystem enum** (30 mins)
   - Update models for "go" ecosystem

4. **Write tests** (2 hours)
   - Test with various module paths
   - Test version comparison logic
   - Edge cases (no versions, malformed)

5. **Documentation** (1 hour)
   - Go module path examples
   - Update docs

**Total Time:** ~8.5 hours
**Risk Level:** MEDIUM (text parsing, version comparison)

---

### Phase 3: Swift (Swift Package Registry) - Week 3-4

**Priority:** MEDIUM (future-looking)

**Tasks:**
1. **Research registry options** (2 hours)
   - Identify public Swift registries
   - Test API access
   - Determine default registry strategy

2. **Create `registries/swift.py`** (4 hours)
   - Implement `SwiftPMRegistry` class
   - Handle scope/name format
   - Parse response + Link header
   - Custom Accept header handling

3. **Add configuration** (1 hour)
   - Allow custom registry URL
   - Default registry selection

4. **Write tests** (2 hours)
   - Test with known packages
   - Mock tests for edge cases

5. **Documentation** (1 hour)
   - Swift package examples
   - Registry configuration docs

**Total Time:** ~10 hours
**Risk Level:** MEDIUM-HIGH (ecosystem maturity, registry discovery)

---

### Phase 4: Integration & Polish - Week 4

**Tasks:**
1. **Integration testing** (2 hours)
   - Test all 6 ecosystems together
   - Batch operations with mixed ecosystems
   - Performance testing

2. **Update README** (1 hour)
   - Feature list with all ecosystems
   - Updated badge counts
   - New examples

3. **Update CHANGELOG** (30 mins)
   - Document v1.2 features
   - Breaking changes (if any)

4. **Release preparation** (1 hour)
   - Version bump to 1.2.0
   - Final testing
   - Build and verify

**Total Time:** ~4.5 hours

---

## 📋 Detailed Task Breakdown

### Rust Implementation Details

**File:** `src/mcp_package_hero/registries/rust.py`

```python
"""Crates.io registry client."""

import httpx

from ..models import Ecosystem, PackageVersion, VersionStatus
from .base import BaseRegistry


class CratesIORegistry(BaseRegistry):
    """Client for crates.io package registry."""

    def __init__(self, base_url: str = "https://crates.io/api/v1"):
        """Initialize crates.io registry client."""
        super().__init__(Ecosystem.RUST, base_url)

    async def get_latest_version(self, package_name: str) -> PackageVersion:
        """
        Get the latest version from crates.io.

        Args:
            package_name: Name of the Rust crate

        Returns:
            PackageVersion with latest version info
        """
        url = f"{self.base_url}/crates/{package_name}"

        # crates.io requires User-Agent
        headers = {
            "User-Agent": "mcp-package-hero/1.2.0 (https://github.com/moinsen-dev/mcp-package-hero)"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)

                if response.status_code == 404:
                    return self._create_not_found_response(package_name)

                response.raise_for_status()
                data = response.json()

                # crates.io uses "newest_version" or "max_version"
                crate_data = data.get("crate", {})
                version = crate_data.get("newest_version") or crate_data.get("max_version")

                if not version:
                    return self._create_error_response(
                        package_name, "Version information not found in response"
                    )

                return PackageVersion(
                    package_name=package_name,
                    ecosystem=self.ecosystem,
                    latest_version=version,
                    registry_url=f"https://crates.io/crates/{package_name}",
                    status=VersionStatus.SUCCESS,
                )

        except httpx.HTTPStatusError as e:
            return self._create_error_response(
                package_name, f"HTTP error: {e.response.status_code}"
            )
        except httpx.RequestError as e:
            return self._create_error_response(
                package_name, f"Request failed: {e!s}"
            )
        except Exception as e:
            return self._create_error_response(
                package_name, f"Unexpected error: {e!s}"
            )
```

**Changes to models.py:**
```python
class Ecosystem(str, Enum):
    """Supported package ecosystems."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    DART = "dart"
    RUST = "rust"  # NEW
    GO = "go"      # NEW (Phase 2)
    SWIFT = "swift"  # NEW (Phase 3)
```

---

## ⏱️ Time Estimates Summary

| Phase | Ecosystem | Development | Testing | Docs | Total | Risk |
|-------|-----------|-------------|---------|------|-------|------|
| 1 | Rust | 3h | 2h | 1h | 6h | LOW |
| 2 | Go | 5.5h | 2h | 1h | 8.5h | MEDIUM |
| 3 | Swift | 7h | 2h | 1h | 10h | MEDIUM-HIGH |
| 4 | Integration | - | 2h | 1.5h | 4.5h | LOW |
| **TOTAL** | **All** | **15.5h** | **8h** | **4.5h** | **29h** | **MEDIUM** |

**Buffer for unknowns:** +10-15 hours
**Total Estimated Effort:** 40-45 hours
**Calendar Time:** 4-6 weeks (part-time development)

---

## 🎯 Success Criteria

### Per-Ecosystem Criteria

For each new ecosystem (Rust, Go, Swift):

- [ ] Registry client class implemented
- [ ] Extends BaseRegistry properly
- [ ] Success test case passing
- [ ] Not-found test case passing
- [ ] Error handling comprehensive
- [ ] Documentation complete with examples
- [ ] Ecosystem added to Enum
- [ ] Server updated to use new registry
- [ ] README updated
- [ ] CHANGELOG entry added

### Overall v1.2 Criteria

- [ ] All 6 ecosystems working (Python, JS, Dart, Rust, Go, Swift)
- [ ] Batch operations work with all ecosystems
- [ ] Test coverage maintained > 80%
- [ ] Type checking passing (mypy)
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Performance acceptable (< 2s for batch of 10)

---

## 🚧 Risks & Mitigations

### Risk 1: API Changes / Instability
**Impact:** HIGH
**Probability:** LOW-MEDIUM
**Mitigation:**
- Comprehensive error handling
- User-Agent headers for identification
- Monitor API changelog
- Graceful degradation

### Risk 2: Rate Limiting
**Impact:** MEDIUM
**Probability:** MEDIUM (especially crates.io)
**Mitigation:**
- Implement caching (v1.1 feature)
- Respect crawler policies
- Add rate limiting to client
- Document rate limits

### Risk 3: Swift Registry Fragmentation
**Impact:** MEDIUM
**Probability:** HIGH
**Mitigation:**
- Support custom registry URL configuration
- Default to most common registry
- Document registry configuration
- May defer to v1.3 if too complex

### Risk 4: Go Module Path Complexity
**Impact:** MEDIUM
**Probability:** MEDIUM
**Mitigation:**
- Thorough testing with various path formats
- Clear error messages
- Documentation with examples
- Handle common patterns (github.com/*, etc.)

### Risk 5: Maintenance Burden
**Impact:** MEDIUM
**Probability:** MEDIUM
**Mitigation:**
- Keep implementation simple
- Reuse existing patterns
- Comprehensive tests
- Good documentation

---

## 🔄 Alternative Approaches

### Option 1: Phased Release (RECOMMENDED)
- v1.2: Rust only (high priority, low risk)
- v1.3: Go + Swift

**Pros:**
- Faster initial value delivery
- Lower risk per release
- Learn from Rust implementation

**Cons:**
- More releases to manage
- Longer total timeline

### Option 2: All at Once
- v1.2: Rust + Go + Swift together

**Pros:**
- Single comprehensive update
- Consistent release messaging

**Cons:**
- Higher risk
- Longer development cycle
- Delayed value delivery

### Option 3: Community-Driven
- Rust: Core team
- Go/Swift: Accept community PRs

**Pros:**
- Distributed effort
- Community engagement

**Cons:**
- Quality variance
- Review overhead
- Timeline uncertainty

**DECISION: Start with Option 1 (Phased), with Option 2 if Rust goes smoothly**

---

## 📝 Prerequisites

Before starting implementation:

1. **Environment Setup**
   - [ ] Test Rust package lookup manually
   - [ ] Test Go proxy manually
   - [ ] Identify Swift registry to use
   - [ ] Document API responses

2. **Planning**
   - [x] Research complete
   - [ ] Decision on phased vs. all-at-once
   - [ ] Confirm priority order
   - [ ] Assign timeline

3. **Infrastructure**
   - [ ] Decide on caching strategy (if adding now)
   - [ ] Determine rate limiting approach
   - [ ] Plan for configuration (custom registries)

---

## 🎓 Learning Opportunities

### Technical Skills
- Working with different API styles (REST, text-based, custom protocols)
- Version comparison algorithms
- Protocol-specific error handling
- Multi-registry architecture

### Ecosystem Knowledge
- Rust packaging ecosystem
- Go module system
- Swift Package Manager

---

## 📊 Impact Analysis

### User Impact
- **Current users:** More ecosystems = more value
- **New users:** Attracts Rust/Go/Swift developers
- **Adoption:** Broader appeal in polyglot projects

### Maintenance Impact
- **Code complexity:** +30% (3 new registries / 3 existing)
- **Test suite:** +50% (more integration tests needed)
- **Documentation:** +40% (more examples, use cases)

### Performance Impact
- **Response time:** Minimal (async operations)
- **Error rate:** May increase initially (new APIs)
- **Resource usage:** Minimal (lightweight HTTP calls)

---

## ✅ Next Steps

### Immediate (Next 1-2 days)
1. Review this plan with stakeholders
2. Decide on phased vs. all-at-once approach
3. Set target dates for v1.2
4. Create GitHub milestone for v1.2
5. Create issues for each ecosystem

### Short-term (Week 1)
1. Start with Rust implementation
2. Set up test infrastructure
3. Update project board
4. Begin documentation

### Medium-term (Weeks 2-4)
1. Complete Rust, move to Go
2. Continuous testing and integration
3. Documentation updates
4. Prepare for release

---

## 📞 Questions for Discussion

1. **Priority Order:** Confirm Rust → Go → Swift is correct?
2. **Phasing:** Prefer v1.2 with all three, or separate releases?
3. **Swift:** Worth including given registry fragmentation?
4. **Caching:** Add caching layer as part of v1.2?
5. **Timeline:** Is 4-6 weeks acceptable for v1.2?
6. **Resources:** Solo development or seek contributors?

---

**Status:** ✅ **Research Complete - Ready for Review**
**Recommendation:** Start with Rust (Phase 1) for v1.2, evaluate Go/Swift based on effort
