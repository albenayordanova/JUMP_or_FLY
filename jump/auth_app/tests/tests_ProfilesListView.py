from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from jump.auth_app.models import Profile
from jump.auth_app.views import ProfilesListView

UserModel = get_user_model()


class ProfilesListViewTests(TestCase):
    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('list profiles'))
        self.assertTemplateUsed(response, 'profiles_list.html')

    def test_get__when_two_profiles__expect_context_to_contain_two_profiles(self):
        # Arrange
        user1 = self.__create_user(username='testuser', password='_XAP22PA5yCv.xh1',)
        user2 = self.__create_user(username='testauserova', password='_XAP22PA5yCv.xh1777', )
        profiles_to_create = (
            Profile(first_name='Test', last_name='User', picture='http://test.picture/url.png', phone='0888123456', user=user1,),
            Profile(first_name='Testa', last_name='Userova', picture='http://testa.picture/url.png', phone='0888123457', user=user2,),
        )
        Profile.objects.bulk_create(profiles_to_create)

        # Act
        response = self.client.get(reverse('list profiles'))

        # Assert
        profiles = response.context['object_list']

        self.assertEqual(len(profiles), 2)

    def test_get__when_not_logged_in_user__expect_user_to_be_No_user(self):
        response = self.client.get(reverse('list profiles'))
        self.assertEqual(
            ProfilesListView.no_logged_in_user_value,
            response.context[ProfilesListView.context_user_key],
        )

    def test_get__when_logged_in_user__expect_user_to_be_username(self):
        user_data = {
            'username': 'testuser',
            'password': '_XAP22PA5yCv.xh1',
        }
        UserModel.objects.create_user(**user_data)
        self.client.login(**user_data)
        response = self.client.get(reverse('list profiles'))
        self.assertEqual(
            user_data['username'],
            response.context[ProfilesListView.context_user_key],
        )
