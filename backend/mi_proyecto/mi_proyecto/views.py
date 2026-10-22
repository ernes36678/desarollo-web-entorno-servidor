from django.shortcuts import render


def homepage(request):
    """
    Renders and returns the homepage template.
    """
    return render(request, 'index.html')


def contacto(request):
    return render(request, 'contacto.html')
