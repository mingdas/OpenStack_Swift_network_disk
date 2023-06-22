import sys
import json
import requests
from django.urls import reverse
from django.shortcuts import render, redirect
from hork.api.Nova_API import *

# 获取flavor的信息
def get_flavor(project_token):
    url = "http://192.168.217.12:8774/v2.1/flavors"
    headers={}
    headers['X-Auth-Token'] = project_token
    resp = requests.get(url,headers=headers)
    flavorsl_json = resp.json()
    return flavorsl_json

# 获取flavor的详细信息
def info_flavor(project_token,flavor_id):
    url="http://192.168.217.12:8774/v2.1/flavors/%s"%(flavor_id)
    headers={}
    headers['X-Auth-Token'] = project_token
    resp=requests.get(url,headers=headers)
    return resp

# 显示flavor详细信息
def fla_info(request):
    flalist = []
    flavor_json_list = get_flavor(project_token)
    get_flavor_list = flavor_json_list.get('flavors')
    for i in get_flavor_list:
        flavor_id = i.get('id')
        info_project_list = info_flavor(project_token,flavor_id)
        flavorinfo = info_project_list.json()['flavor']
        
        # flavorinfo['Temporary_disk']=flavorinfo.pop('OS-FLV-EXT-DATA:ephemeral')
        
        # flavorinfo.update({'Temporary_disk':flavorinfo.pop('OS-FLV-EXT-DATA:ephemeral')})
        
        flavorinfo['Temporary_disk']=flavorinfo['OS-FLV-EXT-DATA:ephemeral']
        del flavorinfo['OS-FLV-EXT-DATA:ephemeral']
        
        flavorinfo['is_public']=flavorinfo['os-flavor-access:is_public']
        del flavorinfo['os-flavor-access:is_public']
        
        print("flavors_info: ",flavorinfo)
        flalist.append(flavorinfo)
    return render(request, "flalist.html", {'flalist': flalist})

# 创建flavor
# def cre_fla(fla_name,fla_vcpu,fla_ram,fla_disk,fla_Temporary_disk,fla_swap,fla_rxtx):
def cre_fla(request):
    fla_name = request.POST.get("fla_name")
    fla_vcpu = request.POST.get("fla_vcpu")
    fla_ram = request.POST.get("fla_ram")
    fla_disk = request.POST.get("fla_disk")
    fla_Temporary_disk = request.POST.get("fla_Temporary_disk")
    fla_swap = request.POST.get("fla_swap")
    fla_rxtx = request.POST.get("fla_rxtx")
    url="http://192.168.217.12:8774/v2.75/flavors"
    data={
        "flavor": {
            "OS-FLV-DISABLED:disabled": False,
            "disk": fla_disk,
            "OS-FLV-EXT-DATA:ephemeral": fla_Temporary_disk,
            "os-flavor-access:is_public": True,
            # "id": "10",
            # "links": [
                # {
                    # "href": "http://openstack.example.com/v2/6f70656e737461636b20342065766572/flavors/10",
                    # "rel": "self"
                    # },
                # {
                    # "href": "http://openstack.example.com/6f70656e737461636b20342065766572/flavors/10",
                    # "rel": "bookmark"
                    # }
                # ],
            "name": fla_name,
            "ram": fla_ram,
            "swap": fla_swap,
            "rxtx_factor": fla_rxtx,
            "vcpus": fla_vcpu,
            # "description": "test description",
            "extra_specs": {}
            }
        }
    headers={}
    headers['X-Auth-Token'] = project_token
    resp =requests.post(url,data=json.dumps(data),headers=headers)
    return redirect('fla')
    # print('resp+++++++:', resp)
    # return resp    
# cre_fla("test",1,10,3,0,0,1.0)

#  更新flavor
def update_fla(request):
    flavor_id = request.POST.get("fla_id")
    user_name = request.POST.get("user_name")
    domain_token = request.session["domain_token"]
    user_description = request.POST.get("user_description")
    url="http://192.168.217.12:8774/v2.1/flavors/%s"%(flavor_id)
    data={
        "user": {
            "name": user_name,
            "description": user_description,
            }
        }
    headers={}
    headers['X-Auth-Token'] = project_token
    resp_update = requests.put(url,data=json.dumps(data),headers=headers)
    # print(resp_update)
    # return resp_update
    return redirect('fla')
# flavor_id="37151b25161343d99c0fab515dc28a80"
# user_name="user0312"
# user_description="My test user"
# update_fla(domain_token,flavor_id,user_name,user_description)

# 删除flavor
def del_fla(request):
    domain_token = request.session["domain_token"]
    flavor_id = request.POST.get("fla_id")
    url="http://192.168.217.12:8774/v2.1/flavors/%s"%(flavor_id)
    headers={}
    headers['X-Auth-Token'] = project_token
    resp_del = requests.delete(url,headers=headers)
    return redirect('fla')
    # print(resp_del)
    # return resp_del
# flavor_id="e10405c481324e4382da3f1d0baed9c0"
# del_project(domain_token,flavor_id)

# 列出可用flavor
def flavor_list(request):
    url = "http://192.168.217.12:8774/v2.1/flavors"
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.get(url, headers=headers)
    flavorsl_json = result.json()
    flalist = []
    flalen = 0
    for s in flavorsl_json['flavors']:
        # flalist.append(s)
        flalen += 1
        print(flalen)
        
    for i in range(1,flalen+1):
        print(i)
        url1 = "http://192.168.217.12:8774/v2.1/flavors/%s" %i
        headers = {}
        headers["X-Auth-Token"] = project_token
        result1 = requests.get(url1, headers=headers)
        flavorsinfo_json = result1.json()
        flavorinfo = flavorsinfo_json['flavor']
        
        # flavorinfo['Temporary_disk']=flavorinfo.pop('OS-FLV-EXT-DATA:ephemeral')
        
        # flavorinfo.update({'Temporary_disk':flavorinfo.pop('OS-FLV-EXT-DATA:ephemeral')})
        
        flavorinfo['Temporary_disk']=flavorinfo['OS-FLV-EXT-DATA:ephemeral']
        del flavorinfo['OS-FLV-EXT-DATA:ephemeral']
        
        flavorinfo['is_public']=flavorinfo['os-flavor-access:is_public']
        del flavorinfo['os-flavor-access:is_public']
        
        print("flavors_info: ",flavorinfo)
        flalist.append(flavorinfo)
    # for a in flavorinfo:
        # flalist.append(a)
        # print("aa:",a)
    return render(request, "flalist.html", {'flalist': flalist})
    # return result,flalist
# res = images_list()
# print(res)
# print("列出映像images(json)：",res[0].json())
# print("列出映像images：",res[1])
# res = flavor_list()
# print(res)
# print("列出flavor: ",res[0].json())