from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    params = {"name": "John", "place": "New York"}
    return render(request, "index.html", params)

def about(request):
    return HttpResponse("This is the about page.")