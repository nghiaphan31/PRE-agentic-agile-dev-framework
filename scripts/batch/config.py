"""
config.py — BatchConfig dataclass and YAML loader

Defines the configuration format for batch jobs. Each batch is described
by a YAML file that specifies the model, requests, and output locations.

Usage:
    config = BatchConfig.from_yaml("batch.yaml")
    config = BatchConfig.from_dict(data)
"""

from __future__ import annotations

import os
import pathlib
from dataclasses import dataclass, field
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class RequestSpec:
    """
    Specification for a single request within a batch.

    Attributes:
        custom_id:     Unique identifier for this request (used in results)
        system:        System prompt for this request
        user_message:  User message / prompt for this request
    """

    custom_id: str
    system: str = ""
    user_message: str = ""

    def to_anthropic_request(
        self,
        model: str,
        max_tokens: int,
        temperature: float,
    ) -> dict:
        """Build an Anthropic API request dict."""
        params: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": self.user_message}],
        }
        if self.system:
            params["system"] = self.system
        return params


@dataclass
class BatchConfig:
    """
    Configuration for a batch job.

    Attributes:
        name:          Human-readable name for this batch
        description:   Longer description of what this batch does
        model:         Anthropic model to use (e.g. "claude-sonnet-4-6")
        max_tokens:    Max output tokens per request
        temperature:    Sampling temperature (0.0–1.0)
        output_dir:    Directory to write results into
        requests:       List of RequestSpec objects
        batch_id_file:  File to persist/load batch_id (default: <output_dir>/batch_id.txt)
        workspace_root: Root directory for resolving relative paths (default: cwd)
    """

    name: str
    description: str
    model: str
    max_tokens: int
    temperature: float
    output_dir: pathlib.Path
    requests: list[RequestSpec] = field(default_factory=list)
    batch_id_file: pathlib.Path | None = None
    workspace_root: pathlib.Path = field(default_factory=lambda: pathlib.Path.cwd())

    # ---------------------------------------------------------------------------
    # Derived properties
    # ---------------------------------------------------------------------------

    @property
    def batch_id_path(self) -> pathlib.Path:
        """Path to the batch_id file."""
        if self.batch_id_file:
            return self.workspace_root / self.batch_id_file
        return self.workspace_root / self.output_dir / "batch_id.txt"

    # ---------------------------------------------------------------------------
    # YAML loading
    # ---------------------------------------------------------------------------

    @classmethod
    def from_yaml(cls, path: str | pathlib.Path) -> "BatchConfig":
        """
        Load BatchConfig from a YAML file.

        The YAML format is:

            name: "Governance Coherence Audit"
            description: "Audit SP-002/.clinerules, SP-003..006/.roomodes"
            model: "claude-sonnet-4-6"
            max_tokens: 4096
            temperature: 0.3
            output_dir: "plans/batch-full-audit/RESULTS"
            batch_id_file: "plans/batch-full-audit/batch_id_gov.txt"  # optional
            workspace_root: "."  # optional, default: cwd

            requests:
              - custom_id: "gov-sp-clinerules"
                system: "You are an auditor..."
                user_message: "Please audit..."
        """
        p = pathlib.Path(path)
        if not p.exists():
            raise FileNotFoundError(
                f"Batch config file not found: {p}\n"
                "Run this script from the workspace root directory."
            )

        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
        if raw is None:
            raise ValueError(f"Empty batch config file: {p}")

        return cls.from_dict(raw, workspace_root=p.parent)

    @classmethod
    def from_dict(cls, data: dict[str, Any], workspace_root: pathlib.Path | None = None) -> "BatchConfig":
        """
        Build BatchConfig from a dict (e.g. parsed YAML).

        Relative paths in output_dir/batch_id_file are resolved against
        workspace_root (default: cwd).
        """
        ws = (workspace_root or pathlib.Path.cwd())

        output_dir = cls._resolve_path(data.get("output_dir", "batch_results"), ws)
        batch_id_file = cls._resolve_path(data["batch_id_file"], ws) if data.get("batch_id_file") else None

        requests = []
        for r in data.get("requests", []):
            requests.append(
                RequestSpec(
                    custom_id=str(r["custom_id"]),
                    system=r.get("system", ""),
                    user_message=r.get("user_message", ""),
                )
            )

        return cls(
            name=str(data["name"]),
            description=str(data.get("description", "")),
            model=str(data.get("model", "claude-sonnet-4-6")),
            max_tokens=int(data.get("max_tokens", 4096)),
            temperature=float(data.get("temperature", 0.3)),
            output_dir=output_dir,
            batch_id_file=batch_id_file,
            workspace_root=ws,
        )

    # ---------------------------------------------------------------------------
    # Batch ID persistence
    # ---------------------------------------------------------------------------

    def save_batch_id(self, batch_id: str) -> None:
        """Persist the batch ID to disk."""
        path = self.batch_id_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(batch_id, encoding="utf-8")

    def load_batch_id(self) -> str | None:
        """
        Load a previously-saved batch ID.

        Returns None if the file doesn't exist.
        """
        path = self.batch_id_path
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8").strip()

    # ---------------------------------------------------------------------------
    # Validation
    # ---------------------------------------------------------------------------

    def validate(self) -> list[str]:
        """
        Validate the config and return a list of error messages.

        Returns empty list if valid.
        """
        errors = []

        if not self.name:
            errors.append("name is required")
        if not self.model:
            errors.append("model is required")
        if self.max_tokens <= 0:
            errors.append("max_tokens must be positive")
        if not (0.0 <= self.temperature <= 1.0):
            errors.append("temperature must be between 0.0 and 1.0")
        if not self.requests:
            errors.append("at least one request is required")

        seen_ids: set[str] = set()
        for req in self.requests:
            if not req.custom_id:
                errors.append("each request must have a custom_id")
            elif req.custom_id in seen_ids:
                errors.append(f"duplicate custom_id: {req.custom_id}")
            else:
                seen_ids.add(req.custom_id)
            if not req.user_message:
                errors.append(f"request '{req.custom_id}' has empty user_message")

        return errors

    # ---------------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------------

    @staticmethod
    def _resolve_path(path: str | Any, base: pathlib.Path) -> pathlib.Path:
        """Resolve a potentially-relative path against a base directory."""
        if not isinstance(path, str):
            raise TypeError(f"Expected string path, got {type(path).__name__}")
        p = pathlib.Path(path)
        if p.is_absolute():
            return p
        return base / p
