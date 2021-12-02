from django.core.mail import send_mail
from onemillionlandlord.settings import EMAIL_HOST_USER

def mail(email, username, password):
    message = f"""
    Account has been created
    Login details:
    Username: {username}
    Password: {password}
    Go to login: portal.onemillionlandlord.ng
    Reset password: portal.onemillionlandlord.ng/reset_password/
    Please keep this information safe.
    """
    send_mail(
        'Account Created',
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )