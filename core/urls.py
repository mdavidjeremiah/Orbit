from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('portfolio-details/', views.portfolio_details, name='portfolio_details'),
    path('service-details/', views.service_details, name='service_details'),
    path('privacy/',              views.privacy,           name='privacy'),
    path('terms/',                views.terms,             name='terms'),
    path('404/',                  views.page_404,          name='404'),
    # Form endpoints
    path('forms/contact/',      views.contact,           name='contact'),
    path('forms/newsletter/',   views.newsletter,        name='newsletter'),
]
