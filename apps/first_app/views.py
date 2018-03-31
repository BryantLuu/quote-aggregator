from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from models import *
import bcrypt

# Create your views here.
def index(request):
	if request.session['logged_in']:
		return redirect('/quotes')
	return render(request, 'index.html')

def register(request):
	msgs = User.objects.regValidator(request.POST)
	if len(msgs):
		for k,v in msgs.iteritems():
			print k,v
		 	messages.error(request, v, extra_tags=k)
	else:
		hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email=request.POST['email'], password=hashedpw)
		user = User.objects.last()
		request.session['logged_in'] = user.id
		print request.session['logged_in']
		return redirect('/success')
	return redirect('/')

def login(request):
	msgs = User.objects.loginValidator(request.POST)
	if len(msgs):
		print msgs
	else:
		user = User.objects.get(email=request.POST['login_email'])
		request.session['logged_in'] = user.id
		return redirect('/quotes')
	return redirect('/')

def quotes(request):
	quotes = Quote.objects.exclude(
		favorites=request.session['logged_in'],
	)
	favorite_quotes = Quote.objects.filter(
		favorites=request.session['logged_in'],
	)
	context = {
		'user': User.objects.get(id=request.session['logged_in']),
		'quotes': quotes,
		'favorite_quotes': favorite_quotes,
	}
	return render(request, 'quotes.html', context)

def create_quote(request):
	Quote.objects.create(
		content=request.POST['message'],
		quoter=request.POST['quoted_by'],
		user=User.objects.get(pk=request.session['logged_in']),
	)
	return redirect('/quotes')

def profile(request, **kwargs):
	quotes = Quote.objects.filter(
		user_id=kwargs['id'],
	)
	context = {
		'user': User.objects.get(id=request.session['logged_in']),
		'quotes': quotes,
	}
	return render(request, 'profile.html', context)

def add_favorite(request, **kwargs):
	user = User.objects.get(id=request.session['logged_in'])
	quote = Quote.objects.get(
		pk=request.POST['quote_id']
	)
	quote.favorites.add(user)
	return redirect('/quotes')

def remove_favorite(request, **kwargs):
	user = User.objects.get(id=request.session['logged_in'])
	quote = Quote.objects.get(
		pk=request.POST['quote_id']
	)
	quote.favorites.remove(user)
	return redirect('/quotes')

def log_out(request, **kwargs):
	request.session['logged_in'] = None
	return redirect('/')
