from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

"""
This is a utility app for sending messages to different users depending on the actions
"""


def cart_update_user(from_email, to_email, item, action):
    message = ""
    CANCELLED = "cancel"
    PENDING = "pending"
    APPROVE = "approve"
    DISABLE = "disable"
    if action == CANCELLED:
        message = f"We are sorry but {item.reason}"
    elif action == PENDING:
        message = f"Hello, your item {item.title} is currently undergoing review"
    elif action == APPROVE:
        message = f"Congratulations! your items has been approved! login to checkout."
    elif action == DISABLE:
        message = f"Sorry, your item {item.title} has been disabled for {item.reason}"

    subject = "Update!"

    html_content = f"<p>{item.reason}</p>"
    from_email = from_email
    to_email = [to_email]
    try:
        msg = EmailMultiAlternatives(subject, message, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return f"email for {action} has been sent."
        print(msg)
    except Exception as e:
        print(e)


def new_cart_item_email(from_email, to_emails, item_ids):
    url = "localhost:8000/dashboard/orders/"
    subject = "New arrivals!"
    message = f"Hello admin, new items {item_ids} has been added to cart \n be sure to login and check them out. \n {url}"
    send_mail(subject, message, from_email, to_emails, fail_silently=False)
    return f"email sent to {to_emails}"
