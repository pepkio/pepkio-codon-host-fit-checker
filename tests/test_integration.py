import os
from pathlib import Path

import httpx
import pytest

from pepkio_codon_host_fit_checker import DEFAULT_API_BASE_URL, PepkioClient

# Load .env file from workspace root or package directory if available
for env_path in [
    Path(__file__).parents[2] / ".env",
    Path(__file__).parents[1] / ".env",
    Path.cwd() / ".env",
]:
    if env_path.exists():
        try:
            from dotenv import load_dotenv

            load_dotenv(env_path)
        except ImportError:
            pass


def get_target_config():
    """Determine target base URL and API key from environment."""
    base_url = os.getenv("PEPKIO_API_BASE_URL", DEFAULT_API_BASE_URL)
    if "localtest.me" in base_url:
        api_key = os.getenv("LOCAL_PEPKIO_API_KEY") or os.getenv("PEPKIO_API_KEY")
    else:
        api_key = os.getenv("PEPKIO_API_KEY")
    return base_url, api_key


@pytest.fixture
def client():
    base_url, api_key = get_target_config()
    if not api_key:
        pytest.skip("PEPKIO_API_KEY / LOCAL_PEPKIO_API_KEY not configured in environment")

    # For local testing, SSL verification might be disabled for self-signed dev certs
    if "localtest.me" in base_url:
        httpx_client = httpx.Client(verify=False, timeout=60.0)
    else:
        httpx_client = httpx.Client(timeout=60.0)

    c = PepkioClient(api_key=api_key, base_url=base_url, client=httpx_client)
    yield c
    c.close()


def test_integration_manifest(client: PepkioClient):
    manifest = client.get_manifest()
    assert manifest is not None
    assert manifest.get("tool_id") == "codon-host-fit-checker"
    assert "examples" in manifest
    assert len(manifest["examples"]) > 0


def test_integration_run_matrix_example(client: PepkioClient):
    manifest = client.get_manifest()
    examples = manifest.get("examples", [])
    example_input = None
    for ex in examples:
        if ex.get("name") == "gfp_matrix":
            example_input = ex.get("input")
            break
    if not example_input and examples:
        example_input = examples[0].get("input")

    assert example_input is not None, "No example input found in manifest"

    result = client.run(input_data=example_input, label="integration_test_matrix")
    assert result is not None
    assert result.status == "completed"
    assert result.run_id is not None
    assert result.result is not None

    fetched_run = client.get_run(result.run_id)
    assert fetched_run.run_id == result.run_id
    assert fetched_run.status == "completed"


def test_integration_run_inspector_example(client: PepkioClient):
    manifest = client.get_manifest()
    examples = manifest.get("examples", [])
    example_input = None
    for ex in examples:
        if ex.get("name") == "short_inspector":
            example_input = ex.get("input")
            break

    if example_input:
        result = client.run(input_data=example_input, label="integration_test_inspector")
        assert result.status == "completed"
        assert result.result is not None
