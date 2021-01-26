from django.db import models
from django.db.models import Sum
from django import template
#register = template.Library()

class wydruk(models.Model):
    time_text = models.CharField(max_length=50,blank=True,null=True)
    time = models.DateTimeField(blank=True,null=True) #default=now())
    date = models.DateField(blank=True,null=True) #default=now())
    user = models.CharField(max_length=20,blank=True,null=True)
    pages = models.IntegerField(blank=True,null=True)
    copies = models.IntegerField(blank=True,null=True)
    printer =  models.CharField(max_length=30,blank=True,null=True)
    doc = models.CharField(max_length=100,blank=True,null=True)
    client = models.CharField(max_length=30,blank=True,null=True)
    doctype =  models.CharField(max_length=30,blank=True,null=True)
    duplex = models.BooleanField(default=False)
    grayscale=models.BooleanField(default=True)
#    @register.simple_tag
    def suma_klient_pages(self, od, do, cpb):
        my_filter={}
        my_filter['date__gte']=od
        my_filter['date__lte']=do
        if cpb==0:
            my_filter['user']=self.user
            my_filter['printer']=self.printer
        elif cpb==2:
            my_filter['printer']=self.printer
        elif cpb==1:
            my_filter['user']=self.user
        elif cpb==3:
            my_filter['client']=self.client

        
        #suma=wydruk.objects.filter(date__gte=od,date__lte=do,client=self.client,printer=self.printer).aggregate(Sum('pages'))
        suma=wydruk.objects.filter(**my_filter).aggregate(Sum('pages'))
        return suma['pages__sum']
    def suma_klient_copies(self, od, do, cpb):
        my_filter={}
        my_filter['date__gte']=od
        my_filter['date__lte']=do
        if cpb==0:
            my_filter['user']=self.user
            my_filter['printer']=self.printer
        elif cpb==2:
            my_filter['printer']=self.printer
        elif cpb==1:
            my_filter['user']=self.user
        elif cpb==3:
            my_filter['client']=self.client
        #suma=wydruk.objects.filter(date__gte=od,date__lte=do,client=self.client,printer=self.printer).aggregate(Sum('copies'))
        suma=wydruk.objects.filter(**my_filter).aggregate(Sum('copies'))
        return suma['copies__sum']
    def __str__(self):
        return self.printer + self.doc 
class plik(models.Model):
    nazwa = models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.nazwa

    


    

# Create your models here.


