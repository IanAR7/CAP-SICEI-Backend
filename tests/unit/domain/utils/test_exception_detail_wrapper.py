import pytest
from fastapi import HTTPException

from domain.utils.exception_detail_wrapper import exception_detail_wrapper


def test_exception_detail_wrapper_creates_http_exception():
    original_exception = ValueError("Invalid value")
    status_code = 400
    error_type = "ValueError"

    result = exception_detail_wrapper(
        status_code=status_code,
        exception=original_exception,
        error_type=error_type
    )

    assert isinstance(result, HTTPException)
    assert result.status_code == status_code

    assert isinstance(result.detail, list)
    assert len(result.detail) == 1

    detail = result.detail[0]

    assert detail["type"] == error_type
    assert detail["message"] == "Invalid value"
    assert "timestamp" in detail  # No validamos valor exacto porque es dinámico
