from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from jump.auth_app.models import Profile

UserModel = get_user_model()


class ProfileCreateViewTests(TestCase):
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

    def test_create_profile__when_all_valid__expect_to_create(self): ###
           # user_data = {
        #     'username': 'testuser',
        #     'password': '_XAP22PA5yCv.xh1',
        # }
        # UserModel.objects.create_user(**user_data)
        self.client.post(
            reverse('create profile'),
            data=self.VALID_PROFILE_DATA,
        )
        profile = Profile.objects.first()
        self.assertIsNotNone(profile)
        self.assertEqual(self.VALID_PROFILE_DATA['first_name'], profile.first_name)
        self.assertEqual(self.VALID_PROFILE_DATA['last_name'], profile.last_name)
        self.assertEqual(self.VALID_PROFILE_DATA['picture'], profile.picture)
        self.assertEqual(self.VALID_PROFILE_DATA['phone'], profile.phone)

    def test_create_profile__when_all_valid__expect_to_redirect_to_fascia(self): ###
        response = self.client.post(
            reverse('create profile'),
            data=self.VALID_PROFILE_DATA,
        )
        # profile = Profile.objects.first()
        expected_url = reverse('fascia') # , kwargs={'pk': profile.pk}
        self.assertRedirects(response, expected_url)
