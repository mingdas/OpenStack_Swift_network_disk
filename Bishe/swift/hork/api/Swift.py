#coding:utf-8
import json,time,os

import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, FileResponse


# 文件大小
def size_get(num):
    if num < 1024:
        return str(num) + ' ' + 'B'
    elif 1024 <= num < 1024**2:
        x = round(num / 1024, 1)
        return str(x) + ' ' + 'KB'
    else:
        x = round(num / (1024**2), 1)
        return str(x) + ' ' + 'MB'

# 列出容器
def get_swift_counters(request):
    token = request.session.get('token')
    username = request.session['username']
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    print("token*-*-*-token:   ", token, '\n')
    print("user_project_id*-*-*-user_project_id:   ", user_project_id, '\n')
    url = "http://192.168.217.12:8080/v1/AUTH_%s" % (user_project_id)
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers, params=param)
    print("resp*-*-*-resp:   ", resp, '\n')
    respjson = resp.json()
    print("respjson*-*-*-respjson:   ", respjson, '\n')
    coninfo = []
    for i in respjson:
        i['bytes'] = size_get(i['bytes'])
        coninfo.append(i)
    # resp_json = ",".join(repr(e) for e in resp_json1)   # 去除列表[]中括号
    # return resp_json
    if username == 'admin':
        return render(request, "container.html", {'accounts_resp': coninfo})
    else:
        return render(request, "container_user.html",
                      {'accounts_resp': coninfo})


# 创建容器
def cre_conter(request):
    headers = {'X-Auth-Token': request.session["token"]}
    container_name = request.POST.get("container_name")
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s" % (user_project_id,
                                                        container_name)
    con = requests.put(url, headers=headers, params=param)
    return redirect('hork:con')


# 删除容器
def del_conter(request):
    headers = {'X-Auth-Token': request.session["token"]}
    container_name = request.POST.get("container_name")
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s" % (user_project_id,
                                                        container_name)
    con = requests.delete(url, headers=headers, params=param)
    return redirect('hork:con')


# 列出对象
def get_objects(request, count_name):
    username = request.session['username']
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s" % (user_project_id,
                                                        count_name)
    headers = {'X-Auth-Token': request.session["token"]}
    resp = requests.get(url, headers=headers, params=param).json()
    objinfo = []
    j = 0
    for i in resp:
        i['acid'] = j + 1
        i['bytes'] = size_get(i['bytes'])
        objinfo.append(i)
        j += 1
    request.session['container_name'] = count_name
    # print("objects:[;;;[[]]]  :  ", objinfo)
    if username == 'admin':
        return render(request, "object.html", {'objects_resp': objinfo})
    else:
        return render(request, "object_user.html", {'objects_resp': objinfo})


# # 列出文件夹内的对象
# def get_folder_objects(request,container_name,folder_name):
#     param = {'format': 'json'}
#     str_list = folder_name.rsplit('/', maxsplit=1)
#     if len(str_list) > 1:
#         result = str_list[0]
#         print("+56481+:  ",result)
#     else:
#         result = ''
#     url = "http://192.168.217.12:8080/v1/AUTH_76411f617a23498689d108a5fb71a24d/%s/%s" % (
#         container_name,result)
#     headers = {'X-Auth-Token': request.session["token"]}
#     resp = requests.get(url, headers=headers, params=param)
#     objects_resp = resp.json()
#     return render(request, "object.html", {'objects_resp': objects_resp})

# 删除对象
def del_obj(request):
    headers = {'X-Auth-Token': request.session["token"]}
    container_name = request.session['container_name']
    object_name = request.POST.get("object_name")
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    del_url = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s" % (
        user_project_id, container_name, object_name)
    del_obj = requests.delete(del_url, headers=headers, params=param)
    return get_objects(request, container_name)


# 创建文件夹
def cre_folder(request):
    headers = {'X-Auth-Token': request.session["token"]}
    container_name = request.session['container_name']
    folder_name = request.POST.get("folder_name")
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    str_list = folder_name.rsplit('/', maxsplit=1)
    if len(str_list) > 1:
        result = str_list[0]
    else:
        result = ''
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s" % (
        user_project_id, container_name, folder_name)
    url2 = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s" % (
        user_project_id, container_name, result)
    print("url111111:  ", url2)
    resp = requests.put(url, headers=headers, params=param)
    resp2 = requests.get(url2, headers=headers, params=param)
    objects_resp = resp2.json()
    print("++++++-----++++:  ", objects_resp)
    return render(request, "object.html", {'objects_resp': objects_resp})


def yulan(request, count_name, show_object):
    headers = {'X-Auth-Token': request.session["token"]}
    param = {'format': 'json'}
    user_project_id = request.session['user_project_id']
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s" % (
        user_project_id, count_name, show_object)
    resp = requests.get(url, headers=headers, params=param)
    resps = resp.text
    return HttpResponse(resps)


# 下载对象
# def download(request, down_object):
    headers = {'X-Auth-Token': request.session["token"]}
    user_project_id = request.session['user_project_id']
    container_name = request.session.get('container_name')
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s?format=json" % (
        user_project_id,container_name, down_object)
    resp = requests.get(url, headers=headers)
    resptext = resp.text
    down_file = "F:\\Pychrarm_objects\\swiftTqs\\file\\%s" % down_object
    # data = open('hork/static/upload/' + filename, 'wb')
    with open(down_file, 'w+') as f:
        f.write(resptext)
    return HttpResponse("<h1>下载成功！</h1>")

