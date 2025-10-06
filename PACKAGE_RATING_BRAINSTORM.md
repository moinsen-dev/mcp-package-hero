# Package Rating Feature - Brainstorming & Design

**Created:** 2025-10-06
**Status:** Concept/Brainstorming Phase
**For Version:** v2.0 (or v1.3)

---

## 🎯 Vision

**Goal:** Provide an intelligent package quality rating system that helps developers make informed decisions about package adoption.

**New MCP Tool:** `rate_package(package_name, ecosystem)` → Returns comprehensive quality rating

---

## 📊 What We Want to Rate

### Core Rating Dimensions

1. **Maintenance Health** (0-100)
   - Last updated/release date
   - Release frequency
   - Open issues vs closed issues ratio
   - Open PRs vs closed PRs ratio
   - Response time to issues
   - Active maintainers count

2. **Quality Metrics** (0-100)
   - Documentation quality
   - Test coverage (if available)
   - Code quality scores
   - Static analysis results
   - License presence
   - Changelog presence

3. **Popularity & Adoption** (0-100)
   - Download count
   - GitHub stars
   - Dependent packages count
   - Community engagement

4. **Security & Stability** (0-100)
   - Known vulnerabilities
   - Deprecated status
   - Breaking changes frequency
   - Version stability (semver compliance)

5. **Ecosystem Integration** (0-100)
   - Platform support
   - SDK/language version support
   - Dependency health
   - Build/CI status

**Overall Rating:** Weighted average → Letter grade (A+ to F) + Score (0-100)

---

## 🔍 Available Data Sources by Ecosystem

### 1. Python (PyPI)

#### PyPI JSON API
**Endpoint:** `https://pypi.org/pypi/{package}/json`

**Available Data:**
- ✅ Package metadata (name, version, description)
- ✅ Author information
- ✅ License
- ✅ Homepage, documentation, repository URLs
- ✅ Dependencies
- ✅ Release history
- ✅ Last release date
- ❌ No download counts in JSON API
- ❌ No quality scores

**Example Response:**
```json
{
  "info": {
    "name": "requests",
    "version": "2.31.0",
    "license": "Apache 2.0",
    "home_page": "https://requests.readthedocs.io",
    "project_urls": {
      "Source": "https://github.com/psf/requests"
    },
    "requires_python": ">=3.7"
  },
  "releases": { ... }
}
```

#### pypistats.org API
**Endpoint:** `https://pypistats.org/api/packages/{package}/recent`

**Available Data:**
- ✅ Recent download counts (last day, week, month)
- ✅ Download trends

#### GitHub API (if repo linked)
**Available Data:**
- ✅ Stars, forks, watchers
- ✅ Open/closed issues count
- ✅ Open/closed PRs count
- ✅ Last commit date
- ✅ Contributors count
- ✅ Has CI/CD workflows
- ✅ README content

---

### 2. JavaScript/TypeScript (npm)

#### npm Registry API
**Endpoint:** `https://registry.npmjs.org/{package}`

**Available Data:**
- ✅ Package metadata
- ✅ Repository URL
- ✅ License
- ✅ Dependencies
- ✅ Release history
- ✅ Maintainers
- ❌ No download counts
- ❌ No quality scores

#### npm Download Stats
**Endpoint:** `https://api.npmjs.org/downloads/point/last-month/{package}`

**Available Data:**
- ✅ Download counts (day/week/month)

#### npms.io API
**Endpoint:** `https://api.npms.io/v2/package/{package}`

**Available Data:**
- ✅ **Quality score** (0-1)
  - Has README, tests, linting
  - Code coverage
  - Outdated dependencies
- ✅ **Popularity score** (0-1)
  - Downloads
  - Dependents count
  - Stars
- ✅ **Maintenance score** (0-1)
  - Releases frequency
  - Open issues
  - Issues resolution time
- ✅ **Final score** (weighted average)

