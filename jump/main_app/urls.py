from django.urls import path

from jump.main_app.views import HomeView, FasciaView, PhotoDetailsView, CreateEquipView, EditEquipView, DeleteEquipView, \
    CreatePhotoView, EditPhotoView, show_spot, create_spot, DeletePhotoView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('fascia/', FasciaView.as_view(), name='fascia'),

    path('spot/', show_spot, name='spot'),
    path('spot/create/', create_spot, name='create spot'),

    path('photo/details/<int:pk>/', PhotoDetailsView.as_view(), name='photo details'),
    path('photo/add/', CreatePhotoView.as_view(), name='create photo'),
    path('photo/edit/<int:pk>/', EditPhotoView.as_view(), name='edit photo'),
    path('photo/delete/<int:pk>/', DeletePhotoView.as_view(), name='delete photo'),

    path('equip/create/', CreateEquipView.as_view(), name='create equip'),
    path('equip/edit/<int:pk>/', EditEquipView.as_view(), name='edit equip'),
    path('equip/delete/<int:pk>/', DeleteEquipView.as_view(), name='delete equip'),
)
