#!/usr/bin/env python3
"""Small standard-library validator for the JSON Schema keywords in evals/schema.json."""

from __future__ import annotations

from typing import Any


SUPPORTED_KEYWORDS = {
    "$ref", "type", "required", "properties", "items", "enum", "oneOf",
    "minimum", "maximum", "minLength", "minItems", "maxItems",
}


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    return False


def _resolve_ref(root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError("only local JSON Schema references are supported")
    node: Any = root
    for part in reference[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    if not isinstance(node, dict):
        raise ValueError("schema reference does not resolve to an object")
    return node


def validate_instance(value: Any, schema: dict[str, Any], root: dict[str, Any] | None = None, path: str = "$", _depth: int = 0) -> list[str]:
    """Validate the supported Draft 2020-12 subset used by this package schema."""
    if _depth > 100:
        return ["{}: schema nesting exceeded safety limit".format(path)]
    root = schema if root is None else root
    if "$ref" in schema:
        try:
            target = _resolve_ref(root, schema["$ref"])
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            return ["{}: invalid schema reference: {}".format(path, exc)]
        return validate_instance(value, target, root, path, _depth + 1)

    errors = []
    declared = schema.get("type")
    if declared is not None:
        allowed = declared if isinstance(declared, list) else [declared]
        if not any(_matches_type(value, type_name) for type_name in allowed):
            return ["{}: expected type {}, got {}".format(path, " or ".join(allowed), type(value).__name__)]

    if "enum" in schema and value not in schema["enum"]:
        errors.append("{}: value is outside enum".format(path))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append("{}: value is below minimum".format(path))
        if "maximum" in schema and value > schema["maximum"]:
            errors.append("{}: value is above maximum".format(path))
    if isinstance(value, str) and "minLength" in schema and len(value) < schema["minLength"]:
        errors.append("{}: string is shorter than minLength".format(path))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append("{}: array is shorter than minItems".format(path))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append("{}: array is longer than maxItems".format(path))
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, schema["items"], root, "{}[{}]".format(path, index), _depth + 1))
    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append("{}: missing required property {}".format(path, required))
        for name, child_schema in schema.get("properties", {}).items():
            if name in value:
                errors.extend(validate_instance(value[name], child_schema, root, "{}.{}".format(path, name), _depth + 1))
    if "oneOf" in schema:
        match_count = 0
        for candidate in schema["oneOf"]:
            if not validate_instance(value, candidate, root, path, _depth + 1):
                match_count += 1
        if match_count != 1:
            errors.append("{}: expected exactly one oneOf branch, matched {}".format(path, match_count))
    return errors


def validate_schema_document(schema: dict[str, Any]) -> list[str]:
    """Reject unsupported validation keywords instead of silently ignoring them."""
    errors = []

    def visit(node: Any, path: str) -> None:
        if not isinstance(node, dict):
            return
        for key in node:
            if key == "$defs":
                for name, child in node[key].items():
                    visit(child, "{}/$defs/{}".format(path, name))
            elif key.startswith("$") or key in {"title", "description", "default", "examples"}:
                continue
            elif key == "properties":
                for name, child in node[key].items():
                    visit(child, "{}/{}/{}".format(path, key, name))
            elif key in {"items"}:
                visit(node[key], "{}/{}".format(path, key))
            elif key == "oneOf":
                for index, child in enumerate(node[key]):
                    visit(child, "{}/oneOf/{}".format(path, index))
            elif key not in SUPPORTED_KEYWORDS:
                errors.append("{}: unsupported schema keyword {}".format(path, key))

    visit(schema, "$")
    return errors
