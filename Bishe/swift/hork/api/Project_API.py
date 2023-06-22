import sys
import json
import requests
from hork.api.swift_API import *
from django.urls import reverse
# from werkzeug import responder

# 登录验证
def login(request):  # login函数
    if request.method == "GET":  # 前端如果是get请求
        return render(request, 'login.html')  # 返回HTML页面。
    elif request.method == "POST":  # 前端如果是post请求
        domain = "default"
        username = request.POST.get("username")
        password = request.POST.get("password")
        domain_resp = get_v3_token(domain, username, password)
        if domain_resp.status_code == 201:
            request.session["domain_token"] = domain_resp.headers.get("X-Subject-Token")
            accounts_resp = get_swift_counters(request.session["domain_token"])
            # domain_token=domain_resp.headers.get("X-Subject-Token")
            # accounts_resp=get_swift_counters(domain_token)
            domain_token = request.session["domain_token"]
            doinfo = []
            proinfo = []
            pro_res = get_project(domain_token)
            pro_json_list=pro_res.json()
            get_pro_list = pro_json_list.get('projects')
            for i in get_pro_list:
                domain_id = i.get('domain_id')
                domain_info_list = domain_info(domain_token,domain_id)
                domain_info_result=domain_info_list.json().get('domain')
                do_info = domain_info_list.json()['domain']
                doinfo.append(do_info)
            for i in get_pro_list:
                project_id = i.get('id')
                info_project_list = info_project(domain_token,project_id)
                pro_info = info_project_list.json()['project']
                proinfo.append(pro_info)
            request.session['username'] = username
            return render(request, "projectlist.html", {'dopro': [{'do': t[0], 'pro': t[1]} for t in zip(doinfo, proinfo)]})
        else:  # 如果用户名或者密码错误，返回登录页面
            message = "登录失败，域名、账号或密码错误！"
            return render(request, "login.html", {'message': message})
        
# 获取domain范围token
def get_domain_token():
    data = { 
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": "admin",
                        "domain": {
                            "name":"default"
                        },  
                        "password": "ADMIN"
                    }
                }   
            },
            "scope": {
                "domain": {
                    "name":"default"
                }
            }
        }
    }
    url = "http://192.168.217.12:5000/v3/auth/tokens"
    result = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    # 返回的token在 response header 里面
    return result
# domain_token = get_domain_token()
# print(domain_token)

# domain = "default"
# username = "admin"
# password = "1234"
# domain_resp = get_v3_token(domain, username, password)
# domain_token=domain_resp.headers.get("X-Subject-Token")
# print("domain_token:",domain_token)

# 获取项目的信息
def get_project(domain_token):
    url = "http://192.168.217.12:5000/v3/projects"
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp = requests.get(url,headers=headers)
    return resp
 
# pro_res = get_project()
# pro_json_list=pro_res.json()
# print("pro_json_list: ",pro_json_list) 
# get_pro_list = pro_json_list.get('projects')
# for i in get_pro_list:
    # print(i)
    # print(i.get('domain_id'))

# 获取domain的详细信息
def domain_info(domain_token,domain_id):
    url = "http://192.168.217.12:5000/v3/domains/%s"%(domain_id)
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp = requests.get(url,headers=headers)
    return resp
# doinfo = []
# proinfo = []
# for i in get_pro_list:
    # domain_id = i.get('domain_id')
    # print("domain_id: ",domain_id)
    # domain_info_list = domain_info(domain_token,domain_id)
    # print("domain_info: ",domain_info_list.json())
    # domain_info_result=domain_info_list.json().get('domain')
    # print(domain_info_result.get('name'))
    # do_info = domain_info_list.json()['domain']
    # doinfo.append(do_info)

# 列出某一个项目的信息
def info_project(domain_token,project_id):
    url="http://192.168.217.12:5000/v3/projects/%s"%(project_id)
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp=requests.get(url,headers=headers)
    return resp

# for i in get_pro_list:
    # project_id = i.get('id')
    # print("id: ",id)
    # info_project_list = info_project(domain_token,project_id)
    # print("info_project: ",info_project_list.json()['project'])
    # pro_info = info_project_list.json()['project']
    # proinfo.append(pro_info)
# project_id='76411f617a23498689d108a5fb71a24d'
# resu = info_project(domain_token, project_id)
# print(resu.json())

# 显示项目详细信息
def dopro_info(request):
    domain_token = request.session["domain_token"]
    doinfo = []
    proinfo = []
    pro_res = get_project(domain_token)
    pro_json_list=pro_res.json()
    # print("pro_json_list: ",pro_json_list) 
    get_pro_list = pro_json_list.get('projects')
    for i in get_pro_list:
        domain_id = i.get('domain_id')
        # print("domain_id: ",domain_id)
        domain_info_list = domain_info(domain_token,domain_id)
        # print("domain_info: ",domain_info_list.json())
        domain_info_result=domain_info_list.json().get('domain')
        # print(domain_info_result.get('name'))
        do_info = domain_info_list.json()['domain']
        doinfo.append(do_info)
    for i in get_pro_list:
        project_id = i.get('id')
        # print("id: ",id)
        info_project_list = info_project(domain_token,project_id)
        # print("info_project: ",info_project_list.json()['project'])
        pro_info = info_project_list.json()['project']
        proinfo.append(pro_info)
    return render(request, "projectlist.html", {'dopro': [{'do': t[0], 'pro': t[1]} for t in zip(doinfo, proinfo)]})

# 创建项目
def cre_project(request):
    project_name = request.POST.get("project_name")
    project_description = request.POST.get("project_description")
    domain_token = request.session["domain_token"]
    url="http://192.168.217.12:5000/v3/projects"
    data={
            "project": {
                "description": project_description,
                "domain_id": "35e6c13205464420a9c07050223a946b",
                "enabled": True,
                "is_domain": False,
                "name":project_name ,
            }
        }
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp =requests.post(url,data=json.dumps(data),headers=headers)
    return redirect('pro')
    # print(resp)
    # return resp    
# cre_project(domain_token,"myNewProject4271","My new project4271")

#  更新项目   
def update_project(request):
    project_id = request.POST.get("project_id")
    project_name = request.POST.get("project_name")
    domain_token = request.session["domain_token"]
    project_description = request.POST.get("project_description")
    url="http://192.168.217.12:5000/v3/projects/%s"%(project_id)
    data={
        "project": {
            "description":project_description,
            "name": project_name
        }
    }
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp_update = requests.patch(url,data=json.dumps(data),headers=headers)
    # print(resp_update)
    # return resp_update
    return redirect('pro')
# project_id="23c4f63067ba41b7b7fd2fc89be606c2"
# project_name="myUpdatedProject"
# project_description="My updated project"
# update_project(domain_token,project_id,project_name,project_description)
# update_project(domain_token,project_id,project_name,project_description)

# 删除项目
def del_project(request):
    domain_token = request.session["domain_token"]
    project_id = request.POST.get("project_id")
    url="http://192.168.217.12:5000/v3/projects/%s"%(project_id)
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp_del = requests.delete(url,headers=headers)
    return redirect('pro')
    # print(resp_del)
    # return resp_del
# project_id="e10405c481324e4382da3f1d0baed9c0"
# del_project(domain_token,project_id)