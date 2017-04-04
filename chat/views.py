from django.views.generic import View
from .models import *
from django.shortcuts import render,get_object_or_404,render_to_response,redirect
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
		print(ps)
		user = auth.authenticate(username=un,password=ps)
		if user is not None and user.is_active:
			auth.login(request,user)
			print("Login Successful! - " + ps)
			uid = user.id
			return redirect("home",uid)
		else:
			print("Not Successful")
			return redirect("login")

class register(View):
	def get(self,request):
		return render(request,'chat/register.html')

	def post(self,request):
		name = request.POST['name']
		un = request.POST['username']
		ps = request.POST['password']
		mail = request.POST['email']
		cont = request.POST['contact']

		myuser = User.objects.create_user(username=un,password=ps,email=mail)
		print(myuser)
		if myuser is not None:
			p = Person.objects.create(user=myuser,name=name,contact=cont)
			p.save()

			print('created')
			return redirect("login")
		else:
			print("error")
			return redirect("register")

class home(LoginRequiredMixin,View):
	login_url = "/"
	def get(self,request,uid):
		s = Person.objects.get(pk=uid)
		users = Person.objects.exclude(pk=uid)
		print(users)
		return render(request,'chat/home.html',locals())

class dialog(LoginRequiredMixin,View):
	login_url = "/"
	def get(self,request,uid,uuid):
		a = Person.objects.get(pk=uid)
		b = Person.objects.get(pk=uuid)
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
		
		print(dial)
		messages = Message.objects.filter(dialog=dial)
		print(messages)
		return render(request,'chat/dialog.html',locals())


	def post(self,request,uid,uuid):
		mt = request.POST.get('msg',"haha")
		a = Person.objects.get(pk=uid)
		b = Person.objects.get(pk=uuid)
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
		print(d)
		print(mt)
		print(send)
		m = Message.objects.create(dialog=de,sender=send,text=mt)
		m.save()
		return redirect("dialog",uid,uuid)


class logout(View):
	def get(self,request):
		return redirect('login')

