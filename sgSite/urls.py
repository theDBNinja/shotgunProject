from django.urls import path

from . import views

app_name = "sgSite"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('project/<int:project_id>/', views.ProjectView.as_view(), name='project')
]
