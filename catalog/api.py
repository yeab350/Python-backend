from __future__ import annotations

from rest_framework import serializers, viewsets

from config.api_permissions import IsAdminOrReadOnly

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "slug"]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        qs = Product.objects.all()
        if self.request.user and self.request.user.is_staff:
            return qs
        return qs.filter(is_published=True)
