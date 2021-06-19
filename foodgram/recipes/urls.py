from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.recipe_new, name='new_recipe'),
    path('follows/', views.follows, name='follows'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchase/', views.purchase, name='purchase'),
    path('purchase/download/', views.purchase_download, name='download_purchase'),
    path('purchase/<int:recipe_id>/delete/', views.purchase_delete, name='purchase_recipe_delete'),
    path('<str:username>/', views.profile_view, name='profile_view'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('<str:username>/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('<str:username>/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
]
