from django.urls import path
from . import views

urlpatterns = [
    path('', views.ScoreListView.as_view(), name='score-list'),
    path('<int:pk>/', views.ScoreDetailView.as_view(), name='score-detail'),
]
