from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.core import mail
from django.conf import settings


class MailerService(object):

    def __init__(self, request):
        self.request = request

    def send_ask_confirmation_email(self, confirmation_token, email, username):
        confirmation_url = "{}?token={}".format(self.request.build_absolute_uri(reverse('email-confirmation')),
                                                confirmation_token)

        context_params = {'username': username, 'confirmation_url': confirmation_url}
        plain_text_message = get_template('ask_confirmation_email.txt').render(context_params)
        html_message = get_template('ask_confirmation_email.html').render(context_params)

        subject, origin_email, target_email = 'Abidria account confirmation', settings.EMAIL_HOST_USER, email

        mail.send_mail(subject,
                       plain_text_message,
                       origin_email, [target_email, ],
                       html_message=html_message,
                       fail_silently=False)
