from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

def foros(request):
    return render(request, 'blog/foros.html')