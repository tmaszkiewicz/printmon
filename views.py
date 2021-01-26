from django.shortcuts import render
from django.http import HttpResponse
from .functions import *
from .models import wydruk
from .forms import DateForm
import datetime
import pytz
from django.utils.timezone import make_aware

# Create your views here.

def monitor(request, *arg, **kwargs):
    url='printmon/printmon.html'

    context = {        
    }
    pobierz_plik()
    if request.method=='POST':
        form = DateForm(request.POST)
        if form.is_valid():
            od = form.cleaned_data['od']
            do = form.cleaned_data['do']
            grupowanie=form.cleaned_data['grupowanie']
            
            #do=form.cleaned_data['do'] 
            #now_aware = pytz.utc.localize(unaware)
            print(grupowanie)
            if grupowanie==0:
                w = wydruk.objects.filter(date__gte=od,date__lte=do).order_by('user').distinct('user','printer')
            elif grupowanie==1:
                    w = wydruk.objects.filter(date__gte=od,date__lte=do).order_by('user').distinct('user')
            elif grupowanie==2:
                    w = wydruk.objects.filter(date__gte=od,date__lte=do).order_by('printer').distinct('printer')
            elif grupowanie==3:
                w = wydruk.objects.filter(date__gte=od,date__lte=do).order_by('client').distinct('client')
            context['wydruk'] = w
            context['od'] = od
            context['do'] = do
            w2=[]
            data=[]
            labels=[]
            for i in w:
                print(i.user)
                w1={}
                w1['user']=i.user
                w1['client']=i.client
                w1['printer']=i.printer
                #w1['pages']=i.pages
                #w1['copies']=i.copies
                w1['suma_klient_pages']=i.suma_klient_pages(od,do,grupowanie) # 1=cpb client,printer,both
                w1['suma_klient_copies']=i.suma_klient_copies(od,do,grupowanie)
                w2.append(w1)
                data.append(i.suma_klient_pages(od,do,grupowanie))
                labels.append(i.user)

            context['w2']=w2
            context['data']=data
            context['labels']=labels
            context['grupowanie']=grupowanie

                

    else:
        None

    return render(request,url,context)
