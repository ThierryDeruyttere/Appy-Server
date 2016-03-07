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
import shutil

@xframe_options_exempt
def home(request):
    return render(request, 'output.html')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    user = forms.CharField(max_length=50)
    file = forms.CharField()

def escapeString(string):
    return string.translate(str.maketrans({" ": "\ ",
                                         "'": "\\'",
                                         "\\": "\\\\"}))


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
    path = escapeString(path)

    response = os.system("./convert.sh " + path)
    shutil.copy("appy's/" + user + "/" + title + "/" + title + ".html", "templates/output.html")
    return user, title

@csrf_exempt
def upload_file(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed('Only POST here')

    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponseServerError("Invalid call")

    # handle_uploaded_file(form, request.FILES['file'])
    user, appy = handle_uploaded_file(form)

    return HttpResponse('OK')


def get_qr(request, user, appy):
    import socket
    ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    path = ip+":8000/"+ "appy's/" + user + "/" + user + "/" + appy + ".html"
    path = escapeString(path)
    return render(request, "qr.html", {"path": path})

def serve_appy(request, user, appy):
    return render(request, "output.html", {})
