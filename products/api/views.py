from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .serializers import ProductListSerializer, ProductCreateSerializer
from products.models import Product
from django.db.models import FloatField, F
from django.db.models.functions import Coalesce
from .paginations import CustomPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter
from django_filters.rest_framework.backends import DjangoFilterBackend


# @api_view(["GET", "POST"])
# def index_view(request):
#     products = Product.objects.annotate(
#         discount=Coalesce('discount_price', 0, output_field=FloatField()),
#         total_price=F("price") - F("discount")
#     )
#     serializer = ProductListSerializer(products, many=True)
#
#     if request.method == "POST":
#         serializer = ProductListSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=request.user)
#         return Response(serializer.data)
#     return Response(serializer.data)
#
#
# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def product_detail_view(request, id):
#     products = Product.objects.annotate(
#         discount=Coalesce('discount_price', 0, output_field=FloatField()),
#         total_price=F("price") - F("discount")
#     )
#     product = products.get(id=id)
#     serializer = ProductListSerializer(product)
#
#     if request.method == "PUT" or request.method == "PATCH":
#         serializer = ProductListSerializer(data=request.data, instance=product)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#     if request.method == "DELETE":
#         product.delete()
#         return Response({"message": "Succesfully deleted!"})
#     return Response(serializer.data)
#
#
# @api_view(["POST"])
# def product_create_view(request):
#     serializer = ProductListSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save(user=request.user)
#     return Response(serializer.data)
#
#
#
# @api_view(["PATCH"])
# def product_update_view(request, id):
#     products = Product.objects.annotate(
#         discount=Coalesce('discount_price', 0, output_field=FloatField()),
#         total_price=F("price") - F("discount")
#     )
#     product = products.get(id=id)
#     serializer = ProductListSerializer(data=request.data, instance=product, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
#
# @api_view(["DELETE"])
# def product_delete_view(request, id):
#     products = Product.objects.annotate(
#         discount=Coalesce('discount_price', 0, output_field=FloatField()),
#         total_price=F("price") - F("discount")
#     )
#     product = products.get(id=id)
#     product.delete()
#     return Response({"message": "Succesfully deleted!"})



class ProductListView(generics.ListCreateAPIView):
    # serializer_class = ProductListSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter

    def get_queryset(self):
        # return Product.objects.filter(user=self.request.user)
        return Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductListSerializer



class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user)
    #     return Response(serializer.data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    lookup_field = "id"

    def get_object(self):
        # obj = Product.objects.get(id=int(self.kwargs.get("id")))
        obj = self.queryset.get(id=int(self.kwargs.get("id")))
        return obj




class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "id"


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "id"
    permission_classes = (
        IsAuthenticated, IsOwnerOrReadOnly
    )