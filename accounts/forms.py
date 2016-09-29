from django import forms
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)

User = get_user_model()      # user object for UserRegisterForm


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		# user = authenticate(username=username, password=password)     # checking authentication using authenticate

		# user_qs = User.objects.filter(username=username)			  # or using user object filter "Either above or below works"
		# if user_qs.count == 1:
		# 	user = user_qs.first();

		if username and password:
			user = authenticate(username=username, password=password)     # checking authentication using authenticate
			if not user:
			    raise forms.ValidationError("Wrong username or password")
			if not user.check_password(password):
				raise forms.ValidationError("Wrong password")
			if not user.is_active:
				raise forms.ValidationError("This user is nolonger active")
		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):

	email = forms.EmailField(label="Email Address")
	email2 = forms.EmailField(label="Confirm Email")
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'email2', 'password']


	# def clean(self, *args, **kwargs):           # overriding the clean method but the same as below(clean_email2)
	# 	email = self.cleaned_data.get('email')
	# 	email2 = self.cleaned_data.get('email2')

	# 	if email != email2:
	# 		raise forms.ValidationError("Emails Must much")

	# 	email_qs = User.objects.filter(email=email)       # checking if email already exists
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This email is already taken!")
	# 	return super(UserRegisterForm, self).clean(*args, **kwargs)


	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')

		if email != email2:
			raise forms.ValidationError("Emails Must much")

		email_qs = User.objects.filter(email=email)       # checking if email already exists
		if email_qs.exists():
			raise forms.ValidationError("This email is already taken!")
		return email