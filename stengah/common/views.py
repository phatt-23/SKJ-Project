from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.

def index(req: HttpRequest):

    return render(
        req, 
        "web/index.html",
        {
        }
    )
