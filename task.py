# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: task.py(吾爱破解签到)-企业微信机器人通知
Author: Mrzqd-byseven
Date: 2023/2/4 08:00
cron: 30 7 * * *
new Env('吾爱破解签到');
"""
import json
import os
import sys
import urllib.parse

import requests
from bs4 import BeautifulSoup


def do_task():
    # 多cookie使用&分割
    try:
        cookies = os.environ.get("COOKIE")
    except KeyError as e:
        print(f"请在环境变量填写COOKIE的值{e}")
        sys.exit()
    url1 = "https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA=="
    url2 = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F'
    url3 = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
    for n, cookie in enumerate(cookies.split("&"), start=1):
        cookie = urllib.parse.unquote(cookie)
        cookie_list = cookie.split(";")
        cookie = ''
        for i in cookie_list:
            key = i.split("=")[0]
            if "htVC_2132_saltkey" in key:
                cookie += "htVC_2132_saltkey=" + \
                          urllib.parse.quote(i.split("=")[1]) + "; "
            if "htVC_2132_auth" in key:
                cookie += "htVC_2132_auth=" + \
                          urllib.parse.quote(i.split("=")[1]) + ";"

        if 'htVC_2132_saltkey' not in cookie and 'htVC_2132_auth' not in cookie:
            print("第{n}cookie中未包含htVC_2132_saltkey或htVC_2132_auth字段，请检查cookie")
            sys.exit()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        r = requests.get(url1, headers=headers, allow_redirects=False)
        s_cookie = r.headers['Set-Cookie']
        cookie = cookie + s_cookie
        headers['Cookie'] = cookie
        r = requests.get(url2, headers=headers, allow_redirects=False)
        s_cookie = r.headers['Set-Cookie']
        cookie = cookie + s_cookie
        headers['Cookie'] = cookie
        r = requests.get(url3, headers=headers)
        r_data = BeautifulSoup(r.text, "html.parser")
        jx_data = r_data.find("div", id="messagetext").find("p").text
        print(jx_data)
        if "您需要先登录才能继续本操作" in jx_data:
            print(f"第{n}个账号Cookie 失效")
            message = f"第{n}个账号Cookie 失效"
        elif "恭喜" in jx_data:
            print(f"第{n}个账号签到成功")
            message = f"第{n}个账号签到成功"
        elif "不是进行中的任务" in jx_data:
            print(f"第{n}个账号今日已签到")
            message = f"第{n}个账号今日已签到"
        else:
            print(f"第{n}个账号签到失败")
            message = f"第{n}个账号签到失败"
        return message


def send_to_wecom_text(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid='@all'):
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": text
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return False


def main():
    try:
        wecom_id = os.environ.get("wecom_id")
        AgentId = os.environ.get("AgentId")
        Secret = os.environ.get("Secret")
        reback = do_task()
        send_to_wecom_text(reback, wecom_id, AgentId, Secret)
    except KeyError as e:
        return f'环境变量获取错误：{e}'
