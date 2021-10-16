from django.urls import path

from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:poll_id>/', views.detail, name="detail"),
    path('<int:poll_id>/results/', views.results, name="results"),
    path('<int:poll_id>/<int:choice_id>/vote/', views.vote, name="vote"),
    path('accounts/login', views.Login.as_view(), name="login"),
    path('accounts/register', views.Register.as_view(), name="register"),
    path('profile', views.profile, name="profile"),
    path('accounts/logout', views.logout_view, name="logout"),
    path('create/', views.Create.as_view(), name="create"),
    path('add/choice/<int:poll_id>', views.AddChoice.as_view(), name="add_choice"),
    path('past', views.past, name="past"),
    path('polls/remove/<int:poll_id>', views.remove, name="remove"),
    path('polls/end/<int:poll_id>', views.end, name="end"),
    path('polls/search', views.search, name="search"),
]
