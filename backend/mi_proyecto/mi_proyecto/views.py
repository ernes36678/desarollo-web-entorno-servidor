from django.shortcuts import render

def homepage(request):
    """
    Renders and returns the home.html template.
    """
    return render(request, 'home.html')