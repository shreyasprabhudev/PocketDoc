from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('recommendation/', views.recommendation_view, name='recommendation'),  
    # path('recommendation/results/', views.recommendation_results, name='recommendation_results'),  # Optional: if results are handled separately
]
