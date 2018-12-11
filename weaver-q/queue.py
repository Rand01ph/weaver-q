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

if redis.call('exists', KEYS[3], task_id) ~= 1 then
    redis.call('lpush', KEYS[3], 'end-of-circle');
end

redis.call('lpush', KEYS[3], task_id);

return task_id;
"""

DEQUEUE_LUA = """\
local task_id = redis.call('rpoplpush', KEYS[2], KEYS[2]);

local task_dill = redis.call('hget', KEYS[1], task_id)

return {task_id, task_dill};
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
        self._dequeue = self.conn.register_script(DEQUEUE_LUA)

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
        print task_dill
        queue_ret = self._enqueue(keys=[self.task_data_key,
                                        self.task_done_key,
                                        self.tid_list_key], args=[task_id, task_dill])

    def dequeue(self, lock_time=60):
        """
        出队操作
        :return:
        """
        print self._dequeue(keys=[self.task_data_key,
                                  self.tid_list_key], args=[lock_time])
