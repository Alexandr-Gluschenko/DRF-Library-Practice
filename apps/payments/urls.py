from django.urls import path
from .views import StripeSuccessView, StripeCancelView

urlpatterns = [
    path('success/', StripeSuccessView.as_view(), name='success'),
    path('cancel/', StripeCancelView.as_view(), name='cancel'),
]