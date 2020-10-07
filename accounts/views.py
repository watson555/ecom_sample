from django.shortcuts import render,redirect
from django.views.generic import CreateView, FormView
from django.http import HttpResponse
from .forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url
from .models import GuestEmail
from .signals import user_logged_in


def guest_register_view(request):
	form = GuestForm(request.POST or None)
	context = {
	"form":form
	}
	# print(request.user.is_authenticated)
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if form.is_valid():
		print(form.cleaned_data)
		# context['form']=LoginForm()
		email = form.cleaned_data.get('email')
		new_guest_email=GuestEmail.objects.create(email=email)
		request.session["guest_email_id"]=new_guest_email.id
		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)
		else:
			# Redirect to a success page.
			return redirect('/register/')
	
	return redirect('/register/')

class LoginView(FormView):
	form_class =LoginForm
	template_name = 'accounts/login.html'
	success_url = '/'

	def form_valid(self,form):
		request = self.request
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		user = authenticate(request, username=email, password=password)
		# print(request.user.is_authenticated)
		print(user)	
		if user is not None:
			# print(request.user.is_authenticated)
			login(request, user)
			user_logged_in.send(user.__class__, instance=user, request=request)
			try:
				del request.session["guest_email_id"]
			except:
				pass
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				# Redirect to a success page.
				return redirect('/')
		return super(LoginView, self).form_invalid(form)





class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'accounts/register.html'
	success_url = '/login/'

# def login_page(request):
# 	form = LoginForm(request.POST or None)
# 	context = {
# 	"form":form
# 	}
# 	# print(request.user.is_authenticated)
# 	next_ = request.GET.get('next')
# 	next_post = request.POST.get('next')
# 	redirect_path = next_ or next_post or None

# 	if form.is_valid():
# 		print(form.cleaned_data)
# 		# context['form']=LoginForm()
# 		username = form.cleaned_data.get('username')
# 		password = form.cleaned_data.get('password')
# 		user = authenticate(request, username=username, password=password)
# 		# print(request.user.is_authenticated)
# 		print(user)	
# 		if user is not None:
# 			# print(request.user.is_authenticated)
# 			login(request, user)
# 			try:
# 				del request.session["guest_email_id"]
# 			except:
# 				pass
# 			if is_safe_url(redirect_path, request.get_host()):
# 				return redirect(redirect_path)
# 			else:
# 				# Redirect to a success page.
# 				return redirect('/')
# 		else:
# 			# Return an 'invalid login' error message.
# 			print("Error")
	
# 	return render(request, "accounts/login.html", context)


# User=get_user_model()
# def register_page(request):
# 	form = RegisterForm(request.POST or None)
# 	context = {
# 	"form":form
# 	}
# 	if form.is_valid():
# 		form.save()
# 		# print(form.cleaned_data)
# 		# username = form.cleaned_data.get('username')
# 		# email = form.cleaned_data.get('email')
# 		# password = form.cleaned_data.get('password')
# 		# new_user = User.objects.create_user(username, email, password)
# 		# print(new_user)
	
# 	return render(request, "accounts/register.html", context)