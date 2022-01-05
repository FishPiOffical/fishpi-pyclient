# pwl-chat-python
> 摸鱼派聊天室简易python客户端

基于摸鱼打工人社区——摸鱼派开放 API 开发的摸鱼派聊天室python客户端程序，可以在里面边写 Bug 边愉快地吹水摸鱼。 。

* 💬 基本聊天吹水；
* ⬆️ 社区快捷命令
    * 领取昨日活跃度奖励
    * 查看个人积分
    * 查看签到状态
    * 查看当前活跃度
    * 查看聊天室在线用户列表
    * 查询用户详细信息
* 🤖️ 自动复读    
* 🧧 自动化抢红包（脚本哥）
    * 自定义抢红包延时
    * 心跳红包防止踩坑
    * 心跳红包风险预测

## 效果
![image.png](https://pwl.stackoverflow.wiki/2022/01/image-71dba0ea.png)
![image.png](https://pwl.stackoverflow.wiki/2022/01/image-fac11dcb.png)
![image.png](https://pwl.stackoverflow.wiki/2022/01/image-1b685256.png)

## 安装
环境: Python3

### 第一步
执行
~~~bash
pip install -r requirements.txt
~~~

### 第二步
在 `config.ini`中配置摸鱼派账号登陆信息



### 第三步
执行
~~~bash
python core.py
~~~

后台执行
~~~bash
nohup python -u core.py >> pwl.log 2>&1 &
~~~

