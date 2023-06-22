import sys
import json
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from hork.api.Nova_API import domain_token

# 获取用户的信息
def get_user(domain_token):
    url = "http://192.168.217.12:5000/v3/users"
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp = requests.get(url,headers=headers)
    return resp
 
# user_res = get_user(domain_token)
# user_json_list=user_res.json()
# print("user_json_list: ",user_json_list)
# get_user_list = user_json_list.get('users')
# for i in get_user_list:
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
# userinfo = []
# for i in get_user_list:
    # domain_id = i.get('domain_id')
    # print("domain_id: ",domain_id)
    # domain_info_list = domain_info(domain_token,domain_id)
    # print("domain_info: ",domain_info_list.json())
    # domain_info_result=domain_info_list.json().get('domain')
    # print(domain_info_result.get('name'))
    # do_info = domain_info_list.json()['domain']
    # print("do_info:", do_info)
    # doinfo.append(do_info)
    
# 列出某一个用户的信息
def info_user(domain_token,user_id):
    url="http://192.168.217.12:5000/v3/users/%s"%(user_id)
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp=requests.get(url,headers=headers)
    return resp

# for i in get_user_list:
    # user_id = i.get('id')
    # print("id: ",id)
    # info_project_list = info_user(domain_token,user_id)
    # print("info_user: ",info_project_list.json()['user'])
    # pro_info = info_project_list.json()['user']
    # userinfo.append(pro_info)
# user_id='37151b25161343d99c0fab515dc28a80'
# resu = info_user(domain_token, user_id)
# print(resu.json())

# 显示用户详细信息
def dousr_info(request):
    domain_token = request.session["domain_token"]
    doinfo = []
    userinfo = []
    user_res = get_user(domain_token)
    user_json_list=user_res.json()
    get_user_list = user_json_list.get('users')
    for i in get_user_list:
        domain_id = i.get('domain_id')
        domain_info_list = domain_info(domain_token,domain_id)
        domain_info_result=domain_info_list.json().get('domain')
        do_info = domain_info_list.json()['domain']
        doinfo.append(do_info)
    for i in get_user_list:
        user_id = i.get('id')
        info_project_list = info_user(domain_token,user_id)
        pro_info = info_project_list.json()['user']
        userinfo.append(pro_info)
    return render(request, "userlist.html", {'dousr': [{'do': t[0], 'usr': t[1]} for t in zip(doinfo, userinfo)]})

# 创建用户
def cre_user(request):
    user_name = request.POST.get("user_name")
    user_password = request.POST.get("user_password")
    user_description = request.POST.get("user_description")
    domain_token = request.session["domain_token"]
    url="http://192.168.217.12:5000/v3/users"
    data={
        "user": {
            # "default_project_id": "263fd9",
            "domain_id": "35e6c13205464420a9c07050223a946b",
            "enabled": True,
            # "federated": [
                # {
                    # "idp_id": "efbab5a6acad4d108fec6c63d9609d83",
                    # "protocols": [
                        # {
                            # "protocol_id": "mapped",
                            # "unique_id": "test@example.com"
                            # }
                        # ]
                    # }
                # ],
            "name": user_name,
            "password": user_password,
            "description": user_description,
            # "email": "jdoe@example.com",
            "options": {
                "ignore_password_expiry": True
                }
            }
        }
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp =requests.post(url,data=json.dumps(data),headers=headers)
    return redirect('usr')
    # print(resp)
    # return resp    
# cre_user("user0312","test user")

#  更新用户   
def update_user(request):
    user_id = request.POST.get("user_id")
    user_name = request.POST.get("user_name")
    domain_token = request.session["domain_token"]
    user_description = request.POST.get("user_description")
    url="http://192.168.217.12:5000/v3/users/%s"%(user_id)
    data={
        "user": {
            "name": user_name,
            "description": user_description,
            }
        }
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp_update = requests.patch(url,data=json.dumps(data),headers=headers)
    # print(resp_update)
    # return resp_update
    return redirect('usr')
# user_id="37151b25161343d99c0fab515dc28a80"
# user_name="user0312"
# user_description="My test user"
# update_user(domain_token,user_id,user_name,user_description)

# 删除用户
def del_user(request):
    domain_token = request.session["domain_token"]
    user_id = request.POST.get("user_id")
    url="http://192.168.217.12:5000/v3/users/%s"%(user_id)
    headers={}
    headers['X-Auth-Token'] = domain_token
    resp_del = requests.delete(url,headers=headers)
    return redirect('usr')
    # print(resp_del)
    # return resp_del
# user_id="e10405c481324e4382da3f1d0baed9c0"
# del_project(domain_token,user_id)