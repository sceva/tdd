from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


class Command(BaseCommand):

	def handle(self, *_, **__):
		session_key = create_pre_authenticated_session()
		self.stdout.write(session_key)
		

def create_pre_authenticated_session():
	user = User.objects.create(email = 'edith@email.com')
	session = SessionStore()
	session[SESSION_KEY] = user.pk
	session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
	session.save()
	return session.session_key