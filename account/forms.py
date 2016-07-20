from django import forms
from django.forms import ModelForm
from .models import MyUser

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 25)
	password = forms.CharField(widget = forms.PasswordInput)

class ForgotPassword(forms.Form):
	username = forms.CharField(max_length = 25)

	def clean_username(self):
		data_username = self.cleaned_data.get('username','')
		if data_username and not MyUser.objects.filter(username = data_username).exists():
			raise forms.ValidationError("Invalid Username")
		return data_username

class SetNewPassword(forms.Form):
	new_password = forms.CharField(max_length = 25, widget = forms.PasswordInput)
	confirm_new_password = forms.CharField(max_length = 25, widget = forms.PasswordInput)

	def clean_confirm_new_password(self):
		data_new_password = self.cleaned_data.get('new_password')
		data_confirm_new_password = self.cleaned_data.get('confirm_new_password')
		if (data_new_password and data_confirm_new_password and data_new_password != data_confirm_new_password):
			raise forms.ValidationError("The two passwords don't match")
		return data_confirm_new_password

class SignUpForm(ModelForm):
	password = forms.CharField(max_length = 25, widget = forms.PasswordInput)
	confirm_password = forms.CharField(max_length = 25, widget = forms.PasswordInput)

	def clean_email(self):
		data_email = self.cleaned_data.get('email','')
		if not data_email:
			raise forms.ValidationError("This field is required")
		if MyUser.objects.filter(email = data_email):
			raise forms.ValidationError("This e-mail already exists")
		return data_email

	def clean_confirm_password(self):
		data_password = self.cleaned_data.get('password')
		data_confirm_password = self.cleaned_data.get('confirm_password')
		if (data_password and data_confirm_password and data_password != data_confirm_password):
			raise forms.ValidationError("The two passwords dont match")
		return data_confirm_password

	class Meta:
		model = MyUser
		fields = ['username', 'phone', 'first_name', 'last_name', 'email']

		