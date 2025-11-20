from pydantic import BaseModel


class ErrorDetail(BaseModel):
    type: str
    message: str
    timestamp: str


class ErrorResponse(BaseModel):
    detail: list[ErrorDetail]
