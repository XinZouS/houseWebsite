from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User


def register(request):
	if request.method == 'POST':
		# get vals
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password']
		password2 = request.POST['password2']

		testOk = True
		if password1 != password2:
			messages.error(request, 'Passwords do not match')
			request.GET['password'] = ''
			request.GET['password2'] = ''
			testOk = False

		if User.objects.filter(username=username).exists():
			messages.error(request, 'The username is taken')
			testOk = False

		if User.objects.filter(email=email).exists():
			messages.error(request, 'The email is being used')
			testOk = False

		if not testOk:
			values = {
				'first_name': first_name,
				'last_name': last_name,
				'username': username,
				'email': email,
			}
			context = {
				'values': values,
			}
			return render(request, 'accounts/register.html', context)

		# looks good, create user
		user = User.objects.create_user(username=username, password=password1,
			email=email, first_name=first_name, last_name=last_name)
		# login after reigster
		# auth.login(request, user)
		# messages.success(request, 'You are now logged in')
		# return redirect('index')
		user.save()
		messages.success(request, 'You are registered')
		return redirect('login')

	return render(request, 'accounts/register.html')

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			messages.success(request, 'You are now logged in')
			return redirect('dashboard')
		else:
			messages.error(request, 'Invalid credentials')
			return redirect('login')

	return render(request, 'accounts/login.html')


def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		messages.success(request, 'You are logged out')
		return redirect('index')
		
	return render(request, 'accounts/logout.html')

def dashboard(request):
	return render(request, 'accounts/dashboard.html')

