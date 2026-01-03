import stripe
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from apps.notifications.tasks import notify_payment_success

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #payment = serializer.save(user=request.user)

        #notify_payment_success.delay(
        #    payment.id,
        #    payment.borrowing.id,
        #    payment.money_to_pay
        #)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StripeSuccessView(APIView):
    def get(self, request):
        session_id = request.query_params.get("session_id")

        if not session_id:
            return Response(
                {"error": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payment.objects.filter(session_id=session_id).first()

        if not payment:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if session.payment_status == "paid":
            payment.status = "PAID"
            payment.save()

            return Response({"message": "Payment successful ✅"})

        return Response(
            {"message": "Payment not completed yet"},
            status=status.HTTP_400_BAD_REQUEST
        )

class StripeCancelView(APIView):
    def get(self, request):
        return Response({"message": "Payment cancelled ❌"})