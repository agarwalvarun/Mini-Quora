from django import forms
from django.forms import ModelForm
from .models import Question, Answer

class AddQuestion(ModelForm):	
	def clean_title(self):
		data_title = self.cleaned_data.get('title')
		if not data_title:
			raise forms.ValidationError("This field cannot be empty")
		return data_title
	class Meta:
		model = Question
		fields = ['title', 'text']
class AddAnswer(ModelForm):
	class Meta:
		model = Answer
		fields = ['text']
		
