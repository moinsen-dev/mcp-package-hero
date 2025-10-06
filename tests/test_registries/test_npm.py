"""Tests for npm registry client."""

import pytest

from mcp_package_hero.models import VersionStatus
from mcp_package_hero.registries import NpmRegistry


@pytest.mark.asyncio
async def test_get_latest_version_success():
    """Test successful version retrieval from npm."""
    npm = NpmRegistry()
    result = await npm.get_latest_version("react")

    assert result.status == VersionStatus.SUCCESS
    assert result.package_name == "react"
    assert result.latest_version is not None
    assert result.registry_url == "https://www.npmjs.com/package/react"


@pytest.mark.asyncio
async def test_get_latest_version_not_found():
    """Test handling of non-existent package."""
    npm = NpmRegistry()
    result = await npm.get_latest_version("this-package-definitely-does-not-exist-xyz123")

    assert result.status == VersionStatus.NOT_FOUND
    assert result.latest_version is None
    assert result.error_message is not None
