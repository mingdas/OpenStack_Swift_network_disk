import json, requests
from django.shortcuts import render, redirect
from django.contrib import messages
from hork.api.Project import *
from hork.api.Swift import *
from hork.api.User import *
from hork.api.Consumer import *


# 获取token（一）
def get_token(username, password, request):
    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "domain": {
                            "id": "35e6c13205464420a9c07050223a946b",
                            "name": "default"
                        },
                        "name": username,
                        "password": password
                    }
                }
            },
        }
    }
    url = 'http://192.168.217.12:35357/v3/auth/tokens'
    result = requests.post(url, data=json.dumps(data))
    print("result:   ++:  ", result.headers, '\n')
    if 'X-Subject-Token' in result.headers.keys():
        token = result.headers['X-Subject-Token']
        request.session['token'] = token
        return result
    else:
        print('密码错误')
    return result


# 登录验证
def login(request):  # login函数
    if request.method == "GET":  # 前端如果是get请求
        return render(request, 'login.html')  # 返回HTML页面。
    elif request.method == "POST":  # 前端如果是post请求
        username = request.POST.get("username")
        password = request.POST.get("password")
        domain_resp = get_token(username, password, request)
        if domain_resp.status_code == 201:
            request.session['username'] = username
            request.session['password'] = password
            token = request.session.get('token')
            print("session获取token:   ", token, '\n')
            get_cred(request)
            # get_objects_all(request)
            # return dousr_info(request)
            # return get_swift_counters(request)
            # return dousr_info(request)
            if username == 'admin':
                return render(request, "index.html")
            else:
                return render(request, "index_user.html")
        else:  # 如果用户名或者密码错误，返回登录页面
            message = "登录失败，账号或密码错误！"
            messages.success(request, message)
            return render(request, "login.html", {'message': message})
        
def index(request):
    return render(request, "index.html")


# 退出登陆
def logout(request):  # 撤销
    request.session.clear()  # 删除session里的全部内容
    return redirect('hork:login')


# 显示令牌信息
def get_cred(request):
    token = request.session["token"]
    url = "http://192.168.217.12:35357/v3/auth/tokens"
    headers = {'X-Auth-Token': token, 'X-Subject-Token': token}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    print("\n令牌信息:   ", resp_json, '\n')
    # user_project_id = resp_json['token']['project']['id']
    # print("cred*-*-*-*-*-:   ", user_project_id, '\n')
    # request.session['user_project_id'] = user_project_id
    request.session['user_id'] = resp_json['token']['user']['id']
    # return redirect('hork:usr')
    return resp_json


# 文件大小
# def size_get(num):
#     if num < 1024:
#         return str(num) + ' ' + 'B'
#     elif 1024 <= num < 1024**2:
#         x = round(num / 1024, 1)
#         return str(x) + ' ' + 'KB'
#     else:
#         x = round(num / (1024**2), 1)
#         return str(x) + ' ' + 'MB'


# 列出所有对象
def get_objects_all(request):
    objinfo = []
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    url = "http://192.168.217.12:8080/v1/AUTH_%s" % (user_project_id)
    headers = {'X-Auth-Token': request.session["token"]}
    con_json_list = requests.get(url, headers=headers, params=param).json()
    k = 0
    for i in con_json_list:
        container_name = i['name']
        url2 = "http://192.168.217.12:8080/v1/AUTH_%s/%s" % (user_project_id,
                                                             container_name)
        obj_json_list = requests.get(url2, headers=headers,
                                     params=param).json()
        for j in obj_json_list:
            j['acid'] = k + 1
            j['bytes'] = size_get(j['bytes'])
            objinfo.append(j)
            k += 1
        # objinfo.append(j)
    request.session['datas'] = objinfo
    print("objinfo843548351:   ", objinfo, '\n')
    return objinfo

