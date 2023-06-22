#coding:utf-8
import json

import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import FileResponse

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def get_v3_token(domain, username, password):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": domain
                        },
                        "name": username,
                        "password": password,
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "name": "admin"
                }
            }
        }
    }

    url = "http://192.168.217.12:35357/v3/auth/tokens"
    result = requests.post(url, data=json.dumps(data))
    print(result)
    return result
# domain = "default"
# username = "admin"
# password = "1234"
# domain_resp = get_v3_token(domain, username, password)
# domain_token=domain_resp.headers.get("X-Subject-Token")
# print(domain_token)

def get_swift_counters(domain_token):
    url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d?format=json"
    headers = {}
    headers["X-Auth-Token"] = domain_token
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    return resp_json


def get_swift_objects(domain_token, url):
    headers = {}
    headers["X-Auth-Token"] = domain_token
    obj = requests.get(url, headers=headers)
    obj_json = obj.json()
    return obj_json


def get_objects(request, count_name):
    url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s?format=json" % count_name
    accounts_obj = get_swift_objects(request.session["domain_token"], url)
    request.session['count_name'] = count_name
    return render(request, "objects.html", {'accounts_obj': accounts_obj})


def del_swift_obj(request, count_name, del_object):
    headers = {}
    headers["X-Auth-Token"] = request.session['domain_token']
    del_url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s/%s?format=json" % (
         count_name, del_object)
    del_obj = requests.delete(del_url,headers=headers)
    return HttpResponseRedirect("/login/%s"%(count_name))

def cre_conter(request):
    headers = {}
    headers["X-Auth-Token"] = request.session['domain_token']
    count_name = request.POST.get("cre_count")
    url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d?format=json"
    cre_url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s?format=json" %count_name
    cre_con = requests.put(cre_url,headers=headers)
    cre_get = requests.get(url,headers=headers)
    get = cre_get.json()
    return render(request, "list.html", {'accounts_resp': get})

def del_conter(request,delc_name):
    headers = {}
    headers["X-Auth-Token"] = request.session['domain_token']
    url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d?format=json"
    delc_url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s?format=json" %delc_name
    delc = requests.delete(delc_url,headers=headers)
    cre_get = requests.get(url, headers=headers)
    get = cre_get.json()
    return render(request, "list.html", {'accounts_resp': get})

def yulan(request,count_name,show_object):
    headers = {}
    headers["X-Auth-Token"] = request.session['domain_token']
    url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s/%s?format=json" % (
        count_name, show_object)
    resp = requests.get(url,headers=headers)
    resps = resp.text
    return HttpResponse(resps)


def upload(request,count_name):
    object = request.FILES.get('obj')
    object_name=object.name
    with open(object_name,'wb') as f:
        for files in object:
            f.write(files)
    data = open(object_name, 'r')
    print(data)
    headers = {}
    headers["X-Auth-Token"] = request.session['domain_token']
    url = "http://192.168.217.12:8080/v1/" \
          "AUTH_76411f617a23498689d108a5fb71a24d/%s/%s" %(
    count_name, object_name)
    up_obj = requests.put(url=url,headers=headers,data=data)
    return HttpResponseRedirect("/login/%s"%(count_name))
    # return HttpResponse(up_obj)

def download(request,count_name,down_object):
    headers = {}
    headers["X-Auth-Token"] = request.session['domain_token']
    url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s/%s?format=json" % (
        count_name, down_object)
    resp = requests.get(url,headers=headers)
    resps = resp.text
    down_file = "F:\\Pychrarm_objects\\swiftTqs\\file\\%s"%down_object
    with open(down_file,'w+') as f:
        f.write(resps)
    return HttpResponse("<h1>下载成功！</h1>")

'{"auth": {"identity": {"methods": ["password"],"password": {"user": {"domain": {"name": "Default"},"name": "admin","password": "devops"}}},"scope": {"project": {"domain": {"name": "Default"},"name": "admin"}}}}'

# def login(request):  # login函数
    # if request.method == "GET":  # 前端如果是get请求
        # return render(request, 'login.html')  # 返回HTML页面。
    # elif request.method == "POST":  # 前端如果是post请求
        # domain = "default"
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # domain_resp = get_v3_token(domain, username, password)
        # if domain_resp.status_code == 201:
            # request.session["domain_token"] = domain_resp.headers.get("X-Subject-Token")
            # accounts_resp = get_swift_counters(request.session["domain_token"])
            # domain_token=domain_resp.headers.get("X-Subject-Token")
            # # accounts_resp=get_swift_counters(domain_token)
            # request.session['username'] = username
            # request.session['ct_name'] = accounts_resp
            # return render(request, "list.html", {'accounts_resp': accounts_resp})
        # else:  # 如果用户名或者密码错误，返回登录页面
            # message = "登录失败，域名、账号或密码错误！"
            # return render(request, "login.html", {'message': message})


def logout(request):  # 撤销
    request.session.clear()  # 删除session里的全部内容
    return redirect('login')


def index(request):  # index函数
    return render(request, "index.html")


def list_c(request):
    li_c = request.session['ct_name']
    return render(request, "list.html", {'accounts_obj': li_c})


def shouye(request):
    if request.method == "GET":
        accounts_resp = get_swift_counters(request.session["domain_token"])
    return render(request, "list.html", {'accounts_resp': accounts_resp})

def test(request):
    data = {"auth": {"identity": {"methods": ["password"], "password": {
        "user": {"domain": {"name": "default"}, "name": "admin", "password": "1234", }}},
                     "scope": {"project": {"domain": {"name": "default"}, "name": "admin"}}}}
    url = "http://192.168.217.12:35357/v3/auth/tokens"
    result = requests.post(url, data=json.dumps(data))
    token = result.headers.get("X-Subject-Token")
    return HttpResponse(token)