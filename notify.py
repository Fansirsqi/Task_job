#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import json
import os
import threading
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from dotenv import load_dotenv
import requests

load_dotenv()
# 原先的 print 函数和主线程的锁
_print = print
mutex = threading.Lock()


# 定义新的 print 函数
def print(text, *args, **kw):
    """
    使输出有序进行，不出现多线程同一时间输出导致错乱的问题。
    """
    with mutex:
        _print(text, *args, **kw)


# 通知服务
# fmt: off
push_config = {
    'HITOKOTO': True,                  # 启用一言（随机句子）
    
    'SMTP_SERVER': '',                  # SMTP 发送邮件服务器，形如 smtp.exmail.qq.com:465
    'SMTP_SSL': 'false',                # SMTP 发送邮件服务器是否使用 SSL，填写 true 或 false
    'SMTP_EMAIL': '',                   # SMTP 收发件邮箱，通知将会由自己发给自己
    'SMTP_PASSWORD': '',                # SMTP 登录密码，也可能为特殊口令，视具体邮件服务商说明而定
    'SMTP_NAME': '',                    # SMTP 收发件人姓名，可随意填写
    
    'SENDKEY': '',                      # Server酱的 SENDKEY
    
    'WX_TOKEN': '',                     # wxpusher的 Token
    'UIDS':''
}
notify_function = []
# fmt: on

# 首先读取 面板变量 或者 github action 运行变量
for k in push_config:
    if os.getenv(k):
        v = os.getenv(k)
        push_config[k] = v


def smtp(title: str, content: str) -> None:
    """
    使用 SMTP 邮件 推送消息。
    """
    if (
        not push_config.get("SMTP_SERVER")
        or not push_config.get("SMTP_SSL")
        or not push_config.get("SMTP_EMAIL")
        or not push_config.get("SMTP_PASSWORD")
        or not push_config.get("SMTP_NAME")
    ):
        print(
            "SMTP 邮件 的 SMTP_SERVER 或者 SMTP_SSL 或者 SMTP_EMAIL 或者 SMTP_PASSWORD 或者 SMTP_NAME 未设置!!\n取消推送"
        )
        return
    print("SMTP 邮件 服务启动")

    message = MIMEText(content, "plain", "utf-8")
    message["From"] = formataddr(
        (
            Header(push_config.get("SMTP_NAME"), "utf-8").encode(),
            push_config.get("SMTP_EMAIL"),
        )
    )
    message["To"] = formataddr(
        (
            Header(push_config.get("SMTP_NAME"), "utf-8").encode(),
            push_config.get("SMTP_EMAIL"),
        )
    )
    message["Subject"] = Header(title, "utf-8")

    try:
        smtp_server = (
            smtplib.SMTP_SSL(push_config.get("SMTP_SERVER"))
            if push_config.get("SMTP_SSL") == "true"
            else smtplib.SMTP(push_config.get("SMTP_SERVER"))
        )
        smtp_server.login(
            push_config.get("SMTP_EMAIL"), push_config.get("SMTP_PASSWORD")
        )
        smtp_server.sendmail(
            push_config.get("SMTP_EMAIL"),
            push_config.get("SMTP_EMAIL"),
            message.as_bytes(),
        )
        smtp_server.close()
        print("SMTP 邮件 推送成功！")
    except Exception as e:
        print(f"SMTP 邮件 推送失败！{e}")


def server_chan(title, context):
    """
    Server酱推送
    Args:
        title (_type_): _通知标题_
        context (_type_): _通知内容_
    """
    if not push_config.get("SENDKEY"):
        print("Server酱 推送失败！未配置 Server酱 SENDKEY")
        return
    print("Server酱 推送中...(*≧︶≦))(￣▽￣* )ゞ")
    data = {"title": title, "desp": context, "short": "", "channel": "9"}
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
    headers = {"Content-type": "application/json"}
    url = f'https://sctapi.ftqq.com/{push_config.get("SENDKEY")}.send'
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
            print(f"ConnectionError:{e}")


def wx_pusher(title, content):
    """
    wx_pusher推送
    Args:
        wxpuser_token (_type_): _token_
        uids (_type_): _description_
        msg (_type_): _description_
    """
    if not push_config.get("WX_TOKEN") or not push_config.get("UIDS"):
        print("WX_TOKEN 或者 UIDS 未配置,请检查")
        return
    uids:list = str(push_config.get("UIDS")).split(';')
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = json.dumps(
        {
            "appToken": f'{push_config.get("WX_TOKEN")}',
            "content": f"## 吾爱破解Task任务执行日志 \n{title}",  # Title
            "summary": f"{content}",  #
            "contentType": 3,
            "uids": uids,
            "verifyPay": False,
        }
    )
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }
    while True:
        try:
            r = requests.request("POST", url, headers=headers, data=payload).json()
            # print(json.dumps(r))
            msg = r["msg"]
            status = r["data"][0]["status"]
            print(f"🎁 WxPusher {status} - {msg}")
            break
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError:{e}")


def one() -> str:
    """
    获取一条一言。
    :return:
    """
    url = "https://v1.hitokoto.cn/"
    res = requests.get(url).json()
    return res["hitokoto"] + "    ----" + res["from"]


if (
    push_config.get("SMTP_SERVER")
    and push_config.get("SMTP_SSL")
    and push_config.get("SMTP_EMAIL")
    and push_config.get("SMTP_PASSWORD")
    and push_config.get("SMTP_NAME")
):
    notify_function.append(smtp)
if push_config.get("SENDKEY"):
    notify_function.append(server_chan)
if push_config.get("WX_TOKEN") and push_config.get("UIDS"):
    notify_function.append(wx_pusher)


def send(title: str, content: str) -> None:
    if not content:
        print(f"{title} 推送内容为空！")
        return

    hitokoto = bool(push_config.get("HITOKOTO"))

    text = one() if hitokoto else ""
    title += "\n" + text
    print(title)
    ts = [
        threading.Thread(target=mode, args=(title, content), name=mode.__name__)
        for mode in notify_function
    ]
    [t.start() for t in ts]
    [t.join() for t in ts]


def main():
    send("吾爱Task签到反馈", "吾爱Task签到反馈;BYS")


if __name__ == "__main__":
    main()
    # print(one())
    # print()
