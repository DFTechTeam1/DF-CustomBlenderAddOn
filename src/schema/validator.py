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
            raise LLMParserError(detail="Invalid LLM response.")

        if task_type == "cluster":
            for key, value in response.items():
                if not isinstance(key, str):
                    logging.error(f"Key {key} must be a string.")
                    raise LLMParserError(detail="Invalid LLM response.")

                if not isinstance(value, list):
                    logging.error(f"Value for key {key} must be a list.")
                    raise LLMParserError(detail="Invalid LLM response.")

                if not all(isinstance(entry, str) for entry in value):
                    logging.error(f"All elements in the list of {key} must be strings.")
                    raise LLMParserError(detail="Invalid LLM response.")

            for key in list(response.keys()):
                if not response[key]:
                    logging.warning(f"Deleting key {key} due to produce empty data.")
                    del response[key]
        else:
            if not isinstance(response, str):
                logging.error("Response must be a string.")
                raise LLMParserError(detail="Invalid LLM response.")

        return response
