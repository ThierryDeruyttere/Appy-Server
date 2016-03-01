from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.clickjacking import xframe_options_exempt
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
import os

@xframe_options_exempt
def home(request):
    return render(request, 'output.html')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    user = forms.CharField(max_length=50)
    file  = forms.FileField()

def handle_uploaded_file(form, f):
    user = form.cleaned_data["user"]
    title = form.cleaned_data["title"]

    if not os.path.isdir(os.path.join(os.getcwd()) + "appy's/" + user):
        os.mkdir('appy\'s/' + user)

    with open("appy's/" + user + "/" + title, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@csrf_exempt
def upload_file(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseServerError("Invalid call")


    handle_uploaded_file(form, request.FILES['file'])
    return HttpResponse('OK')