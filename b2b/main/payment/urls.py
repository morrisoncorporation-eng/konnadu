from django.urls import path

from . import views

app_name = "payment"

urlpatterns = [
    path(
        "checkout/",
        views.CreateCheckoutSessionView.as_view(),
        name="checkout",
    ),
    path("success/", views.CheckoutSessionSuccessView.as_view(), name="success"),
    path(
        "purchase-subscription",
        views.PurchaseSubscriptionView.as_view(),
        name="purchase_subscription",
    ),
    path(
        "purchase-subscription-success/<id>",
        views.PurchaseSubscriptionSuccessView.as_view(),
        name="purchase_subscription_success",
    ),
    path("payment-intent", views.create_payment_intent, name="payment_intent"),
    path("payment-coinbase", views.coinbase_payment_intent, name="coinbase_intent"),

    path("payment-success/", views.success_view, name="payment-succeded"),
    path("payment-cancelled/", views.cancel_view, name="payment-failed")
]