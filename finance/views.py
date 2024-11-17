from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django_tables2 import SingleTableView

from .forms import RegistrationForm, CardForm, ConfirmDeletionForm, TransactionForm
from .models import Card, User, Transaction
from .tables import PaymentTable


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('payments-and-transfers')


class CardView(LoginRequiredMixin, TemplateView):
    template_name = 'cards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cards = user.cards.all()

        context['cards'] = cards

        return context


class AddCardView(LoginRequiredMixin, CreateView):
    model = Card
    form_class = CardForm
    template_name = 'add_card.html'
    success_url = reverse_lazy('cards')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ConfirmDeleteCardView(LoginRequiredMixin, FormView):
    template_name = 'delete_card.html'
    form_class = ConfirmDeletionForm

    def get_object(self):
        card_id = self.kwargs.get('card_id')
        return get_object_or_404(Card, id=card_id)

    def form_valid(self, form):
        password = form.cleaned_data['password']

        user = authenticate(request=self.request, username=self.request.user.phone_number, password=password)

        if user is not None and user.is_authenticated:
            card = self.get_object()
            card.delete()
            return redirect('cards')

        form.add_error('password', 'Неверный пароль. Попробуйте снова.')
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('cards')


class TransactionView(LoginRequiredMixin, SingleTableView):
    model = Transaction
    table_class = PaymentTable
    template_name = 'index.html'

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Transaction.objects.filter(user=user.id)


class FavoriteTransactionView(TransactionView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_favorite=True)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'add_payment.html'
    success_url = reverse_lazy('payments-and-transfers')

    def get_initial(self):
        transaction: Transaction | None = None
        if 'id' in self.kwargs:
            transaction = get_object_or_404(Transaction, id=self.kwargs['id'])

        initial = {}
        if transaction:
            initial = {
                'description': transaction.description,
                'amount': transaction.amount,
                'card': transaction.card,
                'is_favorite': transaction.is_favorite,
            }
        return initial

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.save()
        return super().form_valid(form)
