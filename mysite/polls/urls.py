from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("admin-view/", views.admin_view, name="admin_view"),
    path("login/", views.login, name="login"),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]