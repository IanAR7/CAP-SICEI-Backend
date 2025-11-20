from datetime import datetime, timezone

from fastapi import HTTPException

from infrastructure.schemas.error_schema import ErrorDetail


def exception_detail_wrapper(status_code: int, exception: Exception, error_type: str = "Exception") -> HTTPException:
    error_detail = ErrorDetail(
        type=error_type,
        message=str(exception),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    return HTTPException(status_code=status_code, detail=[error_detail.model_dump()])
