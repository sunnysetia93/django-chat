from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=50)
	contact = models.CharField(max_length=12)

	def __str__(self):
		return self.name

class Dialog(models.Model):
	author = models.ForeignKey(Person,related_name="self")
	reader = models.ForeignKey(Person)

	def __str__(self):
		return self.author.name + " - " + self.reader.name

class Message(models.Model):
	dialog = models.ForeignKey(Dialog,unique=True)
	sender = models.ForeignKey(Person,unique=True)
	text = models.TextField()

	def __str__(self):
		return self.sender.name + " : " + self.text
