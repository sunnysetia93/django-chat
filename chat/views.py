from django.views.generic import View
from django.core import serializers
from .models import *
from django.http import JsonResponse,HttpResponse
import json
import simplejson
from django.shortcuts import render,get_object_or_404,render_to_response,redirect,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout,get_backends
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class login(View):
	def get(self,request):
		return render(request,'chat/login.html')

	def post(self,request):
		un = request.POST['username']
		ps = request.POST['password']
		user = auth.authenticate(username=un,password=ps)
		if user is not None and user.is_active:
			auth.login(request,user)
			request.session['userid'] = user.id
			p = Person.objects.get(pk=user.id)
			p.online = 1
			print(p.online)
			p.save()
			print("Login Successful!")
			uid = user.id
			return redirect("home")
		else:
			errors = 1
			print("Not Successful")
			return render(request,'chat/login.html',locals())

class register(View):
	def get(self,request):
		return render(request,'chat/register.html')

	def post(self,request):
		name = request.POST['name']
		un = request.POST['username']
		ps = request.POST['password']
		mail = request.POST['email']
		cont = request.POST['contact']
		
		if un is not '':
			checkuser = User.objects.filter(username=un).count()
			if checkuser == 0:
				myuser = User.objects.create_user(username=un,password=ps,email=mail)
				print(myuser)
				if myuser is not None:
					p = Person.objects.create(id=myuser.id,user=myuser,name=name,contact=cont)
					p.save()

					print('created')
					return redirect("login")
			else:
				errors = 2
				print("Not Successful")
				return render(request,'chat/register.html',locals())

		else:
			errors = 1
			print("Not Successful")
			return render(request,'chat/register.html',locals())

class home(LoginRequiredMixin,View):
	login_url = "/"
	def get(self,request):
		user = request.user
		s = Person.objects.get(pk=user.id)
		users = Person.objects.exclude(pk=user.id)
		# print(users)
		return render(request,'chat/home.html',locals())

class dialog(LoginRequiredMixin,View):
	login_url = "/"
	def get(self,request,uid):
		if request.user.is_active and request.user.is_authenticated:
			a = Person.objects.get(pk=request.user.id)
			b = Person.objects.get(pk=uid)
			dial = getDialog(a,b)
			# print(dial)
			messages = Message.objects.filter(dialog=dial)
			# print(messages)
			return render(request,'chat/dialog.html',locals())
		else:
			return render(request,'chat/home.html',locals())

class logout_view(View):
	def get(self,request):
		p = Person.objects.get(pk=request.user.id)
		p.online = 0
		print(p.online)
		p.save()
		logout(request)
		return redirect('/')

def getDialog(a,b):
	d = Dialog.objects.filter(author=a,reader=b).count()
	d1 = Dialog.objects.filter(author=b,reader=a).count()
	if d==1 and d1==0:
		print("case3")	
		dial = Dialog.objects.get(author=a,reader=b)
		sender = a

	elif d==0 and d1==1:
		print("case2")
		dial = Dialog.objects.get(author=b,reader=a)
		sender = b
	elif d==0 and d1==0:
		print("case1")
		dial = Dialog.objects.create(author=a,reader=b)
		sender = a

	return dial

def messages(request):
	print("in messages view")
	user = request.user
	s = Person.objects.get(pk=user.id)
	users = Person.objects.exclude(pk=user.id)
	data = serializers.serialize('json',users)
	return HttpResponse(data,content_type='application/json')


def getmessages(request):
	print("in getmessages view")
	JSONdata = request.POST['text']
	uid = request.POST['uid']
	print(JSONdata)
	print(uid)
	a = Person.objects.get(pk=request.user.id)
	b = Person.objects.get(pk=uid)
	d = Dialog.objects.filter(author=a,reader=b).count()
	d1 = Dialog.objects.filter(author=b,reader=a).count()
	if d==1 and d1==0:
		print("case3")	
		dial = Dialog.objects.get(author=a,reader=b)
		sender = a

	elif d==0 and d1==1:
		print("case2")
		dial = Dialog.objects.get(author=b,reader=a)
		sender = b
	de = dial
	send = a
	m = Message.objects.create(dialog=de,sender=send,text=JSONdata)
	m.save()
	messages = Message.objects.filter(dialog=dial)

	data = '['
	for m in Message.objects.filter(dialog=dial):
		p = Person.objects.get(pk=m.sender.id)
		# print(m.text)
		# print(p.name)
		data += json.dumps({

			"text" : m.text,
			"sender" : p.name

			}) + ','

	data += '{}]'
	print(data)
	# dat = serializers.serialize('json',data)

	return HttpResponse(data,content_type='application/json')
