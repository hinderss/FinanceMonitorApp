from django import forms
from django.core.exceptions import ValidationError

from .models import User, Card, Transaction
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    full_name = forms.Field(label="ФИО")
    passport_number = forms.Field(label="Серия и номер паспорта")
    id_number = forms.Field(label="Идентификационный номер")
    phone_number = forms.Field(label="Номер телефона")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'passport_number', 'id_number', 'phone_number', 'password1', 'password2']


class LoginForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)


class CardForm(forms.ModelForm):
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m'],
        label="Срок действия",
    )
    card_number = forms.CharField(
        max_length=19,
        widget=forms.widgets.Input(attrs={'oninput': 'formatCardNumber(this)'}),
        label="Номер карты"
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.widgets.Input(attrs={'placeholder': 'CVV', 'type': 'password', 'autocomplete': "off", 'autocorrect': "off"}),
        label="cvv"
    )

    class Meta:
        model = Card
        fields = ['card_number', 'cvv', 'expiration_date']

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if len(card_number) != 16:
            raise ValidationError("Введите корректный нномер карты")
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if len(cvv) != 3:
            raise ValidationError("Введите корректный cvv")
        return cvv

    def save(self, commit=True):
        card_number = self.cleaned_data.get('card_number')
        cvv = self.cleaned_data.get('cvv')

        card_instance = super().save(commit=False)

        card_instance.set_card_number(card_number)
        card_instance.set_cvv(cvv)

        if commit:
            card_instance.save()

        return card_instance


class ConfirmDeletionForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class TransactionForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Сумма")
    is_favorite = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = Transaction
        fields = ["card", "unique_code", "amount", "description", "is_favorite"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['card'].queryset = Card.objects.filter(user=user)
