"""Validated NumPy operations used by the web app and unit tests."""
from __future__ import annotations

from typing import Any
import numpy as np

OPERATIONS = {"add", "subtract", "multiply", "transpose_a", "transpose_b"}


def _as_matrix(value: Any, name: str) -> np.ndarray:
    """Convert JSON input into a finite, non-empty 2D NumPy array."""
    try:
        matrix = np.asarray(value, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain valid numeric values.") from exc

    if matrix.ndim != 2:
        raise ValueError(f"{name} must be a two-dimensional matrix.")
    if matrix.size == 0 or 0 in matrix.shape:
        raise ValueError(f"{name} cannot be empty.")
    if matrix.shape[0] > 12 or matrix.shape[1] > 12:
        raise ValueError(f"{name} can have at most 12 rows and 12 columns.")
    if not np.isfinite(matrix).all():
        raise ValueError(f"{name} values must be finite numbers.")
    return matrix


def _json_number(value: float) -> int | float:
    """Return neat JSON numbers without unnecessary .0 decimal endings."""
    number = float(value)
    if number.is_integer():
        return int(number)
    return number


def _serialize(matrix: np.ndarray) -> list[list[int | float]]:
    return [[_json_number(value) for value in row] for row in matrix.tolist()]


def calculate(matrix_a: Any, matrix_b: Any, operation: Any) -> dict[str, Any]:
    """Calculate one supported matrix operation and return JSON-ready data."""
    if operation not in OPERATIONS:
        raise ValueError("Choose addition, subtraction, multiplication, transpose A, or transpose B.")

    a = _as_matrix(matrix_a, "Matrix A")
    b = _as_matrix(matrix_b, "Matrix B")

    if operation in ("add", "subtract") and a.shape != b.shape:
        raise ValueError("Addition and subtraction require matrices with the same dimensions.")
    if operation == "multiply" and a.shape[1] != b.shape[0]:
        raise ValueError(
            f"Matrix multiplication needs columns in A ({a.shape[1]}) to equal rows in B ({b.shape[0]})."
        )

    if operation == "add":
        result = np.add(a, b)
        title, explanation = "A + B", "Add the values in matching positions of A and B."
    elif operation == "subtract":
        result = np.subtract(a, b)
        title, explanation = "A − B", "Subtract each value in B from the value in the same position in A."
    elif operation == "multiply":
        result = np.matmul(a, b)
        title, explanation = "A × B", "Each result cell is a row-column dot product: multiply matching pairs, then add them."
    elif operation == "transpose_a":
        result = a.T
        title, explanation = "Aᵀ", "Transpose A by swapping its rows and columns."
    else:
        result = b.T
        title, explanation = "Bᵀ", "Transpose B by swapping its rows and columns."

    return {
        "operation": operation,
        "title": title,
        "result": _serialize(result),
        "shape": [int(result.shape[0]), int(result.shape[1])],
        "matrix_a_shape": [int(a.shape[0]), int(a.shape[1])],
        "matrix_b_shape": [int(b.shape[0]), int(b.shape[1])],
        "explanation": explanation,
    }
