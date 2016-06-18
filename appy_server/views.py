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
from export import exporter
import os
import shutil
import json
from export.exporter.App import App

@xframe_options_exempt
def home(request):
    return render(request, 'home.html')

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

    if not os.path.isdir("appys/" + user):
        os.mkdir('appys/' + user)

    if not os.path.isdir("appys/" + user + "/" + title):
        os.mkdir('appys/' + user + "/" + title)

    with open("appys/" + user + "/" + title + "/" + title + ".json", 'w') as destination:
        destination.write(file)

    path = "appys/" + user + "/" + title + "/" + title + ".json"
    path = escapeString(path)

    app_description = json.load(open(path, 'r'))
    app = App(app_description)

    path_array = path.split(".")
    f = open(path_array[0] + ".html", 'w')
    f.write(app.generate())
    f.close()

    #exporter.export(path)
    shutil.copy("appys/" + user + "/" + title + "/" + title + ".html", "templates/output.html")
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

    # import socket
    # ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    # path = ip + "/" + "apps/" + user + "/" + appy + "/" + appy + ".html"
    path = "https://appy-ua.herokuapp.com/apps/" + user + "/" + appy + "/" + appy + ".html"
    path = escapeString(path)
    data = {"link": path, "author": user, "version": "1.0.0", "title": appy}
    return HttpResponse(json.dumps(data), content_type="application/json")

def get_qr(request, user, appy):
    # http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    # import socket
    # ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    # path = ip + "/" + "apps/" + user + "/" + appy + "/" + appy + ".html"
    path = "https://appy-ua.herokuapp.com/apps/" + user + "/" + appy + "/" + appy + ".html"
    path = escapeString(path)
    data = {"link": path, "author": user, "version": "1.0.0", "title": appy}
    # return render(request, "qr.html", {"data": json.dumps(data)})
    return HttpResponse(json.dumps(data), content_type="application/json")

@xframe_options_exempt
def serve_appy(request, user, appy):
    file = user + "/" + appy + "/" + appy + ".html"

    return render(request, file, {})
