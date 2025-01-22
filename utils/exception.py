from fastapi import status, FastAPI
from utils.error import (
    create_exception_handler,
    ServiceError,
    DataNotFoundError,
    ServicesConnectionError,
)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        exc_class_or_status_code=ServiceError,
        handler=create_exception_handler(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Service Error."
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=DataNotFoundError,
        handler=create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            "Data not found.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=ServicesConnectionError,
        handler=create_exception_handler(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Service connection error."
        ),
    )
