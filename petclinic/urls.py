from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from petclinic import views

urlpatterns = [
    path('owners/', views.OwnerList.as_view(), name='owner-list'),
    path('owners/<int:pk>', views.OwnerDetail.as_view(), name='owner-detail'),
    path('vets/', views.VetList.as_view(), name='vet-list'),
    path('vets/<int:pk>', views.VetDetail.as_view(), name='vet-detail'),
    path('specialties/', views.SpecialtyList.as_view(), name='specialty-list'),
    path('specialties/<int:pk>', views.SpecialtyDetail.as_view(), name='specialty-detail'),
    path('pet_types/', views.PetTypeList.as_view(), name='pet-type-list'),
    path('pet_types/<int:pk>', views.PetTypeDetail.as_view(), name='pet-type-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
