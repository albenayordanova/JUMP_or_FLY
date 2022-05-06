from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from jump.auth_app.models import Profile
from jump.main_app.models import Equip, Photo

UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '_XAP22PA5yCv.xh1',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'http://test.picture/url.png',
        # 'date_of_birth': date(2000, 7, 23)
    }

    VALID_EQUIP_DATA = {
        'brand': 'The equip',
        'type': Equip.BOOM,
    }

    VALID_PHOTO_DATA = {
        'photo': 'zxc.jpg',
        'publication_date': date.today(),
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def __create_equip_and_photo_for_user(self, user):
        equip = Equip.objects.create(
            **self.VALID_EQUIP_DATA,
            user=user,
        )
        photo = Photo.objects.create(
            **self.VALID_PHOTO_DATA,
            user=user,
        )
        photo.tagged_equip.add(equip)
        photo.save()
        return (equip, photo)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile', kwargs={'pk': profile.pk, }))

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile', kwargs={'pk': 1, }))
        self.assertEqual(404, response.status_code)

    def test_expect_correct_template(self): ###
        user, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('profile_details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self): ###
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)
        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self): ###
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '123456asdf',
        }
        self.__create_user(**credentials)
        self.client.login(**credentials)
        response = self.__get_response_for_profile(profile)
        self.assertFalse(response.context['is_owner'])

    def test_when_user_has_equips__expect_to_return_only_users_equips(self):  ###yes
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'testuser2',
            'password': '123456asdf',
        }
        user2 = self.__create_user(**credentials)
        equip, photo = self.__create_equip_and_photo_for_user(user)
        self.__create_equip_and_photo_for_user(user2)
        response = self.__get_response_for_profile(profile)
        self.assertEqual(
            [equip],
            response.context['equips'],
        )

    def test_when_user_has_no_equips__equips_should_be_empty(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.__get_response_for_profile(profile)
        self.assertListEqual(
            [],
            response.context['equips'],
        )
