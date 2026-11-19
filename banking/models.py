from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings Account'),
        ('CURRENT', 'Current Account'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    account_number = models.CharField(
        max_length=16,
        unique=True
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='SAVINGS'
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_number


class Transaction(models.Model):

    sender = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='sent_transactions'
    )

    receiver = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='received_transactions'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        default='SUCCESS'
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver} : {self.amount}"

class BillPayment(models.Model):

    BILL_TYPES = [
        ('ELECTRICITY', 'Electricity'),
        ('WATER', 'Water'),
        ('INTERNET', 'Internet'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    bill_type = models.CharField(
        max_length=20,
        choices=BILL_TYPES
    )

    consumer_number = models.CharField(max_length=50)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, default='SUCCESS')

    def __str__(self):
        return f"{self.bill_type} - {self.consumer_number}"

    
class Complaint(models.Model):

    COMPLAINT_TYPES = [
        ('TRANSACTION', 'Transaction Issue'),
        ('ACCOUNT', 'Account Issue'),
        ('PAYMENT', 'Bill Payment Issue'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    complaint_type = models.CharField(
        max_length=20,
        choices=COMPLAINT_TYPES
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.complaint_type}"
