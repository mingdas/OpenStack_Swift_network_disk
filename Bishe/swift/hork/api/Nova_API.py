import sys
import json
import requests
from django.shortcuts import render, redirect
from hotk.api.swift_API import *
from hork.api.Flavor_API import *

# 获取domain范围token
# def get_domain_token():
    # data = { 
        # "auth": {
            # "identity": {
                # "methods": ["password"],
                # "password": {
                    # "user": {
                        # "name": "admin",
                        # "domain": {
                            # "name":"default"
                        # },  
                        # "password": "ADMIN"
                    # }
                # }   
            # },
            # "scope": {
                # "domain": {
                    # "name":"default"
                # }
            # }
        # }
    # }
    # url = "http://192.168.217.12:5000/v3/auth/tokens"
    # result = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    # # 返回的token在 response header 里面
    # return result
domain = "default"
username = "admin"
password = "1234"
domain_resp = get_v3_token(domain, username, password)
domain_token=domain_resp.headers.get("X-Subject-Token")
print("domain_token:",domain_token)

# 获取project范围token
def get_project_token(domain_token):
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": domain_token
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
    url = "http://192.168.217.12:5000/v3/auth/tokens"
    result = requests.post(url, data=json.dumps(data)).headers.get("X-Subject-Token")
    # 返回的token在 response header 里面
    return result

project_token = get_project_token(domain_token)
print("projeect_token: ",project_token)

# 列出servers
def servers_list():
    url = "http://192.168.217.12:8774/v2.1/servers"
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.get(url, headers=headers)
    serversl_json = result.json()
    # serlist = []
    # for i in serversl_json['servers']:
        # a = i['name']
        # serlist.append(a)
        # print(a)
    # return render(request, "serlist.html", {'serlist': serlist})
    return serversl_json
    # return result,serlist
# res = servers_list()
# print(res)
# print("列出实例servers：",res[0].json())
# print("列出实例servers：",res[1])

# 实例
def seim_list(request):
    url = "http://192.168.217.12:8774/v2.1/servers"
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.get(url, headers=headers)
    serversl_json = result.json()
    serlist = []
    print("serversl_json: ",serversl_json)
    for i in serversl_json['servers']:
        a = i['name']
        serlist.append(a)
        print("iiiii: ",i)
    url1 = "http://192.168.217.12:9292/v2/images"
    result1 = requests.get(url1, headers=headers)
    imagesl_json = result1.json()
    imalist = []
    for s in imagesl_json['images']:
        imalist.append(s)
        print("sssss: ", s)
    return render(request, "serlist.html", {'seimlist': [{'ser': t[0], 'ima': t[1]} for t in zip(serlist, imalist)]})
# 创建实例分为以下几个步骤：1.请求返回可用的镜像 2.返回可用的flavor 3.创建实例

def ser_info(request):
    serlist = []
    server_json_list = servers_list()
    get_server_list = server_json_list.get('servers')
    for i in get_server_list:
        server_id = i.get('id')
        info_server_list = servers_info(server_id)
        serverinfo = info_server_list.json()['server']
        serverinfo['availability_zone']=serverinfo.pop('OS-EXT-AZ:availability_zone')
        serverinfo['vm_state']=serverinfo.pop('OS-EXT-STS:vm_state')
        
        serverinfo['image_name'] = info_image(serverinfo['image']['id']).json()['name']
        serverinfo['ip_addr'] = serverinfo['addresses']['tse'][0]['addr']
        serverinfo['flavor'] = info_flavor(project_token,serverinfo['flavor']['id']).json()['flavor']['name']
        
        serlist.append(serverinfo)
    return render(request, "serlist.html", {'serlist': serlist})

# 获取image的信息
def get_image():
    url = "http://192.168.217.12:9292/v2/images"
    headers={}
    headers['X-Auth-Token'] = project_token
    resp = requests.get(url,headers=headers)
    image_json = resp.json()
    return image_json

# 获取image的详细信息
def info_image(image_id):
    url="http://192.168.217.12:9292/v2/images/%s"%(image_id)
    headers={}
    headers['X-Auth-Token'] = project_token
    resp=requests.get(url,headers=headers)
    return resp

# 显示image的详细信息
def ima_info(request):
    imalist = []
    image_json_list = get_image()
    get_image_list = image_json_list.get('images')
    for i in get_image_list:
        image_id = i.get('id')
        info_image_list = info_image(image_id)
        imageinfo = info_image_list.json()
        imalist.append(imageinfo)
    return render(request, "imalist.html", {'imalist': imalist})
# 创建实例

# 创建servers
def servers_create(request):
    ser_name = request.POST.get("ser_name")
    url = "http://192.168.217.12:8774/v2.1/servers"
    data = {
        "server": {
            "name": ser_name,
            "imageRef": "db943562-4457-442f-b0f3-527f75d1523e",
            "flavorRef": "http://192.168.217.12:8774/v2.1/flavors/1"
        }
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_create()
# print(res)
# print(res.json())

# 显示servers详细信息
def servers_info(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s"%(server_id)
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.get(url, headers=headers)
    return result

# res = servers_info("d5673ea6-50d5-4e3c-b955-b6fe6ee6c212")
# print(res)
# print("servers_info: ",res.json())

# 删除servers
def servers_del(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s"%(server_id)
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.delete(url, headers=headers)
    return redirect('ser')

# res = servers_del()
# print(res)

# 启动servers
def servers_start(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "os-start" : 'null'
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_start()
# print(res)

# 重新启动servers
def servers_reboot(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "reboot" : {
            "type" : "HARD"
        }
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_reboot()
# print(res)

# 暂停servers
def servers_pause(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "pause": 'null'
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_pause()
# print(res)

# 取消暂停的servers
def servers_unpause(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "unpause": 'null'
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_unpause()
# print(res)

# 挂起servers
def servers_suspend(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "suspend": 'null'
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_suspend()
# print(res)

# 恢复挂起的servers
def servers_resume_suspended(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "resume": 'null'
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_resume_suspended()
# print(res)

# 创建servers的快照
def servers_snapshot(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "createImage" : {
            "name" : "foo-image"
        }
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_snapshot()
# print(res)

# 关闭servers
def servers_stop(server_id):
    url = "http://192.168.217.12:8774/v2.1/servers/%s/action"%(server_id)
    data = {
        "os-stop" : 'null'
    }
    headers = {}
    headers["X-Auth-Token"] = project_token
    result = requests.post(url, data=json.dumps(data), headers=headers)
    return redirect('ser')

# res = servers_stop()
# print(res)