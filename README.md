![摸鱼派cn.png](https://b3logfile.com/file/2023/05/摸鱼派-cn-owZQT8f.png)

# fishpi-pyclient

> 摸鱼派聊天室 python 命令行客户端

基于摸鱼打工人社区——摸鱼派开放 API 开发的摸鱼派聊天室 python 客户端程序，可以在里面边写 Bug 边愉快地吹水摸鱼。
全平台客户端支持，支持一键docker部署。
## 功能
- 全平台支持
  - [x] Windows
  - [x] macOS
  - [x] linux
  - [x] docker
- 🥷 账号多开
  - 一键切换
  - 记住密码
- 📑 查看帖子
  - 发送评论
  - 帖子推送
    - [x] [Bolo](https://github.com/adlered/bolo-solo)/[Solo](https://github.com/88250/solo)
    - [ ] 博客园
    - [ ] 掘金
    - [ ] 自建博客欢迎 PR
- 💬 聊天模式
  - 💬 私聊
  - 💬 聊天吹水
  - 系统通知
    - 聊天室@你
    - 有人私聊你
    - 聊天室关键词
  - 🌈 自定义字体颜色
  - 🤖️ 自动复读
  - 🤖️ 自动领取昨日奖励
  - 🌛 发送清风明月
  - 聊天室消息撤回
  - 小尾巴去除
  - 小冰天气解析
  - 🧠 自言自语
    - 自定义语句池
    - 定时发送
- 命令模式
  - 命令/聊天模式切换
    - (聊天模式也可以执行命令)
  - 进入答题模式(前缀自动加上 鸽)
  - ⬆️ 社区快捷命令
    - 领取昨日活跃度奖励
    - 查看个人积分
    - 查看签到状态
    - 转账
    - 发送清风明月
    - 查看当前活跃度
    - 查看在线用户列表
    - 查询用户详细信息
    - 配置文件导出
    - 🈲️ 小黑屋功能
      - 拒绝接收黑名单在聊天室发送的信息 (红包除外 😂 )
      - 将某人从小黑屋中放出
    - 🈲️ 关键字屏蔽
    - 发红包 🧧
      - 拼手气红包
      - 普通红包
      - 专属红包
      - 心跳红包
      - 猜拳红包
      - 设置抢红包等待时间
      - 抢猜拳红包最大限制
      - 🧧 自动化抢红包（脚本哥）
        - 自定义抢红包延时
        - 心跳红包防止踩坑
        - 心跳红包风险预测

超级丰富的命令行指令，像极客一样操作命令行

```text
[#cli] 进入命令交互模式
[#cr] 进入聊天室模式
[#chat] 私聊 #chat Gakkiyomi 进入和Gakkiyomi的私聊窗口
[#siguo] 思过崖
[#article] 看帖 (默认显示20个帖子) [view|page] (int) / 回帖 #article comment (str)
[#rp] 1 128 1个128积分 (默认5个,128积分)拼手气红包
[#rp-ave] 1 128 1个128积分 (默认5个,32积分)平均红包
[#rp-hb] 5 128 5个128积分 (默认5个,32积分)心跳红包
[#rp-rps] 0 128 128积分 (0=石头 1=剪刀 2=布)猜拳红包
[#rp-rps-limit] 100 (猜拳红包超过100的不抢)
[#rp-to] 32 Gakkiyomi,xiaoIce (积分 用户)专属红包
[#rp-time] 3 设置抢红包等待时间
[#bm] 发送清风明月
[#config] 查看,导出配置文件 config [dump|show] {-d|-c} (file_path)
[#answer] 进入|退出 答题模式
[#checked] 查看当前是否签到
[#reward] 领取昨日活跃奖励
[#revoke] 撤回最近一条聊天室消息
[#transfer] 32 Gakkiyomi 送给你 (积分 用户 留言)
[#point] 查看当前个人积分
[#online-users] 查看当前在线的用户列表
[#user username] 输入 #user 用户名 可查看此用户详细信息 (#user Gakkiyomi)
[#me] 查看当前在线账号 #me (-d)  #me article (view | page){index} 查看自己的帖子
[#push] 推送帖子 #push article {index} 文章索引号
[#account] 查看分身账号
[#su] 账号切换 #su Gakkiyomi
[#bl] 查看黑名单列表
[#op-mode] 设置窗口输出模式 op-mode {file|backup|console} 支持控制台输出,文件输出,备份输出模式
[#op-path] 设置输出路径文件 op-path /abc/chatroom.log
[#ban keyword|user xxx] 将某人或者关键词送入黑名单
[#release keyword|user xxx] 将某人或者关键词解除黑名单
[#notification {-d|-a}}] keyword 动态修改关键词提醒
[#liveness] 查看当前活跃度(⚠️慎用，如果频繁请求此命令(最少间隔30s)，登录状态会被直接注销,需要重启脚本！)
```

## 安装

[版本列表](https://github.com/gakkiyomi/fishpi-pyclient/releases)

### Windows 系统

下载后，双击打开

### MacOS 系统

下载后，执行如下命令

1. ```bash
   chmod a+x ./fishpi-pyclient
   ```

2. ```bash
   ./fishpi-pyclient
   ```

然后需要在偏好设置这里,如下图:
![WechatIMG482.jpg](https://file.fishpi.cn/2023/12/WechatIMG482-3c599a0e.jpg)

### linux 系统
可以使用pip进行安装或者通过docker进行使用
#### docker
~~~bash
docker pull gakkiyomi/fishpi-pyclient:v2.1.9
~~~
交互模式进行聊天
~~~bash
docker run -it gakkiyomi/fishpi-pyclient:v2.1.9 -u username -p password -c <两步验证码>
~~~
后台红包机器人
~~~bash
docker run -d gakkiyomi/fishpi-pyclient:v2.1.9 -u username -p password -c <两步验证码>
~~~

### pip 安装

环境: Python3.12 以上

执行

```bash
pip install fishpi-pyclient
```

```bash
fishpi-pyclient -u username -p password -c <两步验证码>
```

## 调试

```bash
python core.py
```

## 效果

![fenshen.png](https://file.fishpi.cn/2023/12/账号分身-0a25be81.png)
![截屏2023-12-10-13.42.17.png](https://file.fishpi.cn/2023/12/截屏20231210134217-df6839af.png)
![image.png](https://file.fishpi.cn/2023/06/image-d4da9bf7.png)
![redpacket](https://file.fishpi.cn/2023/06/image-d0ad7756.png)
![image.png](https://pwl.stackoverflow.wiki/2022/01/image-f74aae7e.png)
![image.png](https://pwl.stackoverflow.wiki/2022/01/image-1b685256.png)

## 🔑 JetBrains OS licenses

`pwl-chat-ptyhon` had been being developed with `PyCharm IDE` under the free JetBrains Open Source license(s) granted by JetBrains s.r.o., hence I would like to express my thanks here.

<a href="https://www.jetbrains.com/?from=pwl-chat-ptyhon" target="_blank"><img src="https://b3logfile.com/file/2021/05/jetbrains-variant-2-42d96aa4.png" width="250" align="middle"/></a>
