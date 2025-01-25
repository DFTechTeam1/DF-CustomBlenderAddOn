from typing import Union
from utils.error import InvalidOperationError


class UserInputValidatorMixin:
    @classmethod
    def validate_request(cls, user_input: Union[list, str]) -> Union[list, str]:
        if not user_input:
            raise InvalidOperationError(detail="Input cannot be empty.")
        return user_input


class LLMVResponseValidatorMixin:
    @classmethod
    def validate_response(cls, response: Union[dict, str]) -> Union[dict, str]:
        if not response:
            raise InvalidOperationError(
                detail="LLM Parsing Error: Response cannot be empty."
            )

        for key, value in response.items():
            if not (
                isinstance(value, list)
                and all(isinstance(item, (str, dict)) for item in value)
            ):
                raise InvalidOperationError(
                    detail=f"LLM Parsing Error: Invalid format for key '{key}' in 'data'."
                )
        return response
