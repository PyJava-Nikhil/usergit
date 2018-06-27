from django.urls import path
from accounts import views

urlpatterns = [
    path('search_user/', views.SearchUser.as_view(), name="search_github_user"),
]