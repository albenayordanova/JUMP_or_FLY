import slug as slug
from django.contrib.auth import login
from django.views import generic as views
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import reverse_lazy, reverse

from jump.auth_app.forms import CreateProfileForm
from jump.auth_app.models import Profile
from jump.common.view_mixins import RedirectToFascia
from jump.main_app.models import Equip, Photo


class UserRegisterView(RedirectToFascia, views.CreateView): # test -> 2 custom behaviour
    form_class = CreateProfileForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('fascia')

    # def get_success_url(self): # for test
    #     return reverse('profile', kwargs={'pk': self.object.pk})

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(LoginView):
    template_name = 'login_page.html'
    success_url = reverse_lazy('fascia')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class EditProfileView(views.UpdateView):
    model = Profile
    # form_class = EditProfileForm
    template_name = 'profile_edit.html'
    # success_url = reverse_lazy('profile') #
    fields = ('first_name', 'last_name', 'picture', 'phone', 'email')
    # slug_field = 'username'
    # slug_url_kwarg = 'slug'

    # def get_queryset(self):
    #     return Profile.objects.filter(user=self.request.user)


class DeleteProfileView(views.UpdateView):
    model = Profile
    template_name = 'profile_delete.html'
    success_url = reverse_lazy('home')


class ChangeUserPasswordView(PasswordChangeView):
    template_name = 'change_password.html'


class ProfilesListView(views.ListView): # for tests
    model = Profile
    template_name = 'profiles_list.html'
    context_user_key = 'user'
    no_logged_in_user_value = 'No user'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context[self.context_user_key] = self.request.user.username
        else:
            context[self.context_user_key] = self.no_logged_in_user_value
        return context


class ProfileDetailsView(views.DetailView): # tests mandatory
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equips = list(Equip.objects.filter(user_id=self.object.user_id))
        photos = Photo.objects.filter(tagged_equip__in=equips).distinct()

        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
            'equips': equips,
        })
        return context


class UserLogoutView(LogoutView):
    template_name = 'home_page.html'
    success_url = reverse_lazy('home')
