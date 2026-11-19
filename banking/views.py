
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from .models import Account, Transaction, BillPayment, Complaint
from django.db.models import Q

def home(request):
    return render(request, 'banking/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(
                request,
                'banking/login.html',
                {'error': 'Invalid username or password'}
            )

    return render(request, 'banking/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                return render(request, 'banking/register.html',
                              {'error': 'Username already exists'})

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            login(request, user)
            return redirect('dashboard')

        else:
            return render(request, 'banking/register.html',
                          {'error': 'Passwords do not match'})

    return render(request, 'banking/register.html')

@login_required(login_url='login')
def dashboard(request):

    account = Account.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        'banking/dashboard.html',
        {'account': account}
    )

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def money_transfer(request):

    sender = get_object_or_404(
        Account,
        user=request.user
    )

    if request.method == 'POST':

        receiver_number = request.POST.get('receiver_account')
        amount_input = request.POST.get('amount')

        try:
            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                raise ValueError

        except (InvalidOperation, TypeError, ValueError):
            return render(request, 'banking/transfer.html', {
                'error': 'Please enter a valid positive amount.',
                'sender': sender
            })

        if amount.as_tuple().exponent < -2:
            return render(request, 'banking/transfer.html', {
                'error': 'Amount can have a maximum of two decimal places.',
                'sender': sender
            })

        if amount > Decimal('9999999999.99'):
            return render(request, 'banking/transfer.html', {
                'error': 'Amount exceeds the permitted limit.',
                'sender': sender
            })

        try:
            with transaction.atomic():

                sender = Account.objects.select_for_update().get(
                    pk=sender.pk
                )

                receiver = Account.objects.select_for_update().get(
                    account_number=receiver_number
                )

                if sender.pk == receiver.pk:
                    raise ValueError('You cannot transfer money to yourself.')

                if sender.balance < amount:
                    raise ValueError('Insufficient balance.')

                sender.balance -= amount
                receiver.balance += amount

                sender.save()
                receiver.save()

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    status='SUCCESS'
                )

            return render(request, 'banking/transfer.html', {
                'success': 'Money transferred successfully!',
                'sender': sender
            })

        except Account.DoesNotExist:
            error = 'Beneficiary account not found.'

        except ValueError as e:
            error = str(e)

        return render(request, 'banking/transfer.html', {
            'error': error,
            'sender': sender
        })

    return render(request, 'banking/transfer.html', {
        'sender': sender
    })

@login_required(login_url='login')
def account_statement(request):
    account = get_object_or_404(Account, user=request.user)

    transactions = Transaction.objects.filter(
        Q(sender=account) | Q(receiver=account)
    ).order_by('-transaction_date')

    return render(request, 'banking/statement.html', {
        'account': account,
        'transactions': transactions
    })

@login_required(login_url='login')
def pay_bills(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':

        bill_type = request.POST.get('bill_type')
        consumer_number = request.POST.get('consumer_number', '').strip()
        amount_input = request.POST.get('amount')

        valid_types = ['ELECTRICITY', 'WATER', 'INTERNET']

        if bill_type not in valid_types or not consumer_number:
            return render(request, 'banking/pay_bills.html', {
                'account': account,
                'error': 'Please enter valid bill details.'
            })

        try:
            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                raise ValueError

            if amount.as_tuple().exponent < -2:
                raise ValueError

        except (InvalidOperation, TypeError, ValueError):
            return render(request, 'banking/pay_bills.html', {
                'account': account,
                'error': 'Please enter a valid amount with up to two decimal places.'
            })

        try:
            with transaction.atomic():

                account = Account.objects.select_for_update().get(
                    pk=account.pk
                )

                if account.balance < amount:
                    raise ValueError('Insufficient account balance.')

                account.balance -= amount
                account.save()

                BillPayment.objects.create(
                    account=account,
                    bill_type=bill_type,
                    consumer_number=consumer_number,
                    amount=amount,
                    status='SUCCESS'
                )

            return render(request, 'banking/pay_bills.html', {
                'account': account,
                'success': 'Bill payment successful!'
            })

        except ValueError as e:
            return render(request, 'banking/pay_bills.html', {
                'account': account,
                'error': str(e)
            })

    return render(request, 'banking/pay_bills.html', {
        'account': account
    })

@login_required(login_url='login')
def bill_history(request):
    account = get_object_or_404(Account, user=request.user)

    payments = BillPayment.objects.filter(
        account=account
    ).order_by('-payment_date')

    return render(request, 'banking/bill_history.html', {
        'account': account,
        'payments': payments
    })


@login_required(login_url='login')
def raise_complaint(request):

    if request.method == 'POST':

        complaint_type = request.POST.get('complaint_type')
        description = request.POST.get('description', '').strip()

        valid_types = ['TRANSACTION', 'ACCOUNT', 'PAYMENT', 'OTHER']

        if complaint_type not in valid_types or not description:
            return render(request, 'banking/complaint.html', {
                'error': 'Please provide valid complaint details.'
            })

        Complaint.objects.create(
            user=request.user,
            complaint_type=complaint_type,
            description=description
        )

        return render(request, 'banking/complaint.html', {
            'success': 'Your complaint has been submitted successfully!'
        })

    return render(request, 'banking/complaint.html')

@login_required(login_url='login')
def complaint_history(request):

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'banking/complaint_history.html', {
        'complaints': complaints
    })

@login_required(login_url='login')
def profile(request):

    account = Account.objects.filter(
        user=request.user
    ).first()

    return render(request, 'banking/profile.html', {
        'user': request.user,
        'account': account
    })