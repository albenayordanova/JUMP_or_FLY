from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from jump.auth_app.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '_XAP22PA5yCv.xh1',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'http://test.picture/url.png',
        'phone': '0888123456',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile(**self.VALID_PROFILE_DATA, user=user,)
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        first_name = 'Test1'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            phone=self.VALID_PROFILE_DATA['phone'],
            user=user,
        )
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        first_name = 'Te$st'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            phone=self.VALID_PROFILE_DATA['phone'],
            user=user,
        )
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        first_name = 'Tes t'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            phone=self.VALID_PROFILE_DATA['phone'],
            user=user,
        )
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        expected_full_name = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_full_name, profile.full_name)
