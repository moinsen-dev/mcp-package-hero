"""Tests for pub.dev registry client."""

import pytest

from mcp_package_hero.models import VersionStatus
from mcp_package_hero.registries import PubDevRegistry


@pytest.mark.asyncio
async def test_get_latest_version_success():
    """Test successful version retrieval from pub.dev."""
    pubdev = PubDevRegistry()
    result = await pubdev.get_latest_version("http")

    assert result.status == VersionStatus.SUCCESS
    assert result.package_name == "http"
    assert result.latest_version is not None
    assert result.registry_url == "https://pub.dev/packages/http"


@pytest.mark.asyncio
async def test_get_latest_version_not_found():
    """Test handling of non-existent package."""
    pubdev = PubDevRegistry()
    result = await pubdev.get_latest_version("this-package-definitely-does-not-exist-xyz123")

    assert result.status == VersionStatus.NOT_FOUND
    assert result.latest_version is None
    assert result.error_message is not None
