from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')    # getting next page
	title = "Login"
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)     # checking authentication using authenticate

		login(request, user)
		# print(request.user.is_authenticated())
		if next:
			return redirect(next)      # Go next page after login if next request is set
		return redirect("/")    # After login go homepage

	context = {
		"form": form,
		"title": title,
	}

	return render(request, "accounts/login.html", context)

def register_view(request):
	next = request.GET.get('next')    # getting next page
	title = "Register"
	form = UserRegisterForm(request.POST or None)

	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		if next:
			return redirect(next)      # Go next page after login if next request is set
		return redirect("/")         # After login go homepage

	context = {
		"title": title,
		"form": form,
	}
	return render(request, "accounts/register.html", context)

def logout_view(request):
	logout(request)
	return redirect("/")
