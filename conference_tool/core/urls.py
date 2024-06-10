from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('create/', views.create_conference, name='create_conference'),
    path('conference/<uuid:conference_id>/', views.submit_question, name='submit_question'),
    path('conference/<uuid:conference_id>/dashboard/', views.conference_dashboard, name='conference_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
]