**Example Response:**
```json
{
  "score": {
    "final": 0.89,
    "detail": {
      "quality": 0.92,
      "popularity": 0.85,
      "maintenance": 0.90
    }
  },
  "evaluation": {
    "quality": {
      "carefulness": 0.8,
      "tests": 0.9,
      "health": 0.95,
      "branding": 0.9
    }
  }
}
```

---

### 3. Dart/Flutter (pub.dev)

#### pub.dev API
**Endpoint:** `https://pub.dev/api/packages/{package}/score`

**Available Data:**
- ✅ **Pub points** (0-130) - Quality score
  - Follow Dart conventions
  - Provide documentation
  - Platform support
  - Pass static analysis
  - Up-to-date dependencies
- ✅ **Popularity** (0-100%) - Usage percentile
- ✅ **Likes** - User-generated metric

**Example Response:**
```json
{
  "grantedPoints": 120,
  "maxPoints": 130,
  "likeCount": 1523,
  "popularityScore": 0.98,
  "tags": ["sdk:dart", "sdk:flutter"]
}
```

#### pub.dev Package Info
**Endpoint:** `https://pub.dev/api/packages/{package}`

**Available Data:**
- ✅ Repository URL
- ✅ Latest version
- ✅ Dependencies
- ✅ Supported platforms

---

### 4. Rust (crates.io)

#### crates.io API
**Endpoint:** `https://crates.io/api/v1/crates/{crate}`

**Available Data:**
- ✅ Downloads (total, recent)
- ✅ Repository URL
- ✅ Documentation URL
- ✅ Recent versions
- ✅ Dependencies
- ❌ No built-in quality scores

---

### 5. GitHub API (Universal)

**If package has GitHub repository:**

#### Repository Endpoint
**Endpoint:** `https://api.github.com/repos/{owner}/{repo}`

**Available Data:**
- ✅ Stars, forks, watchers
- ✅ Open issues count
- ✅ Last pushed date
- ✅ Default branch
- ✅ License
- ✅ Has wiki, issues enabled
- ✅ Topics/tags

#### Issues Endpoint
**Endpoint:** `https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=1`

**Available Data:**
- ✅ Total issues count (via Link header)
- ✅ Open vs closed ratio

#### Pull Requests Endpoint
**Endpoint:** `https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=1`

**Available Data:**
- ✅ Total PRs count
- ✅ Open vs closed/merged ratio

#### Community Health
**Endpoint:** `https://api.github.com/repos/{owner}/{repo}/community/profile`

**Available Data:**
- ✅ Has CODE_OF_CONDUCT
- ✅ Has CONTRIBUTING guide
- ✅ Has README
- ✅ Has LICENSE
- ✅ Has issue templates

**Rate Limit:** 60 requests/hour (unauthenticated), 5000/hour (authenticated)

---

## 🏗️ Proposed Architecture

### Option 1: Simple Scoring (MVP - Recommended)

**Focus:** Use readily available data without complex analysis

```python
class PackageRating(BaseModel):
    package_name: str
    ecosystem: Ecosystem
    overall_score: float  # 0-100
    grade: str  # A+, A, B+, B, C+, C, D, F

    # Sub-scores
    maintenance_score: float  # 0-100
    popularity_score: float   # 0-100
    quality_score: float      # 0-100

    # Raw metrics
    last_updated: datetime
    github_stars: Optional[int]
    open_issues: Optional[int]
    downloads_last_month: Optional[int]

    # Flags
    has_license: bool
    has_documentation: bool
    is_deprecated: bool

    checked_at: datetime
```

**Rating Calculation:**
```python
# Weighted scoring
overall_score = (
    maintenance_score * 0.35 +
    popularity_score * 0.25 +
    quality_score * 0.40
)

# Letter grades
A+ : 95-100
A  : 90-94
B+ : 85-89
B  : 80-84
C+ : 75-79
C  : 70-74
D  : 60-69
F  : 0-59
```

---

### Option 2: Ecosystem-Specific Scoring

**Use native scoring systems when available:**

