from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect

from jump.common.view_mixins import RedirectToFascia
from jump.main_app.forms import CreateEquipForm, EditEquipForm, \
    DeleteEquipForm, SpotForm
from jump.main_app.models import Photo, Equip, Spot


class HomeView(RedirectToFascia, views.TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class FasciaView(views.ListView):
    model = Photo
    template_name = 'fascia.html'
    context_object_name = 'equip_photos'
    paginate_by = 3


class CreateEquipView(views.CreateView):
    template_name = 'equip_create.html'
    form_class = CreateEquipForm
    success_url = reverse_lazy('fascia')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditEquipView(views.UpdateView):
    template_name = 'equip_edit.html'
    form_class = EditEquipForm
    success_url = reverse_lazy('fascia')

    def get_queryset(self):
        return Equip.objects.filter(user=self.request.user)


class DeleteEquipView(views.DeleteView):
    template_name = 'equip_delete.html'
    form_class = DeleteEquipForm
    success_url = reverse_lazy('fascia')

    def get_queryset(self):
        return Equip.objects.filter(user=self.request.user)


class PhotoDetailsView(LoginRequiredMixin, views.DetailView):
    model = Photo
    template_name = 'photo_details.html'
    context_object_name = 'equip_photo'

    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
    #     viewed_photos = request.session.get('last_viewed_photo_ids', [])
    #     viewed_photos.insert(0, self.kwargs['pk'])
    #     request.session['last_viewed_photo_ids'] = viewed_photos[:5]
    #     return response

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tagged_equip')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class CreatePhotoView(LoginRequiredMixin, views.CreateView):
    model = Photo
    template_name = 'photo_create.html'
    fields = ('photo', 'description', 'tagged_equip')

    success_url = reverse_lazy('fascia')

    def get_queryset(self):
    #     .filter(user=self.request.user)
    #     return super().get_queryset().filter(user=self.request.user).prefetch_related('tagged_equip')
        return Equip.objects.prefetch_related('tagged_equip').filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPhotoView(LoginRequiredMixin, views.UpdateView):
    model = Photo
    template_name = 'photo_edit.html'
    fields = ('description', 'tagged_equip')

    def get_success_url(self):
        return reverse_lazy('photo details', kwargs={'pk': self.object.id})


class DeletePhotoView(views.DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('fascia')

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)


# class SpotView(views.ListView):
#     form_class = SpotForm
#     template_name = 'spot.html'
#     paginate_by = 3
#
#     def get_queryset(self):
#         return Spot.objects.all() ###

def show_spot(request):
    spots = Spot.objects.all()
    paginator = Paginator(spots, per_page=2)
    current_page = request.GET.get('page', 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'spots': spots,
        'form': SpotForm(),
        'spots_page': paginator.get_page(current_page),
        'page_obj': page_obj,
    }

    return render(request, 'spot.html', context)


def create_spot(request):
    form = SpotForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('spot')


class SpotDetailsView(views.DetailView):
    model = Spot
    template_name = 'spot_details.html'

