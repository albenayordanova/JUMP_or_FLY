# from django import test as django_test
from unittest import TestCase

from django.core.exceptions import ValidationError

from jump.common.validators import ValidateFileMaxSizeInMb


class FakeFile:
    size = 5


class FakeImage:
    file = FakeFile()


class ValidateFileMaxSizeInMbTests(TestCase):
    def test_when_file_is_bigger__expect_to_raise(self):
        validator = ValidateFileMaxSizeInMb(0.000001)
        file = FakeImage()
        with self.assertRaises(ValidationError) as context:
            validator(file)
        self.assertIsNotNone(context.exception)

    def test_when_file_size_is_valid__expect_to_do_nothing(self):
        validator = ValidateFileMaxSizeInMb(1)
        file = FakeImage()
        validator(file)
