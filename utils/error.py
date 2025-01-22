from utils.logger import logging
from typing import Callable
from fastapi import Request
from fastapi.responses import JSONResponse


class BaseErrorCustomBlenderAddOn(Exception):
    def __init__(
        self,
        detail: str = "Service is unavailable.",
        name: str = None,
    ) -> None:
        self.detail = detail
        self.name = name
        super().__init__(self.detail, self.name)


def create_exception_handler(
    status_code: int, detail_message: str
) -> Callable[[Request, BaseErrorCustomBlenderAddOn], JSONResponse]:
    detail = {"message": detail_message}

    async def exception_handler(
        _: Request, exc: BaseErrorCustomBlenderAddOn
    ) -> JSONResponse:
        if exc:
            detail["message"] = exc.detail

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        logging.error(exc)
        return JSONResponse(
            status_code=status_code,
            content={"detail": detail["message"]},
        )

    return exception_handler


class ServiceError(BaseErrorCustomBlenderAddOn):
    """Failures in internal Custom Blender Add On services."""

    pass


class DataNotFoundError(BaseErrorCustomBlenderAddOn):
    """Error occurred when target data not found."""

    pass


class ServicesConnectionError(BaseErrorCustomBlenderAddOn):
    """Error occurred when try to connecting third party services."""

    pass