- **pub.dev:** Use existing pub points + popularity
- **npm:** Use npms.io scores
- **PyPI:** Calculate custom score
- **Rust:** Calculate custom score

**Normalize all to 0-100 scale**

---

### Option 3: Hybrid Approach (Recommended for v2.0)

**Combine ecosystem scores + GitHub metrics + custom analysis**

1. Get ecosystem-native scores (if available)
2. Fetch GitHub metrics (if repo available)
3. Calculate custom metrics
4. Combine with weighted formula
5. Return unified rating

---

## 🛠️ Implementation Plan

### Phase 1: MVP - Simple Rating (v1.3)

**Effort:** 15-20 hours
**Timeline:** 2-3 weeks

#### Tasks:

1. **Create Rating Models** (2h)
   - Define `PackageRating` Pydantic model
   - Define sub-score models
   - Create rating calculation utilities

2. **Implement Data Fetchers** (6h)
   - Fetch package metadata (already have this!)
   - Add GitHub API integration
   - Add download stats fetchers
   - Add ecosystem-specific score fetchers

3. **Build Rating Calculator** (4h)
   - Maintenance score algorithm
   - Popularity score algorithm
   - Quality score algorithm
   - Overall score + grading

4. **Add MCP Tool** (2h)
   - `rate_package(package_name, ecosystem)` tool
   - Integrate with existing registries

5. **Testing** (3h)
   - Test across all ecosystems
   - Edge cases (missing GitHub, no scores)
   - Rate limiting handling

6. **Documentation** (2h)
   - Update README with rating feature
   - Add examples
   - Document scoring methodology

---

### Phase 2: Enhanced Rating (v2.0)

**Add:**
- Security vulnerability scanning
- Dependency health analysis
- Historical trend analysis
- Comparison with similar packages
- Confidence scores

---

## 📐 Scoring Algorithms (MVP)

### Maintenance Score (0-100)

```python
def calculate_maintenance_score(package_data, github_data):
    score = 0

    # Last updated (40 points)
    days_since_update = (now - last_release_date).days
    if days_since_update < 30:
        score += 40
    elif days_since_update < 90:
        score += 30
    elif days_since_update < 180:
        score += 20
    elif days_since_update < 365:
        score += 10
    # else: 0 points

    # GitHub activity (30 points) - if available
    if github_data:
        # Open vs closed issues ratio
        total_issues = open_issues + closed_issues
        if total_issues > 0:
            closed_ratio = closed_issues / total_issues
            score += closed_ratio * 15

        # PR merge rate
        total_prs = open_prs + merged_prs
        if total_prs > 0:
            merge_ratio = merged_prs / total_prs
            score += merge_ratio * 15

    # Release frequency (30 points)
    releases_last_year = count_releases_in_last_year()
    if releases_last_year >= 12:  # Monthly
        score += 30
    elif releases_last_year >= 6:  # Bi-monthly
        score += 25
    elif releases_last_year >= 4:  # Quarterly
        score += 20
    elif releases_last_year >= 2:  # Semi-annual
        score += 15
    elif releases_last_year >= 1:  # Annual
        score += 10

    return min(score, 100)
```

### Popularity Score (0-100)

```python
def calculate_popularity_score(package_data, github_data, downloads):
    score = 0

    # Downloads (50 points)
    if ecosystem == "pub.dev":
        # Use popularity percentage directly
        score += popularity_percentage * 50
    else:
        # Normalize downloads
        if downloads_last_month > 1000000:
            score += 50
        elif downloads_last_month > 100000:
            score += 40
        elif downloads_last_month > 10000:
            score += 30
        elif downloads_last_month > 1000:
            score += 20
        elif downloads_last_month > 100:
            score += 10

    # GitHub stars (30 points) - if available
    if github_data:
        if stars > 10000:
            score += 30
        elif stars > 5000:
            score += 25
        elif stars > 1000:
            score += 20
        elif stars > 500:
            score += 15
        elif stars > 100:
            score += 10
        elif stars > 10:
            score += 5

    # Dependent packages (20 points)
    # (If data available from ecosystem)

    return min(score, 100)
```

