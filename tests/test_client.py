import httpx
import pytest

from pepkio_codon_host_fit_checker import (
    PepkioAPIError,
    PepkioAuthError,
    PepkioClient,
    PepkioNotFoundError,
    PepkioValidationError,
)

BASE_URL = "https://tools.pepkio.com"


def test_get_manifest_success():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/codon-host-fit-checker/manifest"
        return httpx.Response(
            200,
            json={
                "tool_id": "codon-host-fit-checker",
                "title": "Codon Host Fit Checker",
                "examples": [
                    {
                        "name": "gfp_matrix",
                        "input": {
                            "tab": "matrix",
                            "sequence": "ATGGTGAGCAAG",
                            "host_ids": ["e_coli_k12"],
                        },
                    }
                ],
            },
        )

    transport = httpx.MockTransport(handler)
    client_http = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", base_url=BASE_URL, client=client_http)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "codon-host-fit-checker"
    assert manifest["title"] == "Codon Host Fit Checker"

    typed = client.get_typed_manifest()
    assert typed.tool_id == "codon-host-fit-checker"
    assert typed.title == "Codon Host Fit Checker"


def test_run_success():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/codon-host-fit-checker/run"
        assert request.headers.get("Authorization") == "Bearer test_key"
        return httpx.Response(
            200,
            json={
                "run_id": "run_123",
                "status": "completed",
                "result": {"sequences": [{"host_metrics": [{"host_id": "e_coli_k12"}]}]},
                "error": None,
                "result_url": f"{BASE_URL}/api/tools/v1/runs/run_123",
                "permalink": f"{BASE_URL}/r/run_123",
            },
        )

    transport = httpx.MockTransport(handler)
    client_http = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", base_url=BASE_URL, client=client_http)

    res = client.run(
        input_data={
            "tab": "matrix",
            "sequence": "ATGGTGAGCAAG",
            "host_ids": ["e_coli_k12"],
        }
    )
    assert res.run_id == "run_123"
    assert res.status == "completed"
    assert res.result is not None
    assert res.result_url == f"{BASE_URL}/api/tools/v1/runs/run_123"


def test_get_run_success():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run_123"
        return httpx.Response(
            200,
            json={
                "run_id": "run_123",
                "status": "completed",
                "result": {"status": "ok"},
                "error": None,
            },
        )

    transport = httpx.MockTransport(handler)
    client_http = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", base_url=BASE_URL, client=client_http)

    res = client.get_run("run_123")
    assert res.run_id == "run_123"
    assert res.status == "completed"


def test_auth_error_401():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "Invalid API key"})

    transport = httpx.MockTransport(handler)
    client_http = httpx.Client(transport=transport)
    client = PepkioClient(api_key="bad_key", base_url=BASE_URL, client=client_http)

    with pytest.raises(PepkioAuthError) as exc_info:
        client.run(input_data={"tab": "matrix"})
    assert exc_info.value.status_code == 401


def test_not_found_404():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "Run not found"})

    transport = httpx.MockTransport(handler)
    client_http = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", base_url=BASE_URL, client=client_http)

    with pytest.raises(PepkioNotFoundError) as exc_info:
        client.get_run("non_existent")
    assert exc_info.value.status_code == 404


def test_body_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"run_id": "r1", "status": "failed", "error": "Execution error"},
        )

    transport = httpx.MockTransport(handler)
    client_http = httpx.Client(transport=transport)
    client = PepkioClient(api_key="test_key", base_url=BASE_URL, client=client_http)

    with pytest.raises(PepkioAPIError) as exc_info:
        client.run(input_data={"tab": "matrix"})
    assert "Execution error" in str(exc_info.value)


def test_validation_errors():
    client = PepkioClient(api_key="test_key", base_url=BASE_URL)
    with pytest.raises(PepkioValidationError):
        client.run("not a dict")  # type: ignore

    with pytest.raises(PepkioValidationError):
        client.get_run("")
