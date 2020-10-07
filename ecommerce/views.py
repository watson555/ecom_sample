from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .forms import ContactForm  #,LoginForm,RegisterForm
# from django.contrib.auth import authenticate, login, get_user_model
# def home_page(request):
# 	return HttpResponse("<h1>Hello World</h1>")


def home_page(request):
	# print(request.session.get("first_name", "Unknown"))
    # request.session['first_name']
	context = {
	"title":"Hello World",
	"content":"Wellcome to home page"
	# "premium_content":"yyyyyyy"
	}
	if request.user.is_authenticated():
		context["premium_content"]="yyyyyyy"

	return render(request, 'home_page.html', context)

def about_page(request):
	context = {
	"title":"Hello World",
	"content":"Wellcome to home page"
	}
	return render(request, 'home_page.html', context)

def contact_page(request):
	context_form = ContactForm(request.POST or None)
	
	context = {
	"title":"Hello World",
	"content":"Wellcome to home page",
	"form":context_form
	}
	if context_form.is_valid():
		print(context_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message":"thank you"})

	if context_form.errors:
		errors = context_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')
	# if request.method=='POST':
	# 	# print(request.POST)
	# 	print(request.POST.get("fullname"))
	# 	print(request.POST.get("email"))
	# 	print(request.POST.get("content"))
	return render(request, 'contact/view.html', context)

