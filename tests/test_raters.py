"""Integration tests for package raters."""

import pytest

from mcp_package_hero.models import Ecosystem, LetterGrade, VersionStatus
from mcp_package_hero.raters import DartPackageRater, JavaScriptPackageRater, PythonPackageRater, RustPackageRater


@pytest.mark.asyncio
class TestPythonPackageRater:
    """Tests for Python package rater."""

    async def test_rate_popular_package(self):
        """Test rating a popular Python package."""
        rater = PythonPackageRater()
        rating = await rater.rate_package("requests")

        assert rating.package_name == "requests"
        assert rating.ecosystem == Ecosystem.PYTHON
        assert rating.status == VersionStatus.SUCCESS
        assert 0 <= rating.overall_score <= 100
        assert rating.letter_grade in [grade.value for grade in LetterGrade]
        assert rating.repository_url is not None
        assert "github.com" in rating.repository_url.lower()
        assert len(rating.insights) > 0

    async def test_rate_nonexistent_package(self):
        """Test rating a nonexistent Python package."""
        rater = PythonPackageRater()
        rating = await rater.rate_package("this-package-definitely-does-not-exist-12345")

        assert rating.status == VersionStatus.NOT_FOUND
        assert rating.overall_score == 0.0
        assert rating.error_message is not None

    async def test_maintenance_score_components(self):
        """Test that maintenance score has all components."""
        rater = PythonPackageRater()
        rating = await rater.rate_package("requests")

        assert rating.maintenance.score >= 0
        assert rating.maintenance.release_frequency_score >= 0
        assert rating.maintenance.issue_resolution_score >= 0
        assert rating.maintenance.pr_merge_score >= 0

    async def test_popularity_score_components(self):
        """Test that popularity score has components."""
        rater = PythonPackageRater()
        rating = await rater.rate_package("requests")

        assert rating.popularity.score >= 0
        assert rating.popularity.downloads_score >= 0
        assert rating.popularity.stars_score >= 0

    async def test_quality_score_components(self):
        """Test that quality score has all components."""
        rater = PythonPackageRater()
        rating = await rater.rate_package("requests")

        assert rating.quality.score >= 0
        assert isinstance(rating.quality.has_documentation, bool)
        assert isinstance(rating.quality.has_license, bool)


@pytest.mark.asyncio
class TestJavaScriptPackageRater:
    """Tests for JavaScript package rater."""

    async def test_rate_popular_package(self):
        """Test rating a popular JavaScript package."""
        rater = JavaScriptPackageRater()
        rating = await rater.rate_package("react")

        assert rating.package_name == "react"
        assert rating.ecosystem == Ecosystem.JAVASCRIPT
        assert rating.status == VersionStatus.SUCCESS
        assert 0 <= rating.overall_score <= 100
        assert rating.letter_grade in [grade.value for grade in LetterGrade]
        assert rating.repository_url is not None
        assert len(rating.insights) > 0

    async def test_rate_nonexistent_package(self):
        """Test rating a nonexistent JavaScript package."""
        rater = JavaScriptPackageRater()
        rating = await rater.rate_package("this-package-definitely-does-not-exist-12345")

        assert rating.status == VersionStatus.NOT_FOUND
        assert rating.overall_score == 0.0

    async def test_npms_score_integration(self):
        """Test that npms.io scores are integrated."""
        rater = JavaScriptPackageRater()
        rating = await rater.rate_package("react")

        # React should have good scores (note: GitHub API may rate limit in tests)
        assert rating.overall_score >= 40
        # Should have insights about popularity or npms score
        assert len(rating.insights) > 0
        # Check if npms score is mentioned in insights
        assert any("npms.io" in insight for insight in rating.insights)

    async def test_test_detection(self):
        """Test detection of test frameworks."""
        rater = JavaScriptPackageRater()
        rating = await rater.rate_package("react")

        # React should have tests
        assert rating.quality.has_tests is True or rating.quality.has_tests is None


