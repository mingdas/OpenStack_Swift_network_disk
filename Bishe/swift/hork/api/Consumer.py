import json, requests
from django.shortcuts import render, redirect


# 创建Consumer
def cre_cons(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/OS-OAUTH1/consumers"
    headers = {'X-Auth-Token': token}
    data = {"consumer": {"description": "My consumer"}}
    resp =requests.post(url,data=json.dumps(data), headers=headers)
    consumer_json_list = resp.json()
    print("consumer_json_list: ",consumer_json_list)
    return redirect('hork:usr')


# 创建Consumer
def get_cons(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/OS-OAUTH1/consumers"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    user_json_list = resp.json()


# 创建Consumer
def del_cons(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/OS-OAUTH1/consumers/1bc26954d7fd4e3ea41913b9b6d23371"
    headers = {'X-Auth-Token': token}
    resp = requests.delete(url, headers=headers)
    return redirect('hork:usr')


# 创建Consumer
def get_user(request):
    token = request.session.get('token')
    url = "http://192.168.217.12:5000/v3/OS-OAUTH1/consumers"
    headers = {'X-Auth-Token': token}
    resp = requests.get(url, headers=headers)
    user_json_list = resp.json()
