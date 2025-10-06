"""Tests for PyPI registry client."""

import pytest

from mcp_package_hero.models import VersionStatus
from mcp_package_hero.registries import PyPIRegistry


@pytest.mark.asyncio
async def test_get_latest_version_success():
    """Test successful version retrieval from PyPI."""
    pypi = PyPIRegistry()
    result = await pypi.get_latest_version("requests")

    assert result.status == VersionStatus.SUCCESS
    assert result.package_name == "requests"
    assert result.latest_version is not None
    assert result.registry_url == "https://pypi.org/project/requests/"


@pytest.mark.asyncio
async def test_get_latest_version_not_found():
    """Test handling of non-existent package."""
    pypi = PyPIRegistry()
    result = await pypi.get_latest_version("this-package-definitely-does-not-exist-xyz123")

    assert result.status == VersionStatus.NOT_FOUND
    assert result.latest_version is None
    assert result.error_message is not None
