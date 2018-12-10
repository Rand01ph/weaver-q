# weaver-q
A task queue with Redis

# lua
使用lua实现入队，出队的原子操作

# TODO
1. 入队
2. 出队
3. 重试
4. backoff
5. 任务依赖(检查依赖task_id是否完成，没有完成的话优先执行task_id，并且将当前task入队)

# 技术栈
Python + Lua + Redis
使用dill序列化python task

# 细节
weaver:<task_queue_name>:tasks  使用hash结构，存储 {task_id: task_dill}

weaver:<task_queue_name>:locks  使用hash结构，存储 {task_id: lock过期时间}

weaver:<task_queue_name>:nattempts  使用hash结构，存储 {task_id: 任务尝试次数}

weaver:<task_queue_name>:tid-circle  使用list结构，存储 task_id队列, 'end-of-circle'标记队列尾

weaver:<task_queue_name>:done  使用set结构，用于等待gc，重新入队等

weaver:<task_queue_name>:requeue  使用set结构，用于允许重新入队功能


# Inspired by carmine
