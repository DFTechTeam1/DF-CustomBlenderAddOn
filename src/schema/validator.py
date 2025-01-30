from typing import Union, Literal
from utils.logger import logging
from utils.error import InvalidOperationError, LLMParserError


class UserInputValidatorMixin:
    @classmethod
    def validate_request(cls, user_input: Union[list, str]) -> Union[list, str]:
        if not user_input:
            raise InvalidOperationError(detail="Input cannot be empty.")
        return user_input


class LLMVResponseValidatorMixin:
    @classmethod
    def validate_response(
        cls, response: Union[dict, str], task_type: Literal["cluster", "code"]
    ) -> Union[dict, str]:
        if not response:
            logging.error("LLM response empty.")
            raise LLMParserError(detail="LLM response format is invalid.")

        if task_type == "cluster":
            for key, value in response.items():
                if not isinstance(key, str):
                    logging.error(f"Key {key} must be a string.")
                    raise LLMParserError(detail="LLM response format is invalid.")

                if not isinstance(value, list):
                    logging.error(f"Value for key {key} must be a list.")
                    raise LLMParserError(detail="LLM response format is invalid.")

                if not all(isinstance(entry, str) for entry in value):
                    logging.error(f"All elements in the list of {key} must be strings.")
                    raise LLMParserError(detail="LLM response format is invalid.")
        else:
            if not isinstance(response, str):
                logging.error("Response must be a string.")
                raise LLMParserError(detail="LLM response format is invalid.")

        return response
