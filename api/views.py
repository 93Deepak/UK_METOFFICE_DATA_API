
import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from bs4 import BeautifulSoup

from .models import *


def params():
    # try:
    #     obj = Country.objects.last()
    # except:
    #     obj = None
    # if obj == None:
    
    ls_region = []
    ls_parameter = []
    r = requests.get("https://www.metoffice.gov.uk/research/climate/maps-and-data/uk-and-regional-series")
    soup = BeautifulSoup(r.content, 'html.parser')
    region = soup.find(id='region')
    region_list = region.find_all("option")
    parameter = soup.find(id='parameter')
    param_list = parameter.find_all("option")
    for i in region_list:
        if i['value'] != '':
            ls_region.append(i['value'])
    for i in param_list:
        if i['value'] != '':
            ls_parameter.append(i['value'])
        
    return ls_region, ls_parameter
        # for i in region_list:
        #     obj = Country.objects.create(country=i['value'])
        #     obj.save()
        #     for j in param_list:
        #         param = Parameter.objects.create(country=obj, parameter=j['value'])
    # else:
    #     pass
                           
    
# Create your views here.
def get_data(param,country):
    try:
        r = requests.get(
            "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{}/date/{}.txt".format(param,country))
        res = json.dumps(r._content.decode('utf-8'), default=str)
        file = open("data.txt","w+")
        file.write(json.loads(res))
        file.close()
    except:
        return JsonResponse({'Status':"Could Not Fetch Data"})

@csrf_exempt
def Check(request):
    if request.POST:
        get_data(request.POST.get('Parameter'), request.POST.get('Country'))
        with open("data.txt","r") as f:
            data = f.readlines()
            Head = []
            # Head = ['Year','Jan','Feb','Mar','Apr','May','June','July','August','Sept','oct','Nov','Dec','Winter','Spring','Summer','Autumn','Annual']
            value = []
            
            
            for index,i in enumerate(data):
                n = 0
                if index == 5:
                    for j in range(len(i)):
                        if n < 89:
                            Head += [data[index][n:n+4]]
                            n += 7
                        elif n >= 91 and n <= 122:
                            Head += [data[index][n:n+7]]
                            n += 8
                        elif n > 122 and n <= 129:
                            Head += [data[index][n:n+5]]
                            n+= 8
                        else:
                            n += 1
                        
                if index > 5:
                    ls = []
                    for j in range(len(i)):
                        if n < 89:
                            ls += [data[index][n:n+4]]
                            n += 7
                        elif n >= 91 and n <= 122:
                            ls += [data[index][n:n+7]]
                            n += 8
                        elif n > 122 and n <=129:
                            ls += [data[index][n:n+5]]
                            n += 8
                        else:
                            n += 1
                    value.append(ls)
                            
                            
            
            
            respons = {}
            for i in range(len(value)):
                index = {}
                data = {}
                index[Head[0]] = value[i][0]
                for j in range(len(Head)):
                    if j > 0:
                        data[Head[j]] = value[i][j]
                index['data'] = data
                respons[i] = index            
            
            return JsonResponse({'data':respons})
    else:
        region, param = params()
        
        return JsonResponse({'Query':"To get weather data send Post request with following keywords from list, example Country=UK, Parameter=Tmax",'KeyWords':{'Country':region,'Parameter':param}})
    

    