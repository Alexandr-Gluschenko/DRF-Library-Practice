from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
