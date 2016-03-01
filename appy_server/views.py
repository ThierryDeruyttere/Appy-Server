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
    file  = forms.CharField()

def handle_uploaded_file(form):
    user = form.cleaned_data["user"]
    title = form.cleaned_data["title"]
    file = form.cleaned_data["file"]

    if not os.path.isdir("appy's/" + user):
        os.mkdir('appy\'s/' + user)


    if not os.path.isdir("appy's/" + user + "/" + title):
        os.mkdir('appy\'s/' + user + "/" + title)


    with open("appy's/" + user + "/" + title + "/" + title + ".json", 'w') as destination:
        destination.write(file)

    path = "appy's/" + user + "/" + title + "/" + title + ".json"
    path = path.translate(str.maketrans({" ": "\ ",
                                         "'": "\\'",
                                         "\\": "\\\\"}))

    os.system("./convert.sh " + path)

@csrf_exempt
def upload_file(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseServerError("Invalid call")

    #handle_uploaded_file(form, request.FILES['file'])
    handle_uploaded_file(form)
    return HttpResponse('OK')