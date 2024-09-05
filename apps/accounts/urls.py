from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/extra_profile/', views.extra_profile, name='extra_profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('fbuser/', views.fbuser, name='fbuser'),

    path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password/reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email_html-inline.html'
    ), name="password_reset"),
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
