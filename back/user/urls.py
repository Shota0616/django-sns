from django.urls import path, re_path
from user import views
from django.views.generic import TemplateView

urlpatterns = [
    # マイページ
    path('profile', views.ProfileView.as_view(), name='profile'),
    # マイページ編集
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    # allauthの上書き
    # ログイン・ログアウト
    # path('login/', TemplateView.as_view(template_name = 'account/login.html'), name='account_login'),
    # path('logout/', TemplateView.as_view(template_name = 'account/logout.html'), name='account_logout'),
    # # 新規登録
    # path('signup/', TemplateView.as_view(template_name = 'account/signup.html'), name='account_signup'),
    # # 確認メール送信完了メール
    # path("confirm-email/", views.ConfirmEmailView.as_view(), name="account_email_verification_sent"),
    # # メール確認ページ
    # re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.ConfirmEmailView.as_view(), name="account_confirm_email"),
    # #path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    # # パスワードリセット（メールアドレス入力）
    # path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # # パスワードリセットメール送信完了ページ
    # path('password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # # パスワード再設定ページ
    # re_path( r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.PasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    # # パスワード再設定完了ページ
    # path("password/reset/key/done/", views.PasswordResetFromKeyDoneView.as_view(), name="account_reset_password_from_key_done"),
]