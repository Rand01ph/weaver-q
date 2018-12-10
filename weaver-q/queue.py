#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import dill

from connections import RedisQ

logger = logging.getLogger(__name__)

redis_conn = RedisQ(url="redis://127.0.0.1:6379/0")

ENQUEUE_LUA = """\
local task_id = ARGV[1];
local task_dill = ARGV[2];

redis.call('hset', KEYS[1], task_id, task_dill);

if redis.call('exists', KEYS[4], task_id) ~= 1 then
    redis.call('lpush', KEYS[4], 'end-of-circle');
end

redis.call('lpush', KEYS[4], task_id);

return task_id;
"""


class Queue(object):

    def __init__(self, prefix='weaver', qname='normal'):
        self.q_prefix = '{0}:{1}:'.format(prefix, qname)

        self.task_data_key = self.q_prefix + 'tasks'
        self.task_locks_key = self.q_prefix + 'locks'
        self.tid_list_key = self.q_prefix + 'tid-circle'
        self.task_done_key = self.q_prefix + 'done'

        self.conn = redis_conn.conn
        self._enqueue = self.conn.register_script(ENQUEUE_LUA)

    def enqueue(self, task_id, task_fn, task_args):
        """
        入队操作
        :return:
        """
        task_data = {
            "task_fn": task_fn,
            "task_args": task_args
        }
        logger.info("get into weaver queue data is %s", task_data)
        task_dill = dill.dumps(task_data)
        queue_ret = self._enqueue(keys=[self.task_data_key,
                                        self.task_locks_key,
                                        self.task_done_key,
                                        self.tid_list_key], args=[task_id, task_dill])

    def dequeue(self):
        """
        出队操作
        :return:
        """
        pass
