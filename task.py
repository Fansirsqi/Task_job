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


def do_task(COOKIE_CONFIG: dict):
    url1 = "https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA=="
    url2 = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F'
    url3 = 'https://www.52pojie.cn/home.php?mod=task&do=draw&id=2'
    for user_name, cookie in COOKIE_CONFIG.items():
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
            print("第{count}cookie中未包含htVC_2132_saltkey或htVC_2132_auth字段，请检查cookie")
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
        try:
            print('🚲开始执行')
            r = requests.get(url1, headers=headers, allow_redirects=False)
            s_cookie = r.headers['Set-Cookie']
            cookie = cookie + s_cookie
            headers['Cookie'] = cookie
        except requests.exceptions.RequestException as e:
            print(e)
        try:
            print('🏍️开始执行')
            r = requests.get(url2, headers=headers, allow_redirects=False)
            s_cookie = r.headers['Set-Cookie']
            cookie = cookie + s_cookie
            headers['Cookie'] = cookie
        except requests.exceptions.RequestException as e:
            print(e)
        try:
            print('🚀开始执行')
            r = requests.get(url3, headers=headers)
            r_data = BeautifulSoup(r.text, "html.parser")
            jx_data = r_data.find("div", id="messagetext").find("p").text
            print(jx_data)
            if "您需要先登录才能继续本操作" in jx_data:
                print(f"🔴账号:{user_name}  Cookie 失效")
                message = f" 账号:{user_name}  🔴Cookie 失效\n"
            elif "恭喜" in jx_data:
                print(f"🟢账号:{user_name}  签到成功")
                message = f" 账号:{user_name}  🟢签到成功\n"
            elif "不是进行中的任务" in jx_data:
                print(f"🟡账号:{user_name}  今日已签到")
                message = f" 账号:{user_name}  🟡今日已签到\n"
            else:
                print(f"🔴账号:{user_name}  签到失败")
                message = f" 账号:{user_name}  🔴签到失败\n"
            return message
        except requests.exceptions.RequestException as e:
            print(e)


def server_chan(sendkey, title, context):
    data = {
        "title": title,
        "desp": context,
        "short": "",
        "channel": "9"
    }
    # 动态指定本次推送使用的消息通道，选填。如不指定，
    # 则使用网站上的消息通道页面设置的通道。
    # 支持最多两个通道，多个通道值用竖线|隔开。
    # 比如，同时发送服务号和企业微信应用消息通道，则使用 9|66 。
    # 通道对应的值如下：
    # 方糖服务号=9
    # 企业微信应用消息=66
    # Bark iOS=8
    # 企业微信群机器人=1
    # 钉钉群机器人=2
    # 飞书群机器人=3
    # 测试号=0
    # 自定义=88
    # PushDeer=18
    # 官方Android版·β=98
    headers = {
        'Content-type': 'application/json'
    }
    url = f'https://sctapi.ftqq.com/{sendkey}.send'
    while True:
        try:
            r = requests.post(url=url, headers=headers, json=data).json()
            print(f"🎁ServerChan推送结果:{r['data']['error']}")
            # 一般返回 SUCCESS 就是成功了
            # pushid = r['data']['pushid']
            # readkey = r['data']['readkey']
            # print(f'查询推送结果请访问: https://sctapi.ftqq.com/push?id={pushid}&readkey={readkey}')
            break
        except requests.exceptions.ConnectionError as e:
            print(f'ConnectionError:{e}')


def wx_pusher(wxpuser_token, uids, msg):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = json.dumps({
        "appToken": f"{wxpuser_token}",
        "content": f"##{msg}",
        "summary": f"{msg}",
        "contentType": 3,
        "uids": uids,
        "verifyPay": False
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json'
    }
    while True:
        try:
            r = requests.request("POST", url, headers=headers, data=payload).json()
            msg = r['msg']
            status = r['msg']['data'][0]['status']
            print(f'🎁 WxPusher {status} - {msg}')
            break
        except requests.exceptions.ConnectionError as e:
            print(f'ConnectionError:{e}')


def main():
    try:
        COOKIE_CONFIG = eval(os.environ.get("COOKIE_CONFIG"))
        re_back = do_task(COOKIE_CONFIG)
        try:
            SENDKEY = os.getenv('SENDKEY')
            server_chan(SENDKEY, "Task_job 签到反馈", '##' + re_back)
        except Exception as server_err:
            msg = f'🔴SERVER酱推送失败{server_err}'
            print(msg)
        try:
            WX_TOKEN = os.getenv('WX_TOKEN')
            UIDS = os.getenv('UIDS').split(',')  # UID 用‘，’分割
            wx_pusher(WX_TOKEN, UIDS, re_back)
        except Exception as wx_puser_err:
            msg = f'🔴WX_PUSHER推送报错: {wx_puser_err}'
            print(msg)
    except KeyError as wuai_err:
        msg = f'🔴吾爱Token 环境变量获取错误：{wuai_err}'
        print(msg)
        return msg


if __name__ == '__main__':
    main()
