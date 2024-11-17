from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, CustomLoginView, AddCardView, CardView, ConfirmDeleteCardView, TransactionView, \
    TransactionCreateView, FavoriteTransactionView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('add_card/', AddCardView.as_view(), name='add-card'),
    path('delete_card/<int:card_id>/', ConfirmDeleteCardView.as_view(), name='delete-card'),
    path('cards/', CardView.as_view(), name='cards'),
    path('add-payment/', TransactionCreateView.as_view(), name='add-payment'),
    path('add-payment/<int:id>/', TransactionCreateView.as_view(), name='add-payment-id'),
    path('', TransactionView.as_view(), name='payments-and-transfers'),
    path('favorite/', FavoriteTransactionView.as_view(), name='favorite-payments'),
]
