from django.shortcuts import render

# Create your views here.

def about_site(request):
    return render(request, 'about_site.html')