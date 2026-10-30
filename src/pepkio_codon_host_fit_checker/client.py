# SPDX-License-Identifier: MIT
from typing import Any, Dict, Optional

import httpx

from .config import TOOL_ID, get_api_base_url, get_api_key
from .exceptions import PepkioAPIError, PepkioAuthError, PepkioNotFoundError, PepkioValidationError
from .models import RunResult, ToolManifest


class PepkioClient:
    """Client for interacting with the Pepkio codon-host-fit-checker REST API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        client: Optional[httpx.Client] = None,
    ):
        self.api_key = get_api_key(api_key)
        self.base_url = get_api_base_url(base_url)
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.tool_id = TOOL_ID

        if client is not None:
            self._client = client
            self._external_client = True
        else:
            self._client = httpx.Client(timeout=self.timeout, verify=self.verify_ssl)
            self._external_client = False

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Validate response status and parse JSON."""
        try:
            data = response.json()
        except Exception:
            data = None

        if response.status_code in (401, 403):
            msg = (
                data.get("error", "Unauthorized or invalid API key")
                if isinstance(data, dict)
                else response.text
            )
            raise PepkioAuthError(
                f"Authentication failed ({response.status_code}): {msg}",
                status_code=response.status_code,
                response_body=data,
            )
        elif response.status_code == 404:
            msg = (
                data.get("error", "Resource not found") if isinstance(data, dict) else response.text
            )
            raise PepkioNotFoundError(
                f"Not found ({response.status_code}): {msg}",
                status_code=response.status_code,
                response_body=data,
            )
        elif response.status_code >= 400:
            msg = (
                data.get("error", f"HTTP {response.status_code} error")
                if isinstance(data, dict)
                else response.text
            )
            raise PepkioAPIError(
                f"API request failed ({response.status_code}): {msg}",
                status_code=response.status_code,
                response_body=data,
            )

        if not isinstance(data, dict):
            raise PepkioAPIError(
                "Invalid JSON response from server",
                status_code=response.status_code,
                response_body=response.text,
            )

        if data.get("error") is not None:
            err = data["error"]
            err_msg = err if isinstance(err, str) else str(err)
            raise PepkioAPIError(
                f"Run failed with error: {err_msg}",
                status_code=response.status_code,
                response_body=data,
            )

        return data

    def get_manifest(self) -> Dict[str, Any]:
        """Fetch the tool manifest containing schema, examples, and metadata."""
        url = f"{self.base_url}/api/tools/v1/tools/{self.tool_id}/manifest"
        response = self._client.get(url, headers=self._headers())
        return self._handle_response(response)

    def get_typed_manifest(self) -> ToolManifest:
        """Fetch and return the tool manifest as a typed Pydantic model."""
        raw_manifest = self.get_manifest()
        return ToolManifest.model_validate(raw_manifest)

    def run(
        self,
        input_data: Dict[str, Any],
        idempotency_key: Optional[str] = None,
        label: Optional[str] = None,
        **options: Any,
    ) -> RunResult:
        """Execute the codon-host-fit-checker tool with the given input data."""
        if not isinstance(input_data, dict):
            raise PepkioValidationError("input_data must be a dictionary")

        url = f"{self.base_url}/api/tools/v1/tools/{self.tool_id}/run"
        payload: Dict[str, Any] = {"input": input_data}

        opts: Dict[str, Any] = dict(options)
        if idempotency_key:
            opts["idempotency_key"] = idempotency_key
        if label:
            opts["label"] = label
        if opts:
            payload["options"] = opts

        response = self._client.post(url, json=payload, headers=self._headers())
        data = self._handle_response(response)
        return RunResult.model_validate(data)

    def get_run(self, run_id: str) -> RunResult:
        """Retrieve the status and results of a run by its ID."""
        if not run_id:
            raise PepkioValidationError("run_id cannot be empty")

        url = f"{self.base_url}/api/tools/v1/runs/{run_id}"
        response = self._client.get(url, headers=self._headers())
        data = self._handle_response(response)
        return RunResult.model_validate(data)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        if not self._external_client:
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
