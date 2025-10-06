"""Example usage of MCP Package Hero."""

import asyncio

from mcp_package_hero.registries import NpmRegistry, PubDevRegistry, PyPIRegistry


async def main():
    """Demonstrate basic usage of package registries."""
    print("🦸 MCP Package Hero - Example Usage\n")

    # Initialize registries
    pypi = PyPIRegistry()
    npm = NpmRegistry()
    pubdev = PubDevRegistry()

    # Check Python package
    print("📦 Checking Python package...")
    result = await pypi.get_latest_version("requests")
    print(f"  requests: {result.latest_version} ({result.status})")
    print(f"  URL: {result.registry_url}\n")

    # Check JavaScript package
    print("📦 Checking JavaScript package...")
    result = await npm.get_latest_version("react")
    print(f"  react: {result.latest_version} ({result.status})")
    print(f"  URL: {result.registry_url}\n")

    # Check Dart package
    print("📦 Checking Dart package...")
    result = await pubdev.get_latest_version("http")
    print(f"  http: {result.latest_version} ({result.status})")
    print(f"  URL: {result.registry_url}\n")

    # Check non-existent package
    print("📦 Checking non-existent package...")
    result = await pypi.get_latest_version("this-package-does-not-exist-xyz")
    print(f"  Status: {result.status}")
    print(f"  Message: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())
