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
