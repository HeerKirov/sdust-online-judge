SDUST Online Judge Client  
==

这是SDUST Online Judge的用户端实现，用于对用户提供基于机构和课程的答题服务。  

基于Django REST framework开发，前端基于Bootstrap4, 使用HTTP请求和用户端帐号与评测端通过后台服务对接。  

用户端相关功能仍在开发中。

<hr>

## 功能

* 向教学系统内用户提供管理服务：
    * 基于机构与子机构进行人员与资源管理
    
    * 基于课程基类与课程体系管理教学内容
    
* 灵活的答题服务：
    * 基于任务和任务组发布教学、作业、考试任务
    
    * 可以灵活配置任务形式，满足多种不同的教学场景需要

## 软件环境

* Python3.4+
    依赖的包：
    
    * Django (1.10.5)
    
    * Django REST Framework (3.5.3)
    
    * drf-nested-routers (0.11.1)
    
    * django-filter (1.0.1)
    
    * psycopg2 (2.6.2)
    
    * redis (2.10.5)
    
    * requests (2.18.1)
    
    * django-bulk-update (2.2.0)

## 运行 & 部署

用户端分为两个部分。
* HTTP服务器部分：与普通Django项目相同，运行时需要PostgreSQL数据库正常运行。Redis数据库目前处于保留状态。

* 同步服务部分：运行sdustoj_client目录下的app.sh在后台启动更新服务。