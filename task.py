# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: task.py(吾爱破解签到)-企业微信机器人通知
Author: Mrzqd-byseven
Date: 2023/2/4 08:00
cron: 30 7 * * *
new Env('吾爱破解签到');
"""
import os
import urllib.parse
from notify import send
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def do_task(COOKIE_CONFIG: dict):
    """执行签到
    Args:
        COOKIE_CONFIG (dict): _cookies:字典文件,{'自定义名称1':cookie1,'自定义名称2':cookie2}_
    Returns:
        _type_: _description_
    """
    url1 = "https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA=="
    url2 = "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F"
    url3 = "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2"
    count = 0
    logs = "=======>PUSH log<======="
    for user_name, cookie in COOKIE_CONFIG.items():
        cookie = urllib.parse.unquote(cookie)
        cookie_list = cookie.split(";")
        cookie = ""
        count += 1
        for i in cookie_list:
            key = i.split("=")[0]
            if "htVC_2132_saltkey" in key:
                cookie += (
                    "htVC_2132_saltkey=" + urllib.parse.quote(i.split("=")[1]) + ";"
                )
            if "htVC_2132_auth" in key:
                cookie += "htVC_2132_auth=" + urllib.parse.quote(i.split("=")[1]) + ";"
        if "htVC_2132_saltkey" not in cookie and "htVC_2132_auth" not in cookie:
            log = f"第{count}cookie中未包含htVC_2132_saltkey或htVC_2132_auth字段,请检查cookie"
            logs += "\n" + log
            send(log, "cookie配置错误")
            break
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
            log = "🚲  开始执行,第一步"
            logs += "\n" + log
            print(log)
            r = requests.get(url1, headers=headers, allow_redirects=False)
            s_cookie = r.headers["Set-Cookie"]
            cookie = cookie + s_cookie
            headers["Cookie"] = cookie
        except requests.exceptions.RequestException as e:
            print(e)
        try:
            log = "🏍️  开始执行,第二步"
            logs += "\n" + log
            print(log)
            r = requests.get(url2, headers=headers, allow_redirects=False)
            s_cookie = r.headers["Set-Cookie"]
            cookie = cookie + s_cookie
            headers["Cookie"] = cookie
        except requests.exceptions.RequestException as e:
            print(e)
        try:
            log = "🚀 开始执行,第三步"
            logs += "\n" + log
            print(log)
            r = requests.get(url3, headers=headers)
            r_data = BeautifulSoup(r.text, "html.parser")
            jx_data = r_data.find("div", id="messagetext").find("p").text
            # print(jx_data) # 不是进行中的任务

            if "您需要先登录才能继续本操作" in jx_data:
                log = f"🔴账号:{user_name}  Cookie 失效"
                logs += "\n" + log
            elif "恭喜" in jx_data:
                log = f"🟢账号:{user_name}  签到成功"
                logs += "\n" + log
            elif "不是进行中的任务" in jx_data:
                log = f"🟡  账号:{user_name}  今日已签到"
                logs += "\n" + log
            else:
                log = f"🔴账号:{user_name}  签到失败"
                logs += "\n" + log
            logs += "\n" + "=======>PUSH log<======="
            return logs
        except requests.exceptions.RequestException as e:
            print(e)


def main():
    try:
        load_dotenv()
        COOKIE_CONFIG = eval(os.environ.get("COOKIE_CONFIG"))
        print(COOKIE_CONFIG)
        re_back = do_task(COOKIE_CONFIG)
        # print(re_back)
        send(re_back, "DEBUG")
    except KeyError as wuai_err:
        msg = f"🔴吾爱Token 环境变量获取错误：{wuai_err}"
        print(msg)
        return msg


if __name__ == "__main__":
    main()
