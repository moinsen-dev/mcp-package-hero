"""Data models for MCP Package Hero."""

from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Ecosystem(str, Enum):
    """Supported package ecosystems."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    DART = "dart"


class VersionStatus(str, Enum):
    """Status of version check."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    ERROR = "error"


class PackageVersion(BaseModel):
    """Package version information."""

    package_name: str = Field(..., description="Name of the package")
    ecosystem: Ecosystem = Field(..., description="Package ecosystem")
    latest_version: Optional[str] = Field(None, description="Latest stable version")
    registry_url: Optional[str] = Field(None, description="Link to package registry")
    checked_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of version check"
    )
    status: VersionStatus = Field(
        default=VersionStatus.SUCCESS, description="Status of the check"
    )
    error_message: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True


class BatchPackageRequest(BaseModel):
    """Request for batch package version check."""

    package_name: str = Field(..., description="Name of the package")
    ecosystem: Ecosystem = Field(..., description="Package ecosystem")


class BatchPackageResponse(BaseModel):
    """Response for batch package version check."""

    results: list[PackageVersion] = Field(..., description="List of version results")
    checked_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of batch check"
    )
