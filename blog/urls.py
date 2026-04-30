from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]