"""Test `fields`."""
from typing import Any, List
from unittest import TestCase

import pytest
from rest_framework import serializers

from ..fields import ConstrainedFileField

__all__ = ("TestFileField",)

# Generic helpers for testing of django-rest-framework fields.
# Most of the code was copied from the django-rest-framework
# https://github.com/encode/django-rest-framework/blob/master/tests/test_fields.py
# ----------------------------------------


class MockFile:
    def __init__(self, name="", size=0, url=""):
        self.name = name
        self.size = size
        self.url = url

    def __eq__(self, other):
        return (
            isinstance(other, MockFile)
            and self.name == other.name
            and self.size == other.size
            and self.url == other.url
        )


def get_items(mapping_or_list_of_two_tuples):
    # Tests accept either lists of two tuples, or dictionaries.
    if isinstance(mapping_or_list_of_two_tuples, dict):
        # {value: expected}
        return mapping_or_list_of_two_tuples.items()
    # [(value, expected), ...]
    return mapping_or_list_of_two_tuples


class FieldValues(TestCase):
    """Base class for testing valid and invalid input values."""

    valid_inputs: List[List[str, Any]] = []
    invalid_inputs: List[List[str, Any]] = []
    outputs: List[List[str, Any]] = []
    field: serializers.Field

    def test_valid_inputs(self) -> None:
        """Ensure that valid values return the expected validated data."""
        for input_value, expected_output in get_items(self.valid_inputs):
            self.assertEqual(
                self.field.run_validation(input_value),
                expected_output,
                f"input value: {repr(input_value)}",
            )

    def test_invalid_inputs(self) -> None:
        """Ensure that invalid values raise the expected validation error."""
        for input_value, expected_failure in get_items(self.invalid_inputs):
            with pytest.raises(serializers.ValidationError) as exc_info:
                self.field.run_validation(input_value)
            self.assertEqual(
                exc_info.value.detail,
                expected_failure,
                f"input value: {repr(input_value)}",
            )

    def test_outputs(self) -> None:
        """Ensure that outputs have expected values."""
        for output_value, expected_output in get_items(self.outputs):
            self.assertEqual(
                self.field.to_representation(output_value),
                expected_output,
                f"output value: {repr(output_value)}",
            )


# Tests for ConstrainedFileField field for correct input and output values.
# ----------------------------------------


class TestFileField(FieldValues):
    """Values for `ConstrainedFileField`."""

    valid_inputs = [
        (
            MockFile(name="expl.doc", size=1_048_576),
            MockFile(name="expl.doc", size=1_048_576),
        )
    ]
    invalid_inputs = [
        (
            MockFile(name="expl.doc", size=2_048_576),
            ["File size exceeds limit: 2.0M. Limit is 1.0M."],
        ),
    ]
    outputs = [
        (
            MockFile(name="example.doc", size=1_048_576, url="/example.doc"),
            "/example.doc",
        ),
        ("", None),
    ]
    field = ConstrainedFileField(max_length=10, max_upload_size=1_048_576)
