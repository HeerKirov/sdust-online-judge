Virtual Judge Adapter for SDUSTOJ
==

用于SDUSTOJ的Virtual Judge功能适配器。作为评测机对接评测端，用于评测题库内的虚拟题目。  

## 使用方法

### 依赖的python包

* psycopg2 (2.6.2)
* redis (2.10.5)
* SQLAlchemy (1.1.5)
* requests (2.18.1)

### 部署方法
1. 配置该部分服务所需的数据库。该服务需要使用PostgreSQL数据库。
2. 在`conf.py`中修改数据库配置与用作VJ链接的账户的用户名和密码。建议使用专用账户仅用作提交服务，且不在多个评测机上复用。
2. 执行根目录下的`problem_updater.py`,`submissino_reporter.py`,`submission_reptile.py`,`submission_updater.py`即可。  
也可以直接执行`app.sh`快速启动。
