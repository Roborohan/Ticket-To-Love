from django.urls import path
from .views import home,search_movie, profile, RegisterView,about,contact

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('search-movie/', search_movie ,name='search-movie'),
    path('about/', about ,name='about'),
    path('contact/', contact ,name='contact'),
]