# 获取可用的项目范围
def get_options(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/auth/projects"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers).json()
    print("可用的项目范围：   ", resp, '\n')
    auth_pro = resp['projects']
    request.session['auth_pro'] = auth_pro
    print("项目11111 :   ", auth_pro, '\n')
    # user_project_id = resp.json()['projects']['id']
    # print("项目id :   ", user_project_id, '\n')
    # request.session['user_project_id'] = user_project_id
    # 返回 JSON 格式的数据
    return HttpResponse(json.dumps(auth_pro), content_type='application/json')

# 获取前端ajax传递的数据，然后设置为session
def set_session(request):
    if request.method == 'POST':
        selected_value = request.POST.get('selected_value')
        if selected_value == None:
            auth_pro = request.session['auth_pro']
            selected_value = auth_pro[0]['id']
            # 将选中的值保存到 session 中
            request.session['user_project_id'] = selected_value
            print("\n项目id:   ", selected_value)
            get_en_token(request)
            get_objects_all(request)
            return HttpResponse(json.dumps({'success': True}),
                            content_type='application/json')
        else:
            # 将选中的值保存到 session 中
            request.session['user_project_id'] = selected_value
            print("selected_value*-*-*-selected_value:   ", selected_value, '\n')
            get_en_token(request)
            get_objects_all(request)
            return HttpResponse(json.dumps({'success': True}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}),
                            content_type='application/json')
    
# 获取token（二）
def get_en_token(request):
    username = request.session['username']
    password = request.session['password']
    user_project_id = request.session['user_project_id']
    data = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "domain": {
                            "name": "default"
                        },
                        "name": username,
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": "default"
                    },
                    "id": user_project_id
                }
            },
            "roles": [{
                "name": "user"
            }]
        }
    }
    url = 'http://192.168.217.12:35357/v3/auth/tokens'
    result = requests.post(url, data=json.dumps(data))
    print("result:   ++:  ", result.headers, '\n')
    if 'X-Subject-Token' in result.headers.keys():
        token = result.headers['X-Subject-Token']
        request.session['token'] = token
        return result
    else:
        print('密码错误')
    return result

# 项目用户管理
def prouseredit(request):
    project_id = request.POST.get('project_id')
    request.session['project_id'] = project_id
    pro_name = request.POST.get('pro_name')
    request.session['pro_name'] = pro_name
    get_role(request)
    return render(request, 'prouseredit.html')

# 为项目管理显示所有用户
def alluser(request):
    token = request.session["token"]
    url = "http://192.168.217.12:5000/v3/users"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    user_json_list = resp.json()
    # 返回 JSON 格式的数据
    return HttpResponse(json.dumps(user_json_list), content_type='application/json')

# 为项目管理显示当前项目中所拥有的用户及其角色
def prouser(request):
    token = request.session["token"]
    url = "http://192.168.217.12:5000/v3/users"
    headers = {'X-Auth-Token': token}
    resps = requests.get(url, headers=headers)
    user_json_list = resps.json()
    get_user_list = user_json_list.get('users')
    a = []
    for i in get_user_list:
        user_id = i.get('id')
        project_id = request.session.get('project_id')
        url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles"%(project_id, user_id)
        resp = requests.get(url,headers=headers)
        resp_json = resp.json()
        roles = resp_json['roles']
        if roles != []:
            result = {}
            for j in roles:
                i['role_name'] = j['name']
                for key, value in i.items():
                    if key in result:
                        if value not in result[key]:
                            result[key].append(value)
                    else:
                        result[key] = [value]
            a.append(result)
    userinfo = {"users": a}
    # 返回 JSON 格式的数据
    return HttpResponse(json.dumps(userinfo), content_type='application/json')

# 为项目中的用户分配admin角色
def put_admin_role(request):
    if request.method == 'POST':
        token = request.session["token"]
        project_id = request.session.get('project_id')
        admin_role_id = request.session['admin_role_id']
        user_id = request.POST.get("user_id")
        url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, admin_role_id)
        headers = {'X-Auth-Token': token}
        resp = requests.put(url,headers=headers)
        return HttpResponse(json.dumps({'success': True}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}),content_type='application/json')

# 为项目中的用户分配user角色
def put_user_role(request):
    if request.method == 'POST':
        token = request.session["token"]
        project_id = request.session.get('project_id')
        user_role_id = request.session['user_role_id']
        user_id = request.POST.get("user_id")
        url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, user_role_id)
        headers = {'X-Auth-Token': token}
        resp = requests.put(url,headers=headers)
        return HttpResponse(json.dumps({'success': True}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}),content_type='application/json')
    
