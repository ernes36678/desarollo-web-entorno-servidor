from django.shortcuts import render

def index(request):
    """
    Renders and returns the escaparate page template.
    """
    return render(request, 'escaparate/escaparate.html')    