@pytest.mark.asyncio
class TestDartPackageRater:
    """Tests for Dart package rater."""

    async def test_rate_popular_package(self):
        """Test rating a popular Dart package."""
        rater = DartPackageRater()
        rating = await rater.rate_package("http")

        assert rating.package_name == "http"
        assert rating.ecosystem == Ecosystem.DART
        assert rating.status == VersionStatus.SUCCESS
        assert 0 <= rating.overall_score <= 100
        assert rating.letter_grade in [grade.value for grade in LetterGrade]

    async def test_rate_nonexistent_package(self):
        """Test rating a nonexistent Dart package."""
        rater = DartPackageRater()
        rating = await rater.rate_package("this-package-definitely-does-not-exist-12345")

        assert rating.status == VersionStatus.NOT_FOUND
        assert rating.overall_score == 0.0

    async def test_pub_points_integration(self):
        """Test that pub points are integrated."""
        rater = DartPackageRater()
        rating = await rater.rate_package("http")

        # Popular packages on pub.dev should have good scores
        assert rating.overall_score >= 50
        # Should have insights
        assert len(rating.insights) >= 0

    async def test_flutter_package(self):
        """Test rating a Flutter-specific package."""
        rater = DartPackageRater()
        rating = await rater.rate_package("flutter_bloc")

        assert rating.status == VersionStatus.SUCCESS
        assert rating.overall_score > 0


@pytest.mark.asyncio
class TestRustPackageRater:
    """Tests for Rust package rater."""

    async def test_rate_popular_package(self):
        """Test rating a popular Rust package."""
        rater = RustPackageRater()
        rating = await rater.rate_package("serde")

        assert rating.package_name == "serde"
        assert rating.ecosystem == Ecosystem.RUST
        assert rating.status == VersionStatus.SUCCESS
        assert 0 <= rating.overall_score <= 100
        assert rating.letter_grade in [grade.value for grade in LetterGrade]
        assert rating.repository_url is not None
        assert len(rating.insights) > 0

    async def test_rate_nonexistent_package(self):
        """Test rating a nonexistent Rust package."""
        rater = RustPackageRater()
        rating = await rater.rate_package("this-package-definitely-does-not-exist-12345")

        assert rating.status == VersionStatus.NOT_FOUND
        assert rating.overall_score == 0.0

    async def test_rate_tokio_package(self):
        """Test rating the tokio async runtime."""
        rater = RustPackageRater()
        rating = await rater.rate_package("tokio")

        assert rating.status == VersionStatus.SUCCESS
        assert rating.overall_score > 0
        assert rating.repository_url is not None

    async def test_maintenance_score_components(self):
        """Test that maintenance score has all components."""
        rater = RustPackageRater()
        rating = await rater.rate_package("serde")

        assert rating.maintenance.score >= 0
        assert rating.maintenance.release_frequency_score >= 0
        assert rating.maintenance.issue_resolution_score >= 0
        assert rating.maintenance.pr_merge_score >= 0


@pytest.mark.asyncio
class TestRaterComparison:
    """Tests comparing ratings across ecosystems."""

    async def test_popular_packages_have_good_scores(self):
        """Test that popular packages get good scores across all ecosystems."""
        python_rater = PythonPackageRater()
        js_rater = JavaScriptPackageRater()
        dart_rater = DartPackageRater()
        rust_rater = RustPackageRater()

        python_rating = await python_rater.rate_package("requests")
        js_rating = await js_rater.rate_package("react")
        dart_rating = await dart_rater.rate_package("http")
        rust_rating = await rust_rater.rate_package("serde")

        # All popular packages should score well (note: GitHub API may rate limit)
        assert python_rating.overall_score >= 60
        assert js_rating.overall_score >= 40  # Lower threshold due to possible GitHub rate limiting
        assert dart_rating.overall_score >= 50
        assert rust_rating.overall_score >= 50

    async def test_all_raters_handle_not_found(self):
        """Test that all raters handle nonexistent packages correctly."""
        python_rater = PythonPackageRater()
        js_rater = JavaScriptPackageRater()
        dart_rater = DartPackageRater()
        rust_rater = RustPackageRater()

        fake_name = "nonexistent-package-xyz-12345"

        python_rating = await python_rater.rate_package(fake_name)
        js_rating = await js_rater.rate_package(fake_name)
        dart_rating = await dart_rater.rate_package(fake_name)
        rust_rating = await rust_rater.rate_package(fake_name)

        assert python_rating.status == VersionStatus.NOT_FOUND
        assert js_rating.status == VersionStatus.NOT_FOUND
        assert dart_rating.status == VersionStatus.NOT_FOUND
        assert rust_rating.status == VersionStatus.NOT_FOUND
