from django.urls import path, re_path
from user import views
from django.views.generic import TemplateView

urlpatterns = [
    # マイページ
    path('profile', views.ProfileView.as_view(), name='profile'),
    # マイページ編集
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]