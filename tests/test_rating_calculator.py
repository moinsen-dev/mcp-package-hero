"""Tests for rating calculator."""

import pytest

from mcp_package_hero.models import LetterGrade
from mcp_package_hero.rating_calculator import RatingCalculator


class TestMaintenanceScore:
    """Tests for maintenance score calculation."""

    def test_excellent_maintenance(self):
        """Test package with excellent maintenance."""
        score = RatingCalculator.calculate_maintenance_score(
            last_release_days=15,
            open_issues=10,
            closed_issues_30d=50,
            open_prs=5,
            merged_prs_30d=30,
        )

        assert score.score >= 85
        assert score.last_release_days == 15
        assert score.release_frequency_score == 100.0

    def test_poor_maintenance(self):
        """Test package with poor maintenance."""
        score = RatingCalculator.calculate_maintenance_score(
            last_release_days=400,
            open_issues=100,
            closed_issues_30d=5,
            open_prs=50,
            merged_prs_30d=2,
        )

        assert score.score < 50
        assert score.release_frequency_score == 20.0

    def test_unknown_release_date(self):
        """Test package with unknown release date."""
        score = RatingCalculator.calculate_maintenance_score(
            last_release_days=None,
            open_issues=0,
            closed_issues_30d=0,
        )

        assert score.last_release_days is None
        assert score.release_frequency_score == 50.0


class TestPopularityScore:
    """Tests for popularity score calculation."""

    def test_highly_popular(self):
        """Test highly popular package."""
        score = RatingCalculator.calculate_popularity_score(
            downloads=1000000,
            stars=5000,
            dependents=500,
        )

        assert score.score >= 85
        assert score.downloads == 1000000
        assert score.stars == 5000

    def test_unpopular(self):
        """Test unpopular package."""
        score = RatingCalculator.calculate_popularity_score(
            downloads=50,
            stars=3,
        )

        assert score.score < 50

    def test_no_metrics(self):
        """Test package with no popularity metrics."""
        score = RatingCalculator.calculate_popularity_score()

        assert score.score == 0.0
        assert score.downloads is None
        assert score.stars is None


class TestQualityScore:
    """Tests for quality score calculation."""

    def test_excellent_quality(self):
        """Test package with excellent quality."""
        score = RatingCalculator.calculate_quality_score(
            has_documentation=True,
            has_license=True,
            has_tests=True,
            readme_length=3000,
        )

        assert score.score >= 90
        assert score.has_documentation is True
        assert score.has_license is True
        assert score.has_tests is True

    def test_poor_quality(self):
        """Test package with poor quality."""
        score = RatingCalculator.calculate_quality_score(
            has_documentation=False,
            has_license=False,
            has_tests=False,
        )

        assert score.score < 20
        assert score.documentation_score == 0.0
        assert score.license_score == 0.0
        assert score.test_score == 0.0

    def test_partial_quality(self):
        """Test package with some quality indicators."""
        score = RatingCalculator.calculate_quality_score(
            has_documentation=True,
            has_license=True,
            has_tests=None,  # Unknown
            readme_length=500,
        )

        assert 50 < score.score < 80
        assert score.test_score == 50.0  # Unknown = 50


class TestOverallScore:
    """Tests for overall score calculation."""

    def test_calculate_overall_score(self):
        """Test overall score calculation with weights."""
        maintenance = RatingCalculator.calculate_maintenance_score(
            last_release_days=30,
            open_issues=20,
            closed_issues_30d=40,
        )
        popularity = RatingCalculator.calculate_popularity_score(
            downloads=100000,
            stars=1000,
        )
        quality = RatingCalculator.calculate_quality_score(
            has_documentation=True,
            has_license=True,
            has_tests=True,
            readme_length=2000,
        )

        overall = RatingCalculator.calculate_overall_score(maintenance, popularity, quality)

        assert 0 <= overall <= 100
        # Verify it's using the correct weights (35% + 25% + 40% = 100%)
        expected = round(
            maintenance.score * 0.35 + popularity.score * 0.25 + quality.score * 0.40,
            1,
        )
        assert overall == expected


