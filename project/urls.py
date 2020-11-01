"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


# def trigger_error(request):
#     1 / 0


urlpatterns = i18n_patterns(
    path(_("admin/"), admin.site.urls),
    path(_("cart/"), include("dshop.cart.urls", namespace="cart")),
    path(_("orders/"), include("dshop.orders.urls", namespace="orders")),
    path(_("payment/"), include("dshop.payment.urls", namespace="payment")),
    path(_("coupons/"), include("dshop.coupons.urls", namespace="coupons")),
    path("rosetta/", include("rosetta.urls")),
    # path("sentry-debug/", trigger_error),
    path("", include("dshop.shop.urls", namespace="shop")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
