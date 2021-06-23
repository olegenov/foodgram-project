from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from recipes.models import Favorite, Follow, Ingredient, Purchase, Recipe
from .permissions import FollowPermission
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer,
                          RecipeSerializer)


User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [FollowPermission]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, pk):
        follow = get_object_or_404(Follow, author__pk=pk, user=self.request.user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, pk):
        favorite = get_object_or_404(Favorite, recipe__pk=pk, user=self.request.user)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, pk):
        purchase = get_object_or_404(
            Purchase,
            recipe__pk=pk,
            user=self.request.user
        )
        purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.filter(
            name__icontains=self.request.GET.get('query')
        )
        return queryset
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        names = [
            {
                'title': od['name'],
                'dimension': od['units']
            } for od in serializer.data
        ]

        return Response(names)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