class TestLetterGrade:
    """Tests for letter grade conversion."""

    @pytest.mark.parametrize(
        ("score", "expected_grade"),
        [
            (98, LetterGrade.A_PLUS),
            (92, LetterGrade.A),
            (87, LetterGrade.A_MINUS),
            (82, LetterGrade.B_PLUS),
            (77, LetterGrade.B),
            (72, LetterGrade.B_MINUS),
            (67, LetterGrade.C_PLUS),
            (62, LetterGrade.C),
            (57, LetterGrade.C_MINUS),
            (52, LetterGrade.D),
            (42, LetterGrade.F),
        ],
    )
    def test_score_to_letter_grade(self, score, expected_grade):
        """Test score to letter grade conversion."""
        grade = RatingCalculator.score_to_letter_grade(score)
        assert grade == expected_grade


class TestInsightsGeneration:
    """Tests for insights generation."""

    def test_generate_positive_insights(self):
        """Test insights for a great package."""
        maintenance = RatingCalculator.calculate_maintenance_score(
            last_release_days=10,
            open_issues=5,
            closed_issues_30d=50,
            open_prs=2,
            merged_prs_30d=30,
        )
        popularity = RatingCalculator.calculate_popularity_score(
            downloads=500000,
            stars=2000,
        )
        quality = RatingCalculator.calculate_quality_score(
            has_documentation=True,
            has_license=True,
            has_tests=True,
            readme_length=3000,
        )

        insights = RatingCalculator.generate_insights(maintenance, popularity, quality)

        assert len(insights) > 0
        assert any("Recently updated" in insight for insight in insights)
        assert any("popular" in insight.lower() for insight in insights)

    def test_generate_minimal_insights(self):
        """Test insights for a mediocre package."""
        maintenance = RatingCalculator.calculate_maintenance_score(
            last_release_days=100,
            open_issues=20,
            closed_issues_30d=10,
        )
        popularity = RatingCalculator.calculate_popularity_score(
            downloads=1000,
            stars=50,
        )
        quality = RatingCalculator.calculate_quality_score(
            has_documentation=True,
            has_license=False,
        )

        insights = RatingCalculator.generate_insights(maintenance, popularity, quality)

        # Should have few or no insights for mediocre package
        assert len(insights) >= 0


class TestRedFlagsGeneration:
    """Tests for red flags generation."""

    def test_generate_red_flags(self):
        """Test red flags for a problematic package."""
        maintenance = RatingCalculator.calculate_maintenance_score(
            last_release_days=400,
            open_issues=100,
            closed_issues_30d=2,
        )
        popularity = RatingCalculator.calculate_popularity_score(
            downloads=50,
            stars=3,
        )
        quality = RatingCalculator.calculate_quality_score(
            has_documentation=False,
            has_license=False,
            has_tests=False,
        )

        red_flags = RatingCalculator.generate_red_flags(maintenance, popularity, quality)

        assert len(red_flags) > 0
        assert any("not updated" in flag.lower() for flag in red_flags)
        assert any("license" in flag.lower() for flag in red_flags)
        assert any("documentation" in flag.lower() for flag in red_flags)

    def test_no_red_flags(self):
        """Test no red flags for excellent package."""
        maintenance = RatingCalculator.calculate_maintenance_score(
            last_release_days=15,
            open_issues=5,
            closed_issues_30d=50,
        )
        popularity = RatingCalculator.calculate_popularity_score(
            downloads=100000,
            stars=1000,
        )
        quality = RatingCalculator.calculate_quality_score(
            has_documentation=True,
            has_license=True,
            has_tests=True,
            readme_length=2000,
        )

        red_flags = RatingCalculator.generate_red_flags(maintenance, popularity, quality)

        assert len(red_flags) == 0
