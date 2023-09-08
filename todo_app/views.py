from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html', {'todos': [{'football': 'completed'}, {'django': 'pending'}] })

def about(request):
    return render(request, 'about.html')