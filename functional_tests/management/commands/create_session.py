from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


class Command(BaseCommand):
	args = '<email>'
	
	def handle(self, email, **__):
		session_key = create_pre_authenticated_session(email)
		self.stdout.write(session_key)
		

def create_pre_authenticated_session(email):
	user = User.objects.create(email=email)
	session = SessionStore()
	session[SESSION_KEY] = user.pk
	session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
	session.save()
	return session.session_key