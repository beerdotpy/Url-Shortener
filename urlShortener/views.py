from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from models import User, URL, Click
from django.core.files import File
from serializers import UserSerializer, UrlSerializer
from rest_framework.renderers import JSONRenderer
import json
import random
import string
import md5
from django.contrib.auth.hashers import make_password,check_password

#prod_URL = ""
prefix = "localhost:8000/"

@csrf_exempt
def register(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(email = data['email'])
    except:
        user = User.objects.create(email = data['email'], password = make_password(data['password']))
    userSerializer = JSONRenderer().render((UserSerializer(user)).data)
    return HttpResponse(userSerializer)

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(email = data['email'])
    except:
        return HttpResponse("User not found")
    if check_password(data['password'], user.password):
        userSerializer = JSONRenderer().render((UserSerializer(user)).data)
        return HttpResponse(userSerializer)
    else:
        return HttpResponse("Wrong credentials")
    
@csrf_exempt
def shortenURL(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(email = data['email'])
    except:
        return HttpResponse(status = 404)
    try:
        url = URL.objects.get(original = data["url"])
    except:
        url = URL.objects.create(user = user, original = data['url'], shortenURL = getUrlCode())
    urlSerializer = JSONRenderer().render((UrlSerializer(url)).data)
    return HttpResponse(urlSerializer)

def getUrlCode():
    length = 6
    choices = string.ascii_uppercase + string.digits + string.ascii_lowercase
    while True:
        code = ''.join(random.choice(choices) for x in range(length))
        try:
            temp = URL.objects.get(shortenURL = code)
        except:
            return prefix + code

@csrf_exempt
def modifyURL(request):
    data = json.loads(request.body)
    try:
        url = URL.objects.get(shortenURL = data['url'])
    except:
        return HttpResponse("URL does not exist")
    url.original = data['newURL']
    url.save()
    return HttpResponse("URL changed")

@csrf_exempt
def deleteURL(request):
    data = json.loads(request.body)
    try:
        url = URL.objects.get(shortenURL = data['url'])
    except:
        return HttpResponse("URL not found")
    url.isActive = False
    url.save()
    return HttpResponse("URL deleted")

def clicksCount(request):
    data = json.loads(request)
    try:
        url = URL.objects.get(shortenURL = data['url'])
    except:
        return HttpResponse("URL not found")
    click = Click.objects.create(url = url)
    return HttpResponse("Click recorded")

def redirect(request, shortURL):
    temp = prefix + shortURL 
    try:
        url = URL.objects.get(shortenURL = temp)
    except:
        return HttpResponse("Redirect to default page")
    click = Click.objects.create(url = url)
    if url.isActive:
        return HttpResponseRedirect("http://" + url.original)
    else:
        return HttpResponse("Redirect to default page")
    