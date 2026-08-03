import os

DEFAULT_API_BASE_URL = "https://tools.pepkio.com"
TOOL_ID = "codon-host-fit-checker"


def get_api_base_url(override: str | None = None) -> str:
    """Return API base URL (override, env var, or production default)."""
    if override:
        return override.rstrip("/")
    env_url = os.getenv("PEPKIO_API_BASE_URL")
    if env_url:
        return env_url.rstrip("/")
    return DEFAULT_API_BASE_URL


def get_api_key(override: str | None = None) -> str | None:
    """Return API key from parameter or PEPKIO_API_KEY environment variable."""
    if override:
        return override
    return os.getenv("PEPKIO_API_KEY")
