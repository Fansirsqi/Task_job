## update 2023-09-22

52开启了js反爬,暂时先不更新了,等我研究一阵

## update 2023-09-10

新增一些变量..

> 变量配置表

|Key|Value|COMMENT|
|:-             |:-                       |-:                        |
|`HITOKOTO`     | `True`/`False`          | 推送是否启用一言(默认启用) (非必填)|
|`SMTP_SERVER`  | `smtp.exmail.qq.com:465`| SMTP 发送邮件服务器，形如 `smtp.exmail.qq.com:465` (非必填)|
|`SMTP_SSL`     | `false`                 |SMTP 发送邮件服务器是否使用 SSL，填写 true 或 false (非必填)|
|`SMTP_EMAIL`   | `xxxx@qq.com`           |SMTP 收发件邮箱，通知将会由自己发给自己 (非必填)|
|`SMTP_PASSWORD`| `邮箱授权码`             |SMTP 登录密码，也可能为特殊口令，视具体邮件服务商说明而定 (非必填)|
|`SMTP_NAME`    | `发件昵称`               | SMTP 收发件人姓名，可随意填写 (非必填)|
|`SENDKEY`      | `Server酱 的sendkey`|(非必填),默认使用通道9;18|
|`WX_TOKEN`| `wxpusher的token`|(非必填)|
|`UIDS`|`需要推送的uid`|(非必填)|

发现一个问题~,仓库不去动他90天还是60天 工作流会自己停掉..

## update 2023-04-18

- 新增收费暂时没那么严格的`WxPusher`推送，免费额度足够造

- 新增环境变量服务于`WxPusher`
  - `WX_TOKEN`

  - `UIDS`

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202304181842177.png)

#### [获取`appToken`](https://wxpusher.zjiecode.com/docs/#/?id=获取apptoken)

在你创建应用的过程中，你应该已经看到`appToken`，如果没有保存，可以通过下面的方式重制它。

打开应用的后台<https://wxpusher.zjiecode.com/admin/，从左侧菜单栏，找到`appToken`菜单，在这里，你可以重置`appToken`，请注意，重置后，老的`appToken`会立即失效，调用接口会失败。>

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202304181838504.png)

#### [扫码关注应用](https://wxpusher.zjiecode.com/docs/#/?id=扫码关注应用)

创建应用以后，你可以看到应用的应用码和关注链接，你可以让你的用户通过下面2种方式来关注你的应用，关注你的应用以后，你就可以给他发送消息了。

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202304181838724.png)

#### [获取UID](https://wxpusher.zjiecode.com/docs/#/?id=获取uid)

目前有3种方式获取`UID`：

1. 关注公众号：`wxpusher`，然后点击「我的」-「我的`UID`」查询到`UID`；
2. 通过[创建参数二维码](https://wxpusher.zjiecode.com/docs/#/?id=create-qrcode)接口创建一个定制的二维码，用户扫描此二维码后，会通过[用户关注回调](https://wxpusher.zjiecode.com/docs/#/?id=subscribe-callback)把`UID`推送给你；
3. 通过[创建参数二维码](https://wxpusher.zjiecode.com/docs/#/?id=create-qrcode)接口创建一个定制的二维码，然后用[查询扫码用户`UID`](https://wxpusher.zjiecode.com/docs/#/?id=query-uid)接口，查询扫描此二维码的用户`UID`；

## update 2023-03-22

- 删除企业微信，邮箱通知，改用Server酱

- <font color='red'>请务必删除之前设置的所有变量名称,以免造成不必要的威胁</font>

## 如何配置?

1. `pip install -r .\requirements.txt`

2. 参考如下方式配置`COOKIE_CONFIG`变量,`{}`也要带上

```json
{
  "自定义你的账户名1": "账号1cookie",
  "自定义你的账户名2": "账号2cookie"
}
```

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221759547.png)

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221803100.png)

3. 设置`SENDKEY`变量,即server酱的`SendKey`

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221804789.png)

4. > 请求时间是每天的`GithubAction`主机所在时间,
   >
   > 换算到北京时间大概是+8
   >
   > 请访问`main.yml`第10行的`- cron: '59 23 * * *'`
   >
   > 所以第二天的7点59左右,大概是,这个多少会有延迟

<center>
<h2>运行结果:</h2>

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221816356.png)

<h2>手机上收到的样式:</h2>

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221819697.png)

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221817700.png)

<h2>至于为什么是这样:</h2>

![](https://cdn.jsdelivr.net/gh/Fansirsqi/blog-Images/images/202303221818476.png)

</center>
