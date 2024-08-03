#!/usr/bin/env python

import os
from jiav import logger
from jiav.backend import BaseBackend, Result
from typing import List

jiav_logger = logger.subscribe_to_logger()


class ExampleBackend(BaseBackend):
    """
    ExampleBackend object

    An example backend for jiav

    Attributes:
        name   - Backend name
        schema - json_schema to be used to verify that the supplied step is
                 valid according to the backends's requirements
        step   - Backend excution instructions
    """

    MOCK_STEP = {"example": "example"}
    SCHEMA = {
        "type": "object",
        "required": ["example"],
        "properties": {"example": {"type": "string"}},
        "additionalProperties": False,
    }

    def __init__(self) -> None:
        self.name = "example"
        self.schema = self.SCHEMA
        self.step = self.MOCK_STEP
        super().__init__(name=self.name, schema=self.schema, step=self.step)

    # Overrdie method of BaseBackend
    def execute_backend(self) -> None:
        """
        Execute backend

        Returns a namedtuple describing the jiav manifest execution
        """
        # Parse required arugments
        example: str = self.step["example"]
        output: List = []
        errors: List = []
        successful: bool = False
        jiav_logger.debug(f"Example: {example}")
        try:
            os.environ["JIAV_EXAMPLE"] = example
            successful = True
            jiav_logger.debug(
                f"Environment variable 'JIAV_EXAMPLE' was set to '{example}'"
            )
            output.append(f"Environment variable 'JIAV_EXAMPLE' was set to '{example}'")
        except Exception as e:
            jiav_logger.error(e.text)  # type: ignore # pyright: ignore # pylint: disable=E1101
            errors.append(e.text)  # type: ignore # pyright: ignore # pylint: disable=E1101
        self.result = Result(successful, output, errors)
