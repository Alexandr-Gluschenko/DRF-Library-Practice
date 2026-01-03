from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from apps.borrowing.models import Borrowing
from apps.borrowing.serializers import BorrowingSerializer
from apps.notifications.tasks import notify_new_borrowing


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']

        if book.inventory < 1:
            raise ValidationError("Book is out of stock")

        book.inventory -= 1
        book.save()

        borrowing = serializer.save(user=request.user)

        notify_new_borrowing.delay(
            borrowing.id,
            request.user.get_full_name(),
            borrowing.book.title,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_queryset(self):
        queryset = super().get_queryset()

        user_id = self.request.query_params.get('user_id')
        is_active = self.request.query_params.get('is_active')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_active is not None:
            queryset = queryset.filter(
                actual_return_date__isnull=is_active.lower() == "true"
            )

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    @action(methods=["post"], detail=True, url_path="return")
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Book already returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = timezone.now()

        book = borrowing.book
        book.inventory += 1
        book.save()

        borrowing.save()

        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)
