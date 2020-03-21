from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from petclinic import views

urlpatterns = [
    path('owners/', views.OwnerList.as_view(), name='owner-list'),
    path('owners/<int:pk>', views.OwnerDetail.as_view(), name='owner-detail'),
    path('vets/', views.VetList.as_view(), name='vet-list'),
    path('vets/<int:pk>', views.VetDetail.as_view(), name='vet-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
