import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Transaction


DATE_FORMAT = 'd.m.Y H:i'


class BadgeColumn(tables.Column):
    def render(self, value):
        return format_html('<h5><span class="badge bg-secondary">{}</span></h5>', value)


class FavoriteColumn(tables.BooleanColumn):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            attrs={
                # "th": {"style": "max-width: 100%;"},
                # "td": {"style": "text-align: center;"}
            },
            **kwargs,
        )

    def render(self, value, record, bound_column):
        print(value)
        if value:
            return mark_safe("<span>⭐</span>")
        return mark_safe("""<span style="filter: grayscale(100%);">⭐</span>""")


class PaymentTable(tables.Table):
    timestamp = tables.DateTimeColumn(
        format=DATE_FORMAT,
        # attrs={"td": {"style": f"max-width: 1rem;"}},
        verbose_name="Дата операции",
    )
    description = tables.LinkColumn(
        'add-payment-id',
        args=[tables.A('id')],
        verbose_name="Название платежа",
    )
    amount = tables.Column(verbose_name="Сумма")
    card = BadgeColumn(verbose_name="Карта",)
    is_favorite = FavoriteColumn(verbose_name="Избранный платёж")

    class Meta:
        model = Transaction
        orderable = False
        fields = ('timestamp', 'description', 'amount', 'card', 'is_favorite')
        attrs = {"class": "table custom-bordered"}
