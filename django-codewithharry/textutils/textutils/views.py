from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    params = {"name": "John", "place": "New York"}
    return render(request, "index.html", params)

def about(request):
    return HttpResponse("This is the about page.")

def analyze(request):
    djtext = request.GET.get("text", "default")
    removepunc = request.GET.get("removepunc", "off")
    print(removepunc)
    if removepunc == "on":
        punctuations = '''!()-[]{};:'",<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        params = {"purpose": "Removed Punctuations", "analyzed_text": analyzed}
        return render(request, "analyze.html", params)
    else:
        return HttpResponse("Error")
