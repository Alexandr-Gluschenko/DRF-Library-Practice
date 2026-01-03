from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.books.views import BooksViewSet
from apps.borrowing.views import BorrowingViewSet
from apps.payments.views import PaymentViewSet

router = DefaultRouter()
router.register('books', BooksViewSet)
router.register('borrowings', BorrowingViewSet)
router.register('payments', PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('users/', include('apps.users.urls')),
    path('payments/', include('apps.payments.urls')),
]
