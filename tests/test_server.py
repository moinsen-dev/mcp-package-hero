"""Tests for MCP server tools."""

import pytest
from fastmcp import Client

from mcp_package_hero.server import mcp


@pytest.mark.asyncio
async def test_get_latest_version_tool():
    """Test the get_latest_version MCP tool."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_latest_version",
            {"package_name": "requests", "ecosystem": "python"},
        )

        data = result.content[0].text
        assert "requests" in data
        assert "python" in data


@pytest.mark.asyncio
async def test_batch_version_check_tool():
    """Test the get_latest_versions_batch MCP tool."""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_latest_versions_batch",
            {
                "packages": [
                    {"package_name": "requests", "ecosystem": "python"},
                    {"package_name": "react", "ecosystem": "javascript"},
                ],
            },
        )

        data = result.content[0].text
        assert "requests" in data
        assert "react" in data