### Quality Score (0-100)

```python
def calculate_quality_score(package_data, github_data):
    score = 0

    # Use ecosystem scores if available
    if ecosystem == "pub.dev":
        pub_points_ratio = pub_points / max_pub_points
        return pub_points_ratio * 100

    elif ecosystem == "npm" and npms_score:
        return npms_score.quality * 100

    else:
        # Calculate manually

        # Has README (15 points)
        if has_readme:
            score += 15

        # Has LICENSE (15 points)
        if has_license:
            score += 15

        # Has documentation (20 points)
        if has_documentation_url:
            score += 20

        # Has CHANGELOG (10 points)
        if has_changelog:
            score += 10

        # Version >= 1.0.0 (10 points)
        if version >= "1.0.0":
            score += 10

        # Not deprecated (10 points)
        if not is_deprecated:
            score += 10

        # Has CI/CD (10 points) - if GitHub available
        if github_data and has_workflows:
            score += 10

        # Has tests (10 points) - if detectable
        if has_test_directory or has_test_coverage:
            score += 10

    return min(score, 100)
```

---

## 🎨 Example Output

### Tool Call:
```python
rate_package("requests", "python")
```

### Response:
```json
{
  "package_name": "requests",
  "ecosystem": "python",

  "overall_score": 92,
  "grade": "A",

  "maintenance_score": 85,
  "popularity_score": 98,
  "quality_score": 95,

  "metrics": {
    "last_updated": "2024-05-20T10:00:00Z",
    "days_since_update": 140,
    "github_stars": 51234,
    "open_issues": 145,
    "closed_issues": 4823,
    "downloads_last_month": 125000000,
    "has_license": true,
    "has_documentation": true,
    "is_deprecated": false,
    "version": "2.31.0"
  },

  "insights": [
    "✅ Extremely popular package (125M downloads/month)",
    "✅ Well-maintained with regular updates",
    "✅ Active issue resolution (97% closed)",
    "⚠️  Last update was 4 months ago",
    "✅ Comprehensive documentation"
  ],

  "checked_at": "2025-10-06T14:30:00Z"
}
```

---

## 💡 Integration Strategies

### Strategy 1: Extend Existing Registries (Recommended)

**Add rating method to BaseRegistry:**

```python
class BaseRegistry(ABC):
    async def get_latest_version(self, package_name: str) -> PackageVersion:
        """Existing method"""
        pass

    async def rate_package(self, package_name: str) -> PackageRating:
        """New method"""
        pass
```

Each registry implements its own rating logic using available data sources.

---

### Strategy 2: Separate Rating Service

**Create new module:** `src/mcp_package_hero/rating/`

```
rating/
├── __init__.py
├── rater.py          # Main PackageRater class
├── models.py         # PackageRating models
├── github.py         # GitHub API client
├── download_stats.py # Download statistics fetcher
├── calculators.py    # Score calculation algorithms
└── insights.py       # Generate insights from scores
```

---

### Strategy 3: Hybrid (Best for MVP)

1. Keep version checking in registries (existing)
2. Add rating as separate tool in server.py
3. Reuse registry clients for basic package data
4. Add GitHub client for additional metrics
5. Centralize scoring logic

---

## ⚠️ Challenges & Considerations

### 1. Rate Limiting

**Problem:** GitHub API has rate limits (60/hour unauthenticated)

**Solutions:**
- Cache ratings (TTL: 24 hours)
- Support GitHub token for authenticated requests (5000/hour)
- Graceful degradation (rating without GitHub data)
- Show "Limited data" warning when rate limited

### 2. Data Freshness

**Problem:** Some data might be stale

**Solution:**
- Include `checked_at` timestamp
- Cache TTL: 24 hours
- Allow force refresh option

### 3. Missing Data

**Problem:** Not all packages have GitHub repos