# 取消为项目上的用户分配admin角色
def del_admin_role(request):
    if request.method == 'POST':
        token = request.session["token"]
        project_id = request.session.get('project_id')
        admin_role_id = request.session['admin_role_id']
        user_id = request.POST.get("user_id")
        url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, admin_role_id)
        headers = {'X-Auth-Token': token}
        resp = requests.delete(url,headers=headers)
        return HttpResponse(json.dumps({'success': True}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}),content_type='application/json')
    
# 取消为项目上的用户分配user角色
def del_user_role(request):
    if request.method == 'POST':
        token = request.session["token"]
        project_id = request.session.get('project_id')
        user_role_id = request.session['user_role_id']
        user_id = request.POST.get("user_id")
        url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, user_role_id)
        headers = {'X-Auth-Token': token}
        resp = requests.delete(url,headers=headers)
        return HttpResponse(json.dumps({'success': True}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}),content_type='application/json')
    
# 删除项目上的用户
def del_pro_user(request):
    if request.method == 'POST':
        token = request.session["token"]
        project_id = request.session.get('project_id')
        user_role_id = request.session['user_role_id']
        user_id = request.POST.get("user_id")
        url="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, user_role_id)
        headers = {'X-Auth-Token': token}
        resp = requests.delete(url,headers=headers)
        admin_role_id = request.session['admin_role_id']
        url1="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, admin_role_id)
        resp = requests.delete(url1,headers=headers)
        return HttpResponse(json.dumps({'success': True}),content_type='application/json')
    else:
        return HttpResponse(json.dumps({'success': False}),content_type='application/json')
    
# 注册用户（创建用户的同时为其创建一个同名的项目）
def register(request):
    user_name = request.POST.get("user_name")
    user_password = request.POST.get("user_password")
    user_description = request.POST.get("user_description")
    token = request.session["token"]
    headers = {'X-Auth-Token': token}
    url = "http://192.168.217.12:5000/v3/users"
    data = {
        "user": {
            "domain_id": "35e6c13205464420a9c07050223a946b",
            "enabled": True,
            "name": user_name,
            "password": user_password,
            "description": user_description,
            "options": {
                "ignore_password_expiry": True
            }
        }
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers)  # 创建用户
    url1 = "http://192.168.217.12:5000/v3/projects"
    data1 = {
        "project": {
            "description": user_description,
            "domain_id": "35e6c13205464420a9c07050223a946b",
            "enabled": True,
            "is_domain": False,
            "name": user_name,
        }
    }
    resp1 = requests.post(url1, data=json.dumps(data1), headers=headers)  # 创建项目

    url2 = "http://192.168.217.12:5000/v3/users"
    headers = {'X-Auth-Token': token}
    resp2 = requests.get(url2, headers=headers)  # 获取用户列表
    user_json_list = resp2.json()
    get_user_list = user_json_list.get('users')
    for i in get_user_list:
        if i['name'] == user_name:
            user_id = i.get('id')  # 获取创建的用户的用户ID

    pro_res = get_project(request)  # 获取项目列表
    pro_json_list = pro_res.json()
    get_pro_list = pro_json_list.get('projects')
    for i in get_pro_list:
        if i['name'] == user_name:
            project_id = i.get('id')  # 获取创建的项目的项目ID

    get_role(request)  # 获取角色列表
    user_role_id = request.session['user_role_id']  # 设置创建的用户的 role 为 user
    url3="http://192.168.217.12:5000/v3/projects/%s/users/%s/roles/%s"%(project_id, user_id, user_role_id)
    headers = {'X-Auth-Token': token}
    resp3 = requests.put(url3,headers=headers)  # 将创建的用户分配至创建的项目且 role 为 user
    return redirect('hork:usr')

def selecthtml(request):
    # return render(request, 'frtghb.html')
    # return render(request, 'select.html')
    return render(request, 'test.html')

def get_data(request):
    data = [
        {'name': 'Tom', 'age': 25, 'gender': 'Male'},
        {'name': 'Lucy', 'age': 18, 'gender': 'Female'},
        {'name': 'Jack', 'age': 30, 'gender': 'Male'},
    ]
    return render(request, 'test.html',{'data':data})
    return HttpResponse(json.dumps(data), content_type='application/json')