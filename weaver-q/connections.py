#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import ConnectionPool, StrictRedis


class RedisQ(object):
    redis_client = StrictRedis

    def __init__(self, connection_pool=None, url=None, **connection_params):
        if url:
            connection_pool = ConnectionPool.from_url(
                url, decode_components=True
            )
        elif connection_pool is None:
            connection_pool = ConnectionPool(**connection_params)

        self.pool = connection_pool
        self.conn = self.redis_client(connection_pool=connection_pool)
