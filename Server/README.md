SDUST Online Judge Server
==

这是SDUST Online Judge的评测端，用于对用户端提供基于RESTful API的题目评测服务，使用评测机进行题目的评测。

基于Django REST Framework开发，前端基于Bootstrap4，通过Redis与评测机通信，数据库使用PostgreSQL。

<hr>

## 功能

* 对用户端提供基于RESTful API的题目评测服务：
    
    * 查询题目
    
    * 查询题库及题库内目录
    
    * 查询系统支持的编程环境
    
    * 查询提交记录
    
    * 提交代码
    
* 评测端内部管理：
    
    * 题库管理（管理题元/题目/题库）
    
    * 用户端管理
    
    * 评测端管理员管理
    
    * 查看所有提交记录
    
    * 提交代码进行测试
    
## 软件环境

* Python3.4+

    依赖的包：
    
    * Django (1.10.5)
    
    * Django REST Framework (3.5.3)
    
    * drf-nested-routers (0.11.1)
    
    * django-filter (1.0.1)
    
    * psycopg2 (2.6.2)
    
    * redis (2.10.5)
    
    * DRF Docs (0.0.11)
    
    * html2text (2016.9.19)
    
    * requests (2.18.1)

## 运行 & 部署

与普通Django项目相同，运行时需要PostgreSQL与Redis的正常运行。

运行与部署可参见[Django官方文档](https://docs.djangoproject.com/en/1.10/howto/deployment/)。