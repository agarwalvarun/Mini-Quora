from django.conf.urls import url
from .views import print_question, print_all_question, add_question, add_answer
urlpatterns=[
	url(r'^all/$', print_all_question),
	url(r'^(?P<id>\d+)/$', print_question, name = 'print_question'),
	url(r'^add/$', add_question, name = "add_question"),
	url(r'^(?P<q_id>\d+)/add-answer$', add_answer, name = "add_answer"),
]