from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('go/', views.go, name='go'),

    path('invite/', views.invite, name='invite'),
    path('invite/email/', views.invite_email, name='invite_email'),
    path('invite/facebook/', views.invite_facebook, name='invite_facebook'),
    path('invite/facebook/save_invitee/', views.facebook_save_invitee, name='facebook_save_invitee'),

    path('~/', views.myfish, {'user_id': 'me'}, name='myfish'),
    path('~<int:user_id>/', views.myfish, name='userfish'),
    path('~/team/', views.myteam, {'user_id': 'me'}, name='myteam'),
    path('~<int:user_id>/team/', views.myteam, name='userteam'),
    path('team/<int:team_id>/', views.team_alone, name='team_alone'),
    path('fish/new/', views.myfish_new, name='myfish_new'),
    path('fish/<int:fish_id>/', views.fish_enlarge, name='fish_enlarge'),
    path('fish/delete/', views.myfish_delete, name='myfish_delete'),

    path('ajax/newcomment/', views.ajax_new_comment, name='ajax_new_comment'),
    path('ajax/report/', views.ajax_report, name='ajax_report'),

    path('leaderboard/', views.leaderboard, name='leaderboard'),

    path('get_admin_access_token/', views.get_admin_access_token, name='get_admin_access_token'),
    path('get_admin_access_token_complete/', views.get_admin_access_token_complete, name='get_admin_access_token_complete'),
]
