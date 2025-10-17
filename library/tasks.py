from datetime import timedelta
from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task(arks_late=True,time_limit=timedelta(hours=1),soft_time_limit=timedelta(minutes=30))
def check_overdue_loans():
    qs = Loan.objects.filter(
        Q(check_date__isnull=True)|~Q(check_date=timezone.now().date()),
        is_return = False,
        due_date__lt=timezone.now().date(),
    ).select_related("book","member","member__user")

    for loan in qs.iterator(100):
        loan:Loan
        book_title = loan.book.title
        member_email = loan.member.user.email


        send_mail(
            subject='Overdue Loaned',
            message=f'Hello {loan.member.user.username},\n\nYour loaned "{book_title}".\nis overdue.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
        loan.check_date = timezone.now().date()
        loan.save(update_fields=["check_date"])


