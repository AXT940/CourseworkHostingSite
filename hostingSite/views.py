from django.http import HttpResponse

def homepage(question):
    return HttpResponse("Viewing the homepage, initial page for the website. First point of contact.")

def login(request):
    return HttpResponse("Log in page for the users.")

def register(request):
    return HttpResponse("Register page which is used to create new users.")
