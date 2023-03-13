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
import smtplib
import sys
import urllib.parse
from email.header import Header
from email.mime.text import MIMEText

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


class EmailAlerts:
    # 邮箱域名，这里用的QQ邮箱发送
    host = 'smtp.qq.com'
    # port = 25  #或者使用默认的端口号25
    # 发送者邮箱账号
    username = '2595741568@qq.com'
    # 授权码 注意，此处必须填写授权码，不同邮件的获取方法大体相同，参考百度。
    password = 'kagpnieqfgpoebag'
    # 接收者邮箱账号,多个接收者，构造list即可。
    to_addrs = ['2104898527@qq.com']

    @staticmethod
    def set_email_text(to_addrs: list, text: str, hder: str, sender: str):
        """
        :param to_addrs:收件人列表
        :param text: 正文
        :param hder: 邮件标题
        :param sender: 发件人
        """
        # 以下是构造证明，邮件主题、发送者姓名、接收者姓名等。
        msg = MIMEText(text, "plain", 'utf-8')
        msg['Subject'] = Header(hder)
        msg['From'] = Header(sender)  # 发件人
        msg['To'] = Header(','.join(to_addrs))
        return msg

    # 如需抄送，可使用Cc进行抄送
    # msg['Cc'] = Header(','.join(to_addrs))
    def send_email(self, msgx):
        # 创建SMTP对象
        server = smtplib.SMTP_SSL(self.host)
        # 设置发件人邮箱的域名和端口，端口地址为25
        server.connect(self.host, 465)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        server.login(self.username, self.password)
        try:
            print('开始发送')
            # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
            server.sendmail(self.username, self.to_addrs, msgx.as_string())
            print('邮件发送成功')
        except EOFError as error:
            print(error)
        # 关闭SMTP对象
        server.quit()


def main():
    obj = EmailAlerts()
    try:
        wecom_id = os.environ.get("WECOM_ID")
        AgentId = os.environ.get("AGENTID")
        Secret = os.environ.get("SECRET")
        emails = os.environ.get('EMAIL')
        reback = do_task()
        _msg = obj.set_email_text(to_addrs=[emails], text=reback, hder='Task_反馈',
                                  sender='签到机器人')
        try:
            obj.send_email(_msg)
        except Exception as f:
            print(f)
        try:
            send_to_wecom_text(reback, wecom_id, AgentId, Secret)
        except Exception as e:
            print(e)
    except KeyError as g:
        return f'环境变量获取错误：{g}'


if __name__ == '__main__':
    main()
