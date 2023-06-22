import json, requests
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import json

# from hork.views import *


# 获取可用的项目范围
def auth_project(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/auth/projects"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers).json()
    print("可用的项目范围：   ", resp, '\n')
    auth_pro = resp['projects']
    print("项目11111 :   ", auth_pro, '\n')
    return auth_pro


# 获取项目的信息
def get_project(request):
    url = "http://192.168.217.12:5000/v3/projects"
    token = request.session.get('token')
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    return resp


# 获取domain的详细信息
def domain_info(request, domain_id):
    url = "http://192.168.217.12:5000/v3/domains/%s" % (domain_id)
    token = request.session.get('token')
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    return resp


# 列出某一个项目的信息
def info_project(request, project_id):
    url = "http://192.168.217.12:5000/v3/projects/%s" % (project_id)
    token = request.session.get('token')
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    pro_info = resp_json['project']
    pro_info['domain_name'] = 'default'
    return pro_info


# 显示项目详细信息
def dopro_info(request):
    username = request.session['username']
    user_project_id = request.session['user_project_id']
    print("\n项目id:   ", user_project_id)
    proinfo = []
    if username == 'admin' and user_project_id == '76411f617a23498689d108a5fb71a24d':
        pro_res = get_project(request)
        pro_json_list = pro_res.json()
        get_pro_list = pro_json_list.get('projects')
        for i in get_pro_list:
            project_id = i.get('id')
            pro_info = info_project(request, project_id)
            # pro_info = info_project_list.json()['project']
            # pro_info['domain_name'] = 'default'
            # print("项目：   ",pro_info)
            proinfo.append(pro_info)
        # print("proinfo: ",proinfo)
        return render(request, "project.html", {'proinfo': proinfo})
    else:
        proinfo.append(info_project(request, user_project_id))
        return render(request, "project_user.html", {'proinfo': proinfo})


# # 显示项目详细信息
# def dopro_info(request):
#     domain_token = request.session["token"]
#     doinfo = []
#     proinfo = []
#     pro_res = get_project(request)
#     pro_json_list=pro_res.json()
#     # print("pro_json_list: ",pro_json_list)
#     get_pro_list = pro_json_list.get('projects')
#     for i in get_pro_list:
#         domain_id = i.get('domain_id')
#         # print("domain_id: ",domain_id)
#         domain_info_list = domain_info(request,domain_id)
#         # print("domain_info: ",domain_info_list.json())
#         # domain_info_result=domain_info_list.json().get('domain')
#         # print("domain_info_result.get name:  ", domain_info_result.get('name'))
#         do_info = domain_info_list.json()['domain']
#         doinfo.append(do_info)
#     for i in get_pro_list:
#         project_id = i.get('id')
#         # print("id: ",id)
#         info_project_list = info_project(request,project_id)
#         # print("info_project: ",info_project_list.json()['project'])
#         pro_info = info_project_list.json()['project']
#         proinfo.append(pro_info)
#     return render(request, "project.html", {'dopro': [{'do': t[0], 'pro': t[1]} for t in zip(doinfo, proinfo)]})


# 创建项目
def cre_project(request):
    project_name = request.POST.get("project_name")
    project_description = request.POST.get("project_description")
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/projects"
    data = {
        "project": {
            "description": project_description,
            "domain_id": "35e6c13205464420a9c07050223a946b",
            "enabled": True,
            "is_domain": False,
            "name": project_name,
        }
    }
    headers = {'X-Auth-Token': token}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('hork:pro')


#  更新项目
def update_project(request):
    project_id = request.POST.get("project_id")
    project_name = request.POST.get("project_name")
    token = request.session.get('token')
    project_description = request.POST.get("project_description")
    url = "http://192.168.217.12:5000/v3/projects/%s" % (project_id)
    data = {
        "project": {
            "description": project_description,
            "name": project_name
        }
    }
    headers = {'X-Auth-Token': token}
    resp_update = requests.patch(url, data=json.dumps(data), headers=headers)
    return redirect('hork:pro')


# 删除项目
def del_project(request):
    token = request.session.get('token')
    project_id = request.POST.get("project_id")
    url = "http://192.168.217.12:5000/v3/projects/%s" % (project_id)
    headers = {'X-Auth-Token': token}
    resp_del = requests.delete(url, headers=headers)
    return redirect('hork:pro')


# def get_info(request):
#     token = request.session.get('token')
#     url = "http://192.168.217.12:8080/info"
#     headers = {'X-Auth-Token': token}
#     resp = requests.get(url, headers=headers)
#     resp_json = resp.json()
#     print("resp***++++***:  ",resp)
#     print("resp_json+++++****++++:   ",resp_json)
#     # return resp_json
#     return redirect('hork:pro')


# def selecthtml(request):
    # return render(request, 'frtghb.html')
    # return render(request, 'select.html')
    return render(request, 'test.html')

# def get_options(request):
    # 模拟生成选项数据的过程，实际中可能是从数据库或其它 API 获取
    # options = [
    #     {'text': 'Option 1', 'value': 'option1'},
    #     {'text': 'Option 2', 'value': 'option2'},
    #     {'text': 'Option 3', 'value': 'option3'},
    # ]
    options = [
        {
            'id': 1,
            'value': 'A'
        },
        {
            'id': 2,
            'value': 'B'
        },
        {
            'id': 3,
            'value': 'C'
        },
    ]
    # 返回 JSON 格式的数据
    return HttpResponse(json.dumps(options), content_type='application/json')
    
# def get_data(request):
    # 模拟数据
    data = [
        {'value': '1', 'text': '选项1'},
        {'value': '2', 'text': '选项2'},
        {'value': '3', 'text': '选项3'},
    ]
    return JsonResponse(data, safe=False)

# def set_selected_value(request):
    if request.method == 'POST':
        selected_value = request.POST.get('selectedValue')
        # 将选中项存入session
        request.session['selectedValue'] = selected_value
        print("selected_value*-*-*-selected_value:   ", selected_value, '\n')
        return JsonResponse({'status': 'success'})
    else:
        return HttpResponse('请求方法错误！')
    
# def getData(request):
    data = [
        {'value': '1', 'text': '选项一'},
        {'value': '2', 'text': '选项二'},
        {'value': '3', 'text': '选项三'}
    ]
    return JsonResponse(data, safe=False)

# def setSession(request):
    selectedValue = request.GET.get('selectedValue')
    request.session['selectedValue'] = selectedValue
    print("selected_value*-*-*-selected_value:   ", selectedValue, '\n')
    return JsonResponse({'status': 'success'})

# def get_data1(request):
    data = [{'id': 1, 'name': '选项1'},
            {'id': 2, 'name': '选项2'},
            {'id': 3, 'name': '选项3'}]
    return JsonResponse(data, safe=False)
    
# def set_selected_id(request):
    if request.method == 'POST':
        selected_id = request.POST.get('selected_id')
        if selected_id:
            request.session['selected_id'] = selected_id
            print("selected_value*-*-*-selected_value:   ", selected_id, '\n')
            return JsonResponse({'success': True})
    # return HttpResponseBadRequest()
    return HttpResponse('请求方法错误！')
    
# def select1(request):
    selected_id = request.session.get('selected_id')
    return render(request, 'select1.html', {'selected_id': selected_id})