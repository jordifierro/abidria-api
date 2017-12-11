from mock import Mock

from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.template.loader import get_template

from people.services import MailerService


class TestMailerService(TestCase):

    def test_send_ask_confirmation_mail(self):
        TestMailerService._ScenarioMaker() \
                .given_a_confirmation_token() \
                .given_a_username() \
                .given_an_email() \
                .given_a_request_that_builds_absolute_uri() \
                .when_send_ask_confirmation_mail_is_called() \
                .then_django_send_mail_should_be_called_with_correct_processed_params()

    class _ScenarioMaker(object):

        def __init__(self):
            self.response = None
            self.confirmation_token = None
            self.username = None
            self.email = None
            self.request = None

        def given_a_confirmation_token(self):
            self.confirmation_token = 'ABC'
            return self

        def given_a_username(self):
            self.username = 'usr.nm'
            return self

        def given_an_email(self):
            self.email = 'e@m.c'
            return self

        def given_a_request_that_builds_absolute_uri(self):
            self.request = Mock()
            self.url = 'https://base/url/confirmation/path'
            self.request.build_absolute_uri.return_value = self.url
            return self

        def when_send_ask_confirmation_mail_is_called(self):
            MailerService(self.request).send_ask_confirmation_mail(confirmation_token=self.confirmation_token,
                                                                   email=self.email, username=self.username)
            return self

        def then_django_send_mail_should_be_called_with_correct_processed_params(self):
            assert mail.outbox[0].subject == 'Abidria account confirmation'
            confirmation_url = "{}?token={}".format(self.url, self.confirmation_token)
            context_params = {'username': self.username, 'confirmation_url': confirmation_url}
            plain_text_message = get_template('ask_confirmation_email.txt').render(context_params)
            html_message = get_template('ask_confirmation_email.html').render(context_params)
            assert mail.outbox[0].body == plain_text_message
            assert mail.outbox[0].from_email == settings.EMAIL_HOST_USER
            assert mail.outbox[0].to == [self.email, ]
            assert mail.outbox[0].alternatives[0][0] == html_message
            return self
