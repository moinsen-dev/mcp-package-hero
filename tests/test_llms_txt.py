"""Tests for llms.txt functionality."""

import pytest

from mcp_package_hero.llms_txt_client import LLMsTxtClient
from mcp_package_hero.llms_txt_generator import LLMsTxtGenerator


class TestLLMsTxtClient:
    """Tests for LLMsTxtClient."""

    @pytest.fixture
    def client(self):
        """Create client instance."""
        return LLMsTxtClient()

    def test_parse_link_valid(self, client):
        """Test parsing valid markdown link."""
        line = "- [Title](https://example.com): Description"
        result = client._parse_link(line)

        assert result is not None
        assert result["title"] == "Title"
        assert result["url"] == "https://example.com"
        assert result["description"] == "Description"

    def test_parse_link_no_description(self, client):
        """Test parsing link without description."""
        line = "- [Title](https://example.com)"
        result = client._parse_link(line)

        assert result is not None
        assert result["title"] == "Title"
        assert result["url"] == "https://example.com"
        assert result["description"] == ""

    def test_parse_link_invalid(self, client):
        """Test parsing invalid link."""
        line = "- Not a link"
        result = client._parse_link(line)

        assert result is None

    def test_parse_llms_txt_basic(self, client):
        """Test parsing basic llms.txt content."""
        content = """# Project Name

> Project summary

Description paragraph.

## Documentation

- [README](README.md): Getting started
- [API](api.md): API reference
"""

        result = client._parse_llms_txt(content)

        assert result.project_name == "Project Name"
        assert result.summary == "Project summary"
        assert "Description paragraph" in result.description
        assert len(result.sections) == 1
        assert result.sections[0].title == "Documentation"
        assert len(result.sections[0].links) == 2
        assert result.is_valid is True
        assert len(result.validation_warnings) == 0

    def test_parse_llms_txt_no_h1(self, client):
        """Test parsing content without H1."""
        content = "> Summary only"

        result = client._parse_llms_txt(content)

        assert result.project_name == "Unknown"
        assert result.is_valid is False
        assert "Missing required H1 with project name" in result.validation_warnings

    def test_extract_repository_url(self, client):
        """Test extracting repository URL from registry data."""
        # Test direct key
        data = {"repository_url": "https://github.com/user/repo"}
        assert client._extract_repository_url(data) == "https://github.com/user/repo"

        # Test nested structure
        data = {"repository": {"url": "git+https://github.com/user/repo.git"}}
        result = client._extract_repository_url(data)
        assert result == "https://github.com/user/repo"

        # Test not found
        data = {}
        assert client._extract_repository_url(data) is None

    def test_extract_homepage_url(self, client):
        """Test extracting homepage URL from registry data."""
        # Test direct key
        data = {"homepage": "https://example.com"}
        assert client._extract_homepage_url(data) == "https://example.com"

        # Test non-http homepage
        data = {"homepage": "example.com"}
        assert client._extract_homepage_url(data) is None

        # Test not found
        data = {}
        assert client._extract_homepage_url(data) is None


class TestLLMsTxtGenerator:
    """Tests for LLMsTxtGenerator."""

    @pytest.fixture
    def generator(self):
        """Create generator instance."""
        return LLMsTxtGenerator()

    def test_generate_file_title(self, generator):
        """Test generating file titles."""
        assert generator._generate_file_title("README.md") == "README"
        assert generator._generate_file_title("CONTRIBUTING.md") == "Contributing Guide"
        assert generator._generate_file_title("api_reference.md") == "Api Reference"
        assert generator._generate_file_title("my-guide.md") == "My Guide"

    def test_generate_file_description(self, generator):
        """Test generating file descriptions."""
        assert "overview" in generator._generate_file_description("README.md").lower()
        assert "contributing" in generator._generate_file_description("CONTRIBUTING.md").lower()
        assert "tutorial" in generator._generate_file_description("docs/tutorials/intro.md").lower()
        assert generator._generate_file_description("random.md") == ""

    def test_generate_markdown_basic(self, generator):
        """Test generating basic markdown."""
        project_name = "Test Project"
        description = "A test project"
        discovered_files = {
            "documentation": ["README.md"],
            "examples": ["examples/basic.py"],
        }

        result = generator._generate_markdown(
            project_name=project_name,
            description=description,
            discovered_files=discovered_files,
        )

        assert "# Test Project" in result
        assert "> A test project" in result
        assert "## Documentation" in result
        assert "README.md" in result
        assert "## Examples" in result
        assert "examples/basic.py" in result

    def test_generate_markdown_empty_files(self, generator):
        """Test generating markdown with no files."""
        project_name = "Test Project"
        description = "A test project"
        discovered_files = {}

        result = generator._generate_markdown(
            project_name=project_name,
            description=description,
            discovered_files=discovered_files,
        )

        assert "# Test Project" in result
        assert "> A test project" in result
        # Should not have any sections
        assert "##" not in result.split("\n", 3)[-1]

    @pytest.mark.asyncio
    async def test_generate_success(self, generator):
        """Test successful generation."""
        result = await generator.generate(
            project_name="Test Project",
            description="A test description",
            scan_directory=".",
            include_file_tree=False,  # Don't scan real files in test
        )

        assert result.status == "success"
        assert "# Test Project" in result.content
        assert "> A test description" in result.content
        assert result.suggested_path.endswith("llms.txt")
