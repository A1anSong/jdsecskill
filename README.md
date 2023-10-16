# jdsecskill

某电商平台抢购技术研究

平台地址：aHR0cHM6Ly93d3cuamQuY29tLw==

对逆向感兴趣，写了这个项目，目前只是临时拼凑实现了抢购功能，自己挂着跑了一个月，并无更新计划

## 目录结构

***/hook:*** 使用frida hook数据的保留脚本

***convert.py:*** 将抓包数据转换为请求数据的脚本（使用Fiddler保存的数据）

***jd_user.py:*** 封装的JDUser类

***main.py:*** 主程序

***uers.py.example:*** 需要填写抓包获取的一些用户信息，其中是必填项

***页面请求.md*** 记录一些页面请求的参数

## 备注

[http://127.0.0.1:9998/sign]() 是获取逆向的sign参数的接口，详情可见另一个项目
[jd_unidbg](https://github.com/A1anSong/jd_unidbg)