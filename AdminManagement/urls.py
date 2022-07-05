from django.urls import path
from .views import (
    ErrorErrorView,
    ErrorView,
    LugarErrorView,
    ParqueCreateView,
    ParqueListView,
    ParqueDetailView,
    ParqueUpdateView,
    ParqueDeleteView,
    ZonaErrorView,
    ZonaListView,
    ZonaDeleteView,
    ZonaCreateView,
    ZonaDetailView,
    ZonaUpdateView,
    LugarListView,
    LugarCreateView,
    LugarDetailView,
    LugarDeleteView,
    LugarUpdateView,
)

app_name = 'AdminManagement'
urlpatterns = [
    path('', ParqueListView.as_view(), name='parque-list'),
    path('<int:id>/', ParqueDetailView.as_view(), name='parque-detail'),
    path('create/', ParqueCreateView.as_view(), name='parque-create'),
    path('<int:id>/update/', ParqueUpdateView.as_view(), name='parque-update'),
    path('<int:id>/delete/', ParqueDeleteView.as_view(), name='parque-delete'),

    path('<int:id>/zona/', ZonaListView.as_view(), name='zona-list'),
    path('<int:id>/zona/<int:pk>/', ZonaDetailView.as_view(), name='zona-detail'),
    path('<int:id>/zona/<int:pk>/delete/', ZonaDeleteView.as_view(), name='zona-delete'),
    path('<int:id>/zona/create/', ZonaCreateView.as_view(), name='zona-create'),
    path('<int:id>/zona/<int:pk>/update/', ZonaUpdateView.as_view(), name='zona-update'),

    path('<int:id>/zona/<int:pk>/lugar/', LugarListView.as_view(), name='lugar-list'),
    path('<int:id>/zona/<int:pk>/lugar/<int:lugar>/', LugarDetailView.as_view(), name='lugar-detail'),
    path('<int:id>/zona/<int:pk>/lugar/<int:lugar>/delete/', LugarDeleteView.as_view(), name='lugar-delete'),
    path('<int:id>/zona/<int:pk>/lugar/create/', LugarCreateView.as_view(), name='lugar-create'),
    path('<int:id>/zona/<int:pk>/lugar/<int:lugar>/update/', LugarUpdateView.as_view(), name='lugar-update'),

    path('<int:id>/zona/create/erro/', ZonaErrorView.as_view()),
    path('<int:id>/zona/<int:pk>/lugar/create/erro/', LugarErrorView.as_view()),
    path('<int:id>/zona/create/erro/erro/', ErrorView.as_view()),
    path('<int:id>/zona/<int:pk>/update/erro/', ErrorErrorView.as_view()),
]