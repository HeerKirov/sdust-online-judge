# -*- coding: utf-8 -*-
from functions.submission import analyse

# 订阅SDUSTOJ的提交频道，接收来自SDUSTOJ的提交消息并与SDUSTOJ的其他评测机竞争提交。
# 根据获得的提交ID从SDUSTOJ数据库获得提交，将其转换为一至多个HUSTOJ中的提交，写入HUSTOJ的数据库。并标记当前未完成的提交。

# SDUSTOJ的提交消息将根据不同的编程环境（语言）被发送到不同的频道上，
# 例如C语言的提交，其消息将发送到C语言提交对应的频道上，订阅该频道的评测机将收到通知，
# 并通过一个仅含该提交的队列参与该提交的竞争，队列中仅为一个标记，不含提交信息。竞争到的评测机将自行获取提交信息进行评测。

# 当Manager竞争到提交后，将从SDUSTOJ的数据库中获取提交，并根据提交对应的题目在HUSTOJ数据库中查找对应的题目。
# 如果存在未对应的题目，则将自动同步题目，重新执行查询。
# 在找到对应的一至多个题目后，Manager将为每个HUSTOJ题目生成一个对应提交写入HUSTOJ数据库。生成的提交将自动被HUSTOJ进行评测。

# 当提交生成完毕后，Manager会将SDUSTOJ提交ID加入未完成提交队列，
# 并通过Redis的哈希记录此提交的测试数据与HUSTOJ提交的映射关系（一组数据一个提交），供submission_reporter追踪。

analyse()  # 启动一项服务，进行提交解析队列的轮询，处理本机的所有提交。
