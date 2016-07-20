from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404,JsonResponse,HttpResponse
from .models import Question, Answer
from django.core import serializers
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import AddQuestion, AddAnswer
from account.models import MyUser
from django.core.urlresolvers import reverse

# Create your views here.
@require_GET
@login_required
def print_all_question(request):
	context={'q_list':Question.objects.all()}
	return render(request,'question/print_all_question.html',context)
@require_GET
@login_required
def print_question(request, id=None):
	question = get_object_or_404(Question, id = id)
	ques_answers = Answer.objects.filter(question = question).order_by('-created_on')
	context = {'q' : question, 'q_a' : ques_answers}
	return render(request, 'question/print_question.html', context)

@require_http_methods(['GET','POST'])
@login_required
def add_question(request):
	if request.method == 'GET':
		context = {'f' : AddQuestion()}
		return render(request,'question/add_question_form.html',context)
	f = AddQuestion(request.POST)
	if not f.is_valid():
		context = {'f' : f}
		return render(request, 'question/add_question_form.html', context)
	if Question.objects.filter(title = f.cleaned_data.get('title'), created_by = request.user):
		context = {'f' : f, 'error' : "This Question already exists"}
		return render(request, 'question/add_question_form.html', context)
	# Question.objects.create(title = f.cleaned_data.get('title'),created_by = request.user)
	question = f.save(commit = False)
	question.created_by = request.user
	question.save()
	return redirect(reverse('home', kwargs={'id' : request.user.id}))

@require_http_methods(['GET','POST'])
@login_required
def add_answer(request,q_id = None):
	q = get_object_or_404(Question, id = q_id)
	if request.method == 'GET':
		context = {'f' : AddAnswer(), 'q' : q}
		return render(request, 'question/add_answer.html', context)
	f = AddAnswer(request.POST)
	if not f.is_valid():
		context = {'f' : f}
		return render(request, 'question/add_answer.html', context)
	question = get_object_or_404(Question, id = q_id)
	answer = f.save(commit = False)
	answer.created_by = request.user
	answer.question = question
	answer.save()
	return redirect(reverse('print_question', kwargs = {'id' : q.id}))



# @require_POST
# def save_question(request):
# 	title = request.POST.get('title')
# 	if not title:
# 		raise Http404
# 	Question.objects.create(title = title,created_by = request.user)
# 	return HttpResponse('ok')