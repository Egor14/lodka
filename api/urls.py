from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_categories),
    path('<int:id>/', views.get_category),
    path('delete/', views.delete_everything)
]
