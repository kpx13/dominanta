# encoding: utf-8
from django import forms
from django.forms import ModelForm
from models import Article
from django.forms.widgets import CheckboxSelectMultiple

class ArticleForm(ModelForm):
    #category = forms.CharField(widget=CheckboxSelectMultiple())
    class Meta:
        model = Article
        exclude = ('request_date', )