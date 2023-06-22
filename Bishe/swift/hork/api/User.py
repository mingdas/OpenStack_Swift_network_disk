import sys
import json
import requests
from django.shortcuts import render, redirect
from django.urls import reverse


# 获取用户的信息
def get_user(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/users"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    user_json_list = resp.json()
    # print("user_json_list: ",user_json_list)
    # get_user_list = user_json_list.get('users')
    # for i in get_user_list:
    #     print(i)
    #     print(i.get('domain_id'))
    # return resp
    return user_json_list
    # return redirect('hork:pro')


# user_res = get_user(token)
# user_json_list=user_res.json()
# print("user_json_list: ",user_json_list)
# get_user_list = user_json_list.get('users')
# for i in get_user_list:
#     print(i)
#     print(i.get('domain_id'))


# 获取domain的详细信息
def domain_info(request, domain_id):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/domains/%s" % (domain_id)
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    return resp


# doinfo = []
# userinfo = []
# for i in get_user_list:
# domain_id = i.get('domain_id')
# print("domain_id: ",domain_id)
# domain_info_list = domain_info(token,domain_id)
# print("domain_info: ",domain_info_list.json())
# domain_info_result=domain_info_list.json().get('domain')
# print(domain_info_result.get('name'))
# do_info = domain_info_list.json()['domain']
# print("do_info:", do_info)
# doinfo.append(do_info)


# 列出某一个用户的信息
def info_user(token, user_id):
    url = "http://192.168.217.12:5000/v3/users/%s" % (user_id)
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    return resp


# for i in get_user_list:
# user_id = i.get('id')
# print("id: ",id)
# info_user_list = info_user(token,user_id)
# print("info_user: ",info_user_list.json()['user'])
# usr_info = info_user_list.json()['user']
# userinfo.append(usr_info)
# user_id='37151b25161343d99c0fab515dc28a80'
# resu = info_user(token, user_id)
# print(resu.json())


# 显示用户详细信息
def dousr_info(request):
    username = request.session['username']
    user_project_id = request.session['user_project_id']
    if username == 'admin' and user_project_id == '76411f617a23498689d108a5fb71a24d':
        token = request.session["token"]
        userinfo = []
        # user_res = get_user(request)
        # user_json_list = user_res.json()
        user_json_list = get_user(request)
        get_user_list = user_json_list.get('users')
        print("get_user_list   用户:   ", user_json_list, '\n')
        for i in get_user_list:
            user_id = i.get('id')
            info_user_list = info_user(token, user_id)
            usr_info = info_user_list.json()['user']
            usr_info['domain_name'] = 'default'
            userinfo.append(usr_info)
        return render(request, "user.html", {'userinfo': userinfo})
    else:
        return render(request, "user_user.html")

# # 显示用户详细信息
# def dousr_info(request):
#     token = request.session["token"]
#     doinfo = []
#     userinfo = []
#     user_res = get_user(request)
#     user_json_list=user_res.json()
#     get_user_list = user_json_list.get('users')
#     for i in get_user_list:
#         domain_id = i.get('domain_id')
#         domain_info_list = domain_info(request,domain_id)
#         domain_info_result=domain_info_list.json().get('domain')
#         do_info = domain_info_list.json()['domain']
#         doinfo.append(do_info)
#         # print("doinfo+++----+++:   ", doinfo)
#     for i in get_user_list:
#         user_id = i.get('id')
#         info_user_list = info_user(token,user_id)
#         usr_info = info_user_list.json()['user']
#         userinfo.append(usr_info)
#         # print("userinfo+++----+++:   ", userinfo)
#     # return redirect('hork:pro')
#     return render(request, "user.html", {'dousr': [{'do': t[0], 'usr': t[1]} for t in zip(doinfo, userinfo)]})


# 创建用户
def cre_user(request):
    user_name = request.POST.get("user_name")
    user_password = request.POST.get("user_password")
    user_description = request.POST.get("user_description")
    token = request.session["token"]
    url = "http://192.168.217.12:5000/v3/users"
    data = {
        "user": {
            # "default_project_id": "dea2d2aace1648eabbfc13f403fefb7e",
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
    headers = {'X-Auth-Token': token}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('hork:usr')
    # print(resp)
    # return resp


# cre_user("user0312","test user")


#  编辑用户
def update_user(request):
    user_id = request.POST.get("user_id")
    user_name = request.POST.get("user_name")
    token = request.session["token"]
    user_description = request.POST.get("user_description")
    url = "http://192.168.217.12:5000/v3/users/%s" % (user_id)
    data = {
        "user": {
            "name": user_name,
            "description": user_description,
        }
    }
    headers = {'X-Auth-Token': token}
    resp_update = requests.patch(url, data=json.dumps(data), headers=headers)
    return redirect('hork:usr')


# 删除用户
def del_user(request):
    token = request.session["token"]
    user_id = request.POST.get("user_id")
    url = "http://192.168.217.12:5000/v3/users/%s" % (user_id)
    headers = {}
    headers['X-Auth-Token'] = token
    resp_del = requests.delete(url, headers=headers)
    return redirect('hork:usr')


#  admin更改用户密码
def update_pwd(request):
    user_id = request.POST.get("user_id")
    password = request.POST.get("password")
    token = request.session["token"]
    new_password = request.POST.get("new_password")
    url = "http://192.168.217.12:5000/v3/users/%s/password" % (user_id)
    data = {
        "user": {
            "password": new_password,
            "original_password": password,
        }
    }
    headers = {'X-Auth-Token': token}
    resp_update = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('hork:usr')

# 跳转更改密码页面
def setu(request):
    return render(request, "user_user.html")

# 用户更改密码
def update_user_pwd(request):
    username = request.session['username']
    user_id = request.session['user_id']
    password = request.POST.get("password")
    token = request.session["token"]
    new_password = request.POST.get("new_password")
    url = "http://192.168.217.12:5000/v3/users/%s/password" % (user_id)
    data = {
        "user": {
            "password": new_password,
            "original_password": password,
        }
    }
    headers = {'X-Auth-Token': token}
    resp_update = requests.post(url, data=json.dumps(data), headers=headers)
    request.session.clear()  # 删除session里的全部内容
    return redirect('hork:login')

# # 列出凭据
# def get_cred(request):
#     token = request.session["token"]
#     user_id = "54a47b966cdf447d8766292132cc5b5e"
#     # user_id = request.POST.get("user_id")
#     url="http://192.168.217.12:5000/v3/users/%s/application_credentials"%(user_id)
#     headers = {'X-Auth-Token': token}
#     resp = requests.get(url,headers=headers)
#     print("cred*-*-*-*-*-:   ", resp.json())
#     return redirect('hork:usr')


# 创建凭据
def cre_cred(request):
    token = request.session["token"]
    user_id = request.POST.get("user_id")
    url = "http://192.168.217.12:5000/v3/credentials"
    data = {
        "credential": {
            "blob": "{\"access\":\"181920\",\"secret\":\"secretKey\"}",
            "project_id": "dea2d2aace1648eabbfc13f403fefb7e",
            "type": "ec2",  # 凭证类型
            # "type": "cert",
            "user_id": "e8f9ad8a545d42759cd4830ee1f12f20"
        }
    }
    headers = {'X-Auth-Token': token}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    print("Create credential:  ", resp)
    return redirect('hork:usr')

# 列出角色
def get_role(request):
    token = request.session["token"]
    url="http://192.168.217.12:5000/v3/roles"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url,headers=headers)
    resp_json = resp.json()
    roles = resp_json['roles']
    for i in roles:
        if i['name'] == 'admin':
            admin_role_id = i['id']
            request.session['admin_role_id'] = admin_role_id
        elif i['name'] == 'user':
            user_role_id = i['id']
            request.session['user_role_id'] = user_role_id
        else:
            return
    return resp


# 列出项目上用户的角色分配
def get_pro_usr_role(request):
    token = request.session["token"]
    # project_id = request.session['user_project_id']
    project_id = 'c0322f2c22614f6fa26773420728c710'
    user_id = request.session['user_id']
    # user_id = request.POST.get("user_id")
    url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles"%(project_id, user_id)
    headers = {'X-Auth-Token': token}
    resp = requests.get(url,headers=headers)
    print("\n项目上用户的角色分配   ", resp.json())
    return redirect('hork:pro')

# 为项目中的用户分配admin角色
def put_pro_usr_admin_role(request):
    token = request.session["token"]
    project_id = request.session['user_project_id']
    admin_role_id = request.session['admin_role_id']
    # project_id = 'c0322f2c22614f6fa26773420728c710'
    user_id = request.session['user_id']
    # user_id = request.POST.get("user_id")
    url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, admin_role_id)
    headers = {'X-Auth-Token': token}
    resp = requests.put(url,headers=headers)
    print("\n为项目中的用户分配角色 :   ", resp.json())
    return redirect('hork:pro')

# 为项目中的用户分配user角色
def put_pro_usr_user_role(request):
    get_role(request)
    token = request.session["token"]
    # project_id = request.session['user_project_id']
    user_role_id = request.session['admin_role_id']
    print("\n今年的春天user_role_id :   ", user_role_id)
    project_id = 'c0322f2c22614f6fa26773420728c710'
    user_id = request.session['user_id']
    # user_id = request.POST.get("user_id")
    url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, user_role_id)
    headers = {'X-Auth-Token': token}
    resp = requests.put(url,headers=headers)
    return redirect('hork:pro')