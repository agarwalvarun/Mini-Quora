from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm, ForgotPassword, SetNewPassword
from .models import MyUser, UserOTP, create_otp, get_valid_otp_object
from django.template import loader
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from question.models import Question

# Create your views here.

# @require_GET
# def show_login(request):
# 	if request.user.is_authenticated():
# 		return redirect(reverse('home', kwargs={'id' : request.user.id}))
# 	return render(request, 'account/auth/login.html')

@require_http_methods(['GET', 'POST'])
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs={'id' : request.user.id}))
	if request.method == 'GET':
		context = { 'f' : LoginForm() }
		return render(request, 'account/auth/login.html', context)
	else:
		f = LoginForm(request.POST)
		if not f.is_valid():
			context = {'f' : f}
			return render(request, 'account/auth/login.html', context)
		username = request.POST.get('username')
		password = request.POST.get('password')	
		user = authenticate(username = username, password = password)
		if not user:
			context={'error' : 'Invalid Username/Password', 'f' : LoginForm()}
			return render(request, 'account/auth/login.html',context)
		if not user.is_active:
			return render(request, 'account/auth/not_activated_user.html', {'u' : user})
		auth_login(request,user)
		return redirect(reverse('home', kwargs={'id' : user.id}))

@require_GET
@login_required
def home(request, id):
	context = {'all_q_list': Question.objects.order_by('-created_on')}
	return render(request,'account/auth/home.html', context)
	'''
	Display LoggedIn Home page
	'''

@require_http_methods(['GET', 'POST'])
def forgot_password(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs = {'id' : request.user.id}))
	if request.method == 'GET':
		context = {'f' : ForgotPassword()}
		return render(request, 'account/auth/forgot_password.html', context)
	f = ForgotPassword(request.POST)	
	if not f.is_valid():
		context = {'f' : f}
		return render(request, 'account/auth/forgot_password.html', context)
	user = MyUser.objects.get(username = f.cleaned_data.get('username'))
	otp = create_otp(user = user, purpose = 'FP')
	email_body_context = {'u' : user, 'otp' : otp}
	body = loader.render_to_string('account/auth/email/forgot_password.txt', email_body_context)
	message = EmailMultiAlternatives('Reset Password', body, settings.EMAIL_HOST_USER, [user.email])
	message.send()
	return render(request, 'account/auth/forgot_password_sent.html', {'u' : user})

@require_http_methods(['GET', 'POST'])
def reset_password(request, id = None, otp = None):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs = {'id' : request.user.id}))
	user = get_object_or_404(MyUser, id = id)
	otp_object = get_valid_otp_object(user = user, purpose = 'FP', otp = otp)
	if not otp_object:
		raise Http404
	if request.method == 'GET':
		context = {'f' : SetNewPassword(), 'otp' : otp_object.otp, 'u' : user}
		return render(request, 'account/auth/set_new_password.html', context)
	f = SetNewPassword(request.POST)
	if not f.is_valid():
		context = {'f' : f, 'otp' : otp_object.otp, 'u' : user}
		return render(request, 'account/auth/set_new_password.html', context)
	user.set_password(f.cleaned_data.get('new_password'))
	user.save()
	otp_object.delete()
	return render(request, 'account/auth/set_new_password_success.html', {'u' : user})

@require_http_methods(['GET','POST'])
def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs={'id' : request.user.id}))
	if request.method == 'GET':
		context = {'f' : SignUpForm()}
		return render(request, 'account/auth/sign_up.html', context)
	f = SignUpForm(request.POST)
	if not f.is_valid():
		context = {'f' : f}
		return render(request, 'account/auth/sign_up.html', context)
	user = f.save(commit = False)
	user.set_password(f.cleaned_data.get('password'))
	user.is_active = False
	user.save()	
	'''
	Generate OTP/Activation E-mail
	'''
	otp = create_otp(user = user, purpose = 'AA')
	email_body_context = {'u' : user, 'otp' : otp}
	body = loader.render_to_string('account/auth/email/activation_mail.txt', email_body_context)
	message = EmailMultiAlternatives('Activation E-mail', body, settings.EMAIL_HOST_USER, [user.email])
	message.send()
	return render(request, 'account/auth/sign_up_success.html', {'u' : user})

@require_GET
def activate(request, id = None, otp = None):
	user = get_object_or_404(MyUser, id = id)
	otp_object = get_valid_otp_object(user = user, purpose = 'AA', otp = otp)
	if not otp_object:
		raise Http404
	user.is_active = True
	user.save()
	otp_object.delete()
	return render(request, 'account/auth/activation_success.html', {'u' : user})

def logout(request):
	auth_logout(request)
	return redirect(reverse('login'))