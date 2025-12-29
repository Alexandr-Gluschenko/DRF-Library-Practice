from datetime import date

from celery import shared_task
from .telegram import send_message
from apps.borrowing.models import Borrowing


@shared_task
def notify_new_borrowing(borrowing_id, user_name, book_title):
    text = f"📚 New borrowing created:\nUser: {user_name}\nBook: {book_title}\nID: {borrowing_id}"
    send_message(text)


@shared_task
def notify_borrowing_overdue(borrowing_id, user_name, book_title):
    text = f"⏰ Borrowing overdue:\nUser: {user_name}\nBook: {book_title}\nID: {borrowing_id}"
    send_message(text)


@shared_task
def notify_payment_success(payment_id, borrowing_id, amount):
    text = f"💰 Payment successful:\nPayment ID: {payment_id}\nBorrowing ID: {borrowing_id}\nAmount: ${amount}"
    send_message(text)


@shared_task
def check_overdue_borrowings():
    overdue = Borrowing.objects.filter(
        expected_return_date__lt=date.today(),
        actual_return_date__isnull=True,
    )
    for b in overdue:
        notify_borrowing_overdue.delay(b.id, b.user.get_full_name(), b.book.title)