# 下载对象
def download(request, down_object):
    headers = {'X-Auth-Token': request.session["token"]}
    user_project_id = request.session['user_project_id']
    container_name = request.session.get('container_name')
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s?format=json" % (
        user_project_id,container_name, down_object)
    resp = requests.get(url, headers=headers)

    # resptext = resp.text
    # respcontent = resp.content
    # down_file = "hork/static/download/%s" % down_object
    # with open(down_file, 'wb') as f:
    #     f.write(respcontent)
    # file = open(down_file, 'rb')
    # # 如果as_attachment=True，则设置内容配置头，它要求浏览器将文件作为下载提供给用户。
    # response = FileResponse(file,as_attachment=True)
    # return HttpResponse("<h1>下载成功！</h1>")

    # 如果as_attachment=True，则设置内容配置头，它要求浏览器将文件作为下载提供给用户。
    response = FileResponse(resp,as_attachment=True)
    response['Content-Type']='application/octet-stream'  # 指定文件类型
    # response['Content-Disposition']='attachment;filename=music.mp3'  # 指定文件下载的名称
    return response

# def upload(request):
#     file = request.FILES.get('file',None)
#     print("file:   ",file)
#     if not file:
#         return HttpResponse("没有上传的文件信息")
#     # List.open(index) -- 可选参数，要移除列表元素的索引值，不能超过列表总长度，默认为 index=-1，删除最后一个列表值。
#     filename = str(time.time()) + '.' + file.name.split('.').pop()
#     print("file.name:   ",file.name)
#     print("file.name.split('.'):   ",file.name.split('.'))
#     data = open('hork/static/upload/' + filename, 'wb')
#     for chunk in file.chunks():
#         data.write(chunk)
#     data.close()
#     return HttpResponse("上传的文件")

# 上传对象
def upload(request):
    user_project_id = request.session['user_project_id']
    headers = {'X-Auth-Token': request.session["token"]}
    container_name = request.session.get('container_name')
    file = request.FILES.get('file',None)
    print("file:   ",file)
    if not file:
        return HttpResponse("没有上传的文件信息")
    filename = request.POST.get('filename')
    print("file.name:   ",file.name)
    print("file.name.split('.'):   ",file.name.split('.'))
    # data = open('hork/static/upload/' + filename, 'wb')
    data = open('settings.UPLOAD_DIRS' + filename, 'wb')
    for chunk in file.chunks():
        data.write(chunk)
    data.close()
    # data = open('D:/Bishe/swift/hork/static/upload/' + filename, 'rb')
    data = open('settings.UPLOAD_DIRS' + filename, 'rb')
    url = "http://192.168.217.12:8080/v1/AUTH_%s/%s/%s" % (user_project_id, container_name, filename)
    result = requests.put(url, headers=headers, data=data)
    return get_objects(request, container_name)


# 图片
def image(request):
    datas = request.session.get('datas')
    image = []
    for d in datas:
        names = d['name']
        type = ['png', 'jpg', 'jpeg']
        if '.' in names:
            s = names.split('.')
            # if s[1] == 'png' or s[1] == 'jpg' or s[1] == 'jpeg':
            if s[1] in type:
                image.append(d)
            else:
                pass
        else:
            pass
    return render(request, 'image.html', {'image': image})


# 文档
def txt(request):
    datas = request.session.get('datas')
    txt = []
    for d in datas:
        names = d['name']
        type = ['txt', 'docx', 'rtf', 'doc', 'pdf', 'xls', 'ppt', 'pptx', 'xlsx']
        if '.' in names:
            s = names.split('.')
            if s[1] in type:
                txt.append(d)
            else:
                pass
        else:
            pass
    print("txt   :   ",txt,'\n')
    return render(request, 'txt.html', {'txt': txt})


# 视频
def video(request):
    datas = request.session.get('datas')
    video = []
    for d in datas:
        names = d['name']
        type = [
            'avi', 'wmv', 'wmp', 'wm', 'asf', 'mpg', 'mpeg', 'mpe', 'm1v',
            'm2v', 'mpv2', 'mp2v', 'ts', 'tp', 'tpr', 'trp', 'vob', 'ifo',
            'ogm', 'ogv', 'mp4', 'm4v', 'm4p', 'm4b', '3gp', '3gpp', '3g2',
            '3gp2', 'mkv', 'rm', 'ram', 'rmvb'
        ]
        if '.' in names:
            s = names.split('.')
            if s[1] in type:
                video.append(d)
            else:
                pass
        else:
            pass
    return render(request, 'video.html', {'video': video})


# 音频
def music(request):
    datas = request.session.get('datas')
    music = []
    for d in datas:
        names = d['name']
        type = [
            'wav', 'wma', 'mpa', 'mp2', 'm1a', 'm2a', 'mp3', 'ogg', 'm4a',
            'aac', 'mka', 'ra', 'flac', 'ape', 'mpc', 'mod', 'ac3', 'eac3',
            'dts', 'dtshd', 'wv', 'tak', 'cda', 'dsf', 'tta', 'aiff', 'aif',
            'opus', 'amr'
        ]
        if '.' in names:
            s = names.split('.')
            if s[1] in type:
                music.append(d)
            else:
                pass
        else:
            pass
    return render(request, 'music.html', {'music': music})


# 未分类
def untype(request):
    datas = request.session.get('datas')
    untype = []
    for d in datas:
        names = d['name']
        if '.' not in names:
            untype.append(d)
        else:
            pass
    return render(request, 'untype.html', {'untype': untype})