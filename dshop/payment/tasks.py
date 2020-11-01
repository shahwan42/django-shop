from io import BytesIO

import weasyprint
from celery import task

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from dshop.orders.models import Order


@task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f"My Shop - EE Invoice no. {order.id}"
    message = "Please, find attached the invoice for your recent purchase."
    email = EmailMessage(subject, message, "admin@django-shop.com", [order.email])

    # generate PDF
    html = render_to_string("orders/order/pdf.html", {"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach PDF file
    email.attach(f"order_{order.id}.pdf", out.getvalue(), "application/pdf")

    # send e-mail
    email.send()
