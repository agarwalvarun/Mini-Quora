from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
# Create your models here.

class MyUser(AbstractUser):
	phone = models.CharField(max_length = 10, null = True)

def create_otp(user = None, purpose = None):
	if not user:
		raise ValueError('Invalid Arguments(user)')
	choices = []
	for choice_purpose, verbose in UserOTP.OTP_PURPOSE_CHOICES:
		choices.append(choice_purpose)
	if not purpose in choices:
		raise ValueError('Invalid Arguments(purpose)')
	if UserOTP.objects.filter(user = user, purpose = purpose).exists():
		old_otp = UserOTP.objects.filter(user = user, purpose = purpose)
		old_otp.delete()
	otp = randint(1000,9999)
	otp_object = UserOTP.objects.create(user = user, otp = otp, purpose = purpose)
	return otp

def get_valid_otp_object(user = None, purpose = None, otp = None):
	if not user:
		raise ValueError('Invalid Arguments(user)')
	choices = []
	for choice_purpose, verbose in UserOTP.OTP_PURPOSE_CHOICES:
		choices.append(choice_purpose)
	if not purpose in choices:
		raise ValueError('Invalid Arguments(purpose)')
	try:
		otp_object = UserOTP.objects.get(user = user, purpose = purpose, otp = otp)
		return otp_object
	except UserOTP.DoesNotExist:
		return None


class UserOTP(models.Model):
	OTP_PURPOSE_CHOICES = (
		('FP', 'Forgot Password'),
		('AA', 'Activate Account'),
	);
	user = models.ForeignKey(MyUser)
	otp = models.CharField(max_length = 4)
	purpose = models.CharField(max_length = 2, choices = OTP_PURPOSE_CHOICES)
	created_on = models.DateTimeField(auto_now_add = True)

	class Meta:
		unique_together = ['user', 'purpose']