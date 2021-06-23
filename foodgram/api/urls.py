from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, FollowViewSet, IngredientViewSet,
                    PurchaseViewSet, RecipeViewSet)


router = DefaultRouter()
router.register('subscribe', FollowViewSet, basename='subscribe')
router.register('favorite', FavoriteViewSet, basename='favorite')
router.register('purchases', PurchaseViewSet, basename='purchase')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipe', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token, name='get_token'),
    path('v1/', include(router.urls))
]
