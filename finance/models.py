from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from cryptography.fernet import Fernet


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=20, unique=True)
    id_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()


key = settings.FERNET_KEY
cipher = Fernet(key)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    _card_number = models.CharField(max_length=255)
    _cvv = models.CharField(max_length=255)
    expiration_date = models.DateField()

    def set_card_number(self, card_number):
        self._card_number = cipher.encrypt(card_number.encode()).decode()

    def get_card_number(self):
        return cipher.decrypt(self._card_number.encode()).decode()

    def set_cvv(self, cvv):
        self._cvv = cipher.encrypt(cvv.encode()).decode()

    def get_cvv(self):
        return cipher.decrypt(self._cvv.encode()).decode()

    @property
    def card_number_last4(self):
        return self.get_card_number()[-4:]

    @property
    def cvv_last4(self):
        return self.get_cvv()

    def __str__(self):
        return f"** {self.card_number_last4}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions', verbose_name="Карта")
    unique_code = models.IntegerField(verbose_name="Уникальный код услуги")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    description = models.CharField(max_length=255, verbose_name="Название платежа")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата операции")
    is_favorite = models.BooleanField(default=False, verbose_name="Избранный платёж")

    class Meta:
        ordering = ("-timestamp",)
