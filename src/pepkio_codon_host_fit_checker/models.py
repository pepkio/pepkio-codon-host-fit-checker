# SPDX-License-Identifier: MIT
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RunOptions(BaseModel):
    idempotency_key: Optional[str] = None
    label: Optional[str] = None


class RunResult(BaseModel):
    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Any] = None
    result_url: Optional[str] = None
    permalink: Optional[str] = None
    duration_ms: Optional[int] = None


class ToolExample(BaseModel):
    name: str
    input: Dict[str, Any]
    output: Optional[Dict[str, Any]] = None


class ToolManifest(BaseModel):
    schema_version: Optional[str] = None
    tool_id: str
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    category: Optional[str] = None
    execution_mode: Optional[str] = None
    estimated_runtime_sec: Optional[int] = None
    input: Optional[Dict[str, Any]] = None
    output: Optional[Dict[str, Any]] = None
    agent_notes: Optional[str] = None
    example_prompts: Optional[List[str]] = Field(default_factory=list)
    examples: Optional[List[ToolExample]] = Field(default_factory=list)
    limits: Optional[Dict[str, Any]] = None
    input_schema: Optional[Dict[str, Any]] = None
