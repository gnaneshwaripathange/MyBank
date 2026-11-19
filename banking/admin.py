from django.contrib import admin
from .models import Account,Transaction,BillPayment,Complaint

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(BillPayment)
admin.site.register(Complaint)