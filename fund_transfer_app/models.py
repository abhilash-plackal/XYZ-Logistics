from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Node(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, unique=True, null=False)
    parent = models.ForeignKey('self', null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    TRANSACTION_TYPE = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    actor = models.ForeignKey(User, null=False)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
