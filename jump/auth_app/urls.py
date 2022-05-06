from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from jump.auth_app.views import UserLoginView, ProfileDetailsView, UserRegisterView, ChangeUserPasswordView, \
    EditProfileView, DeleteProfileView, UserLogoutView, ProfilesListView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('fascia')), name='password_change_done'),

    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile'),
    path('profile/create/', UserRegisterView.as_view(), name='create profile'), # register
    path('profile/edit/', EditProfileView.as_view(), name='edit profile'),
    path('profile/list/', ProfilesListView.as_view(), name='list profiles'), # for tests

    path('profile/delete/', DeleteProfileView.as_view(), name='delete profile'),
)
