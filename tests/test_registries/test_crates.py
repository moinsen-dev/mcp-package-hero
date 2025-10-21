"""Tests for crates.io registry client."""

import pytest

from mcp_package_hero.models import VersionStatus
from mcp_package_hero.registries import CratesRegistry


@pytest.mark.asyncio
async def test_get_latest_version_success():
    """Test successful version retrieval from crates.io."""
    crates = CratesRegistry()
    result = await crates.get_latest_version("serde")

    assert result.status == VersionStatus.SUCCESS
    assert result.package_name == "serde"
    assert result.latest_version is not None
    assert result.registry_url == "https://crates.io/crates/serde"


@pytest.mark.asyncio
async def test_get_latest_version_not_found():
    """Test handling of non-existent package."""
    crates = CratesRegistry()
    result = await crates.get_latest_version("this-package-definitely-does-not-exist-xyz123")

    assert result.status == VersionStatus.NOT_FOUND
    assert result.latest_version is None
    assert result.error_message is not None