**Solution:**
- Graceful fallback
- Adjust scoring weights when data unavailable
- Clearly indicate data sources used

### 4. Consistency Across Ecosystems

**Problem:** Different ecosystems have different data

**Solution:**
- Normalize to common 0-100 scale
- Use ecosystem-specific weights
- Document methodology per ecosystem

### 5. Computational Cost

**Problem:** Multiple API calls per rating

**Solution:**
- Aggressive caching
- Async/parallel requests
- Optional "quick rating" (fewer data sources)

---

## 🎯 MVP Scope (v1.3)

### ✅ IN SCOPE

- Basic rating (maintenance, popularity, quality)
- Overall score (0-100) + letter grade (A-F)
- Support for all current ecosystems (Python, JS, Dart)
- GitHub integration (stars, issues, PRs)
- Download statistics
- Basic insights (3-5 bullet points)
- Caching (24h TTL)

### ❌ OUT OF SCOPE (for v2.0)

- Security vulnerability scanning
- Dependency health analysis
- Historical trends/charts
- Package comparison
- Custom weighting
- Advanced CI/CD analysis
- License compatibility checking
- Community health deep-dive

---

## 📊 Effort Estimation

| Task | Hours | Priority |
|------|-------|----------|
| Models & Data Structures | 2h | HIGH |
| GitHub API Client | 3h | HIGH |
| Download Stats Fetchers | 2h | MEDIUM |
| Ecosystem Score Fetchers | 2h | MEDIUM |
| Rating Calculators | 4h | HIGH |
| Insights Generator | 2h | MEDIUM |
| MCP Tool Integration | 2h | HIGH |
| Caching Layer | 2h | MEDIUM |
| Testing | 3h | HIGH |
| Documentation | 2h | HIGH |
| **TOTAL** | **24h** | |

**Buffer:** +6-8 hours for unknowns

**Total Estimated:** 30-32 hours
**Timeline:** 3-4 weeks (part-time)

---

## 🚀 Recommended Approach

### **For v1.3: MVP Rating Feature**

**Priority Order:**
1. Implement basic rating for **Python** first (test the concept)
2. Extend to **Dart** (has native scoring - easier)
3. Extend to **JavaScript** (use npms.io - easier)
4. Polish and release

**Why this order?**
- Python: Most complex (no native scores), best for testing algorithm
- Dart: Easiest (native pub points)
- JavaScript: Medium (npms.io API available)

### **Implementation Steps:**

**Week 1:** Foundation
- Create rating models
- Build GitHub API client
- Implement caching layer

**Week 2:** Python Rating
- Implement rating for PyPI
- Test and refine algorithms
- Add insights generation

**Week 3:** Dart & JavaScript
- Leverage native scores
- Unify output format
- Integration testing

**Week 4:** Polish & Release
- Documentation
- Examples
- CHANGELOG
- Release v1.3

---

## 🤔 Open Questions

1. **Should we require GitHub token for better rate limits?**
   - Pro: 5000 req/hour vs 60
   - Con: User setup friction

2. **How long should we cache ratings?**
   - 24 hours? 7 days? User-configurable?

3. **Should rating be a separate tool or part of version check?**
   - Separate: `rate_package()` - cleaner
   - Combined: `get_package_info()` - more comprehensive

4. **Include Rust/Go/Swift from the start?**
   - Wait for v1.2 (ecosystems) then add rating in v1.3?

5. **Quick vs Deep rating modes?**
   - Quick: Registry data only (fast, no rate limits)
   - Deep: + GitHub + downloads (slower, more accurate)

---

## ✅ Next Steps

1. **Review this brainstorm** - Get feedback on approach
2. **Decide on MVP scope** - Confirm what's in/out for v1.3
3. **Prototype Python rating** - Validate the concept
4. **Create tracking issue** - GitHub issue for feature
5. **Start implementation** - Begin with foundation

---

**Status:** 📝 **Ready for Review & Discussion**
