from django.urls import path

from .views import PayoutViewSet

payout_list = PayoutViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
payout_detail = PayoutViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('payouts/', payout_list, name='payout-list'),
    path('payouts/<uuid:pk>/', payout_detail, name='payout-detail'),
]
