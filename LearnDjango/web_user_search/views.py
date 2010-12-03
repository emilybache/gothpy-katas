# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from models import WebUser
from forms import WebUserForm, SearchUserForm

def index(request):
    return HttpResponse("Hello World")
    
    
def new_user(request):
    message = ""
    if request.method == "POST":
        form = WebUserForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Successfully added user"
        else:
            message = "Invalid form submission"
    return render_to_response('new_user.html', 
                              {'message' : message, 'form' : WebUserForm()},
                              RequestContext(request))
                              
def search(request):
    form = SearchUserForm(request.GET)
    results = []
    if form.is_valid():
        name = form.cleaned_data['search']
        results = WebUser.objects.filter(name__icontains = name)
    return render_to_response('search.html', 
                                {'form' : SearchUserForm(), 
                                'results' : results},
                                RequestContext(request))