from django.urls import path
from apps.books.views import BooksViewSet

urlpatterns = [
    path('users/books/', BooksViewSet.as_view({"get": "list", "post": "create"}), name="books-list-create"),
    path('users/books/<int:pk>/', BooksViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    }), name="books-detail"),
]
