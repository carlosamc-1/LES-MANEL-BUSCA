from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

def WelcomeView(request) :

    template = loader.get_template('welcome_screen.html')
    context = {
        'isLoggedIn' : request.user.is_authenticated,
        'user' : request.user,
    }
    return HttpResponse(template.render(context, request))